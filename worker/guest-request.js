// POST /api/guest-request handler. Pure module: no cloudflare: imports, so it
// runs under node --test. Email delivery is injected as deps.sendEmail.
//
// Contract: JSON body {name, email, companyRole, link, story, nickname, t}.
// "nickname" is a honeypot and "t" is the epoch-ms render time (time trap).

import { validateGuestRequest } from "./validate.js";
import { stripHeaderBreaks } from "./mime.js";

const MAX_BODY_BYTES = 8 * 1024;
const MIN_FILL_MS = 3000;
const USER_AGENT_MAX = 200;
const SUBJECT_MAX = 200;
const RESEND_ENDPOINT = "https://api.resend.com/emails";

// The form appends "You can also message me on LinkedIn." to these, so they
// must not mention LinkedIn themselves.
const MSG_UNAVAILABLE = "Guest requests are temporarily unavailable.";
const MSG_SEND_FAILED =
  "Something went wrong sending your request. Please try again in a minute.";
const MSG_BAD_REQUEST =
  "Something was wrong with that request. Please refresh and try again.";

const BASE_HEADERS = Object.freeze({
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store",
  "x-content-type-options": "nosniff",
});

export function jsonResponse(status, body, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...BASE_HEADERS, ...extraHeaders },
  });
}

const ok = () => jsonResponse(200, { ok: true });
const error = (status, message, field) =>
  jsonResponse(status, { ok: false, error: message, ...(field ? { field } : {}) });

function parseAllowedOrigins(env) {
  return String(env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((o) => o.trim().replace(/\/+$/, ""))
    .filter(Boolean);
}

function isLocalOrigin(origin) {
  return /^http:\/\/(localhost|127\.0\.0\.1)(:\d{1,5})?$/.test(origin);
}

export function isOriginAllowed(origin, env) {
  if (!origin) return false;
  if (parseAllowedOrigins(env).includes(origin)) return true;
  return env.ALLOW_LOCAL_ORIGINS === "1" && isLocalOrigin(origin);
}

function isJsonContentType(request) {
  const type = (request.headers.get("content-type") || "").split(";")[0].trim();
  return type.toLowerCase() === "application/json";
}

/**
 * Read the body with a hard byte cap. Returns null when it is too large.
 * Streams the body so a chunked upload with no content-length is cut off as
 * soon as it passes the cap instead of being buffered in full.
 */
async function readCappedText(request) {
  const declared = Number(request.headers.get("content-length"));
  if (Number.isFinite(declared) && declared > MAX_BODY_BYTES) return null;
  if (!request.body) return "";
  const reader = request.body.getReader();
  const chunks = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > MAX_BODY_BYTES) {
      await reader.cancel().catch(() => {});
      return null;
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(total);
  chunks.reduce((offset, chunk) => {
    bytes.set(chunk, offset);
    return offset + chunk.byteLength;
  }, 0);
  return new TextDecoder().decode(bytes);
}

/** True when the submission looks automated (honeypot filled, no/odd timestamp, or too fast). */
function isLikelyBot(body, now) {
  const honeypot = typeof body.nickname === "string" ? body.nickname.trim() : body.nickname;
  if (honeypot) return true;
  const renderedAt = Number(body.t);
  if (!Number.isFinite(renderedAt) || renderedAt <= 0) return true;
  return now - renderedAt < MIN_FILL_MS;
}

function errorMessage(err) {
  return err instanceof Error ? err.message : String(err);
}

async function isRateLimited(env, ip) {
  if (!env.GUEST_RL || typeof env.GUEST_RL.limit !== "function") return false;
  try {
    const { success } = await env.GUEST_RL.limit({ key: ip || "unknown" });
    return success === false;
  } catch (err) {
    console.error("guest-request: rate limiter error", errorMessage(err));
    return false; // fail open: the honeypot and time trap still apply
  }
}

function truncate(value, max) {
  return value.length > max ? value.slice(0, max - 1) + "…" : value;
}

export function buildSubject({ name, companyRole }) {
  return truncate(stripHeaderBreaks(`Guest request: ${name} (${companyRole})`), SUBJECT_MAX);
}

export function buildEmailText(fields, meta) {
  return [
    "New guest request from themakingofhostedbyjackpitts.com",
    "",
    `Name: ${fields.name}`,
    `Email: ${fields.email}`,
    `Company / role: ${fields.companyRole}`,
    `Link: ${fields.link || "(none)"}`,
    "",
    "Story:",
    fields.story,
    "",
    "----",
    `Submitted: ${meta.submittedAt}`,
    `Country: ${meta.country || "unknown"}`,
    `User agent: ${meta.userAgent || "unknown"}`,
    "",
    "Reply to this email to answer the guest directly.",
  ].join("\n");
}

async function sendViaResend(env, message, fetchImpl) {
  const res = await fetchImpl(RESEND_ENDPOINT, {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.RESEND_API_KEY}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      from: env.RESEND_FROM,
      to: [message.to],
      reply_to: message.replyTo,
      subject: message.subject,
      text: message.text,
    }),
  });
  if (!res.ok) throw new Error(`Resend responded ${res.status}`);
}

/** Try send_email first, then the optional Resend fallback. Never logs message content. */
async function deliver(env, deps, message) {
  try {
    await deps.sendEmail(message);
    return true;
  } catch (err) {
    console.error("guest-request: send_email failed", errorMessage(err));
  }

  const fetchImpl = deps.fetch || globalThis.fetch;
  if (!env.RESEND_API_KEY || !env.RESEND_FROM || !fetchImpl) return false;
  try {
    await sendViaResend(env, message, fetchImpl);
    return true;
  } catch (err) {
    console.error("guest-request: Resend fallback failed", errorMessage(err));
    return false;
  }
}

function isConfigured(env) {
  return Boolean(env.GUEST_REQUEST_TO && env.GUEST_REQUEST_FROM && env.GUEST_MAIL);
}

async function parseBody(request) {
  const text = await readCappedText(request);
  if (text === null) {
    return { response: error(413, "That request is too large. Please shorten your story.") };
  }
  try {
    const body = JSON.parse(text);
    if (body && typeof body === "object" && !Array.isArray(body)) return { body };
  } catch {
    // fall through to the 400 below
  }
  return { response: error(400, MSG_BAD_REQUEST) };
}

/**
 * @param {Request} request
 * @param {Record<string, any>} env
 * @param {{sendEmail:(m:{from:string,to:string,replyTo:string,subject:string,text:string})=>Promise<void>,
 *   fetch?:typeof fetch, now?:()=>number}} deps
 * @returns {Promise<Response>}
 */
export async function handleGuestRequest(request, env, deps) {
  if (request.method !== "POST") {
    return jsonResponse(405, { ok: false, error: "Method not allowed." }, { allow: "POST" });
  }
  if (!isOriginAllowed(request.headers.get("origin"), env)) {
    return error(403, "Forbidden.");
  }
  if (!isJsonContentType(request)) {
    return error(415, "Please send the form as JSON.");
  }

  const { body, response } = await parseBody(request);
  if (response) return response;

  const now = (deps.now || Date.now)();
  if (isLikelyBot(body, now)) return ok(); // fake success, nothing is sent

  const result = validateGuestRequest(body);
  if (!result.ok) return error(400, result.error, result.field);

  if (!isConfigured(env)) {
    console.error(
      "guest-request: not configured (need GUEST_REQUEST_TO, GUEST_REQUEST_FROM and the GUEST_MAIL send_email binding)"
    );
    return error(503, MSG_UNAVAILABLE);
  }

  const ip = request.headers.get("cf-connecting-ip") || "";
  if (await isRateLimited(env, ip)) {
    return error(429, "Too many requests. Please try again in a minute.");
  }

  const fields = result.value;
  const message = {
    from: env.GUEST_REQUEST_FROM,
    to: env.GUEST_REQUEST_TO,
    replyTo: stripHeaderBreaks(fields.email),
    subject: buildSubject(fields),
    text: buildEmailText(fields, {
      submittedAt: new Date(now).toISOString(),
      country: request.cf && request.cf.country,
      userAgent: truncate(stripHeaderBreaks(request.headers.get("user-agent") || ""), USER_AGENT_MAX),
    }),
  };

  const delivered = await deliver(env, deps, message);
  return delivered ? ok() : error(502, MSG_SEND_FAILED);
}
