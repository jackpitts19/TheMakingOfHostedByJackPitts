// Run with: node --test tests/worker/*.test.mjs
import { test, describe, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";

import { handleGuestRequest } from "../../worker/guest-request.js";
import { normalizeLink } from "../../worker/validate.js";
import { buildMimeMessage, encodeQuotedPrintable } from "../../worker/mime.js";

const ORIGIN = "https://themakingofhostedbyjackpitts.com";
const NOW = 1_800_000_000_000;
const ENDPOINT = `${ORIGIN}/api/guest-request`;

const validBody = (overrides = {}) => ({
  name: "Jane Doe",
  email: "jane@example.com",
  companyRole: "Founder, Acme Supply",
  link: "linkedin.com/in/janedoe",
  story: "Started in my garage in 2009 and grew to forty employees.",
  nickname: "",
  t: NOW - 10_000,
  ...overrides,
});

const baseEnv = (overrides = {}) => ({
  ALLOWED_ORIGINS: ORIGIN,
  GUEST_REQUEST_FROM: "guest-requests@themakingofhostedbyjackpitts.com",
  GUEST_REQUEST_TO: "inbox@example.org",
  GUEST_MAIL: { send: async () => {} },
  ...overrides,
});

function makeRequest({
  method = "POST",
  origin = ORIGIN,
  contentType = "application/json",
  body = validBody(),
  rawBody,
  headers = {},
} = {}) {
  const h = new Headers(headers);
  if (origin) h.set("origin", origin);
  if (contentType) h.set("content-type", contentType);
  const init = { method, headers: h };
  if (method !== "GET" && method !== "HEAD") {
    init.body = rawBody !== undefined ? rawBody : JSON.stringify(body);
  }
  return new Request(ENDPOINT, init);
}

function makeDeps({ sendImpl, fetchImpl } = {}) {
  const sent = [];
  const fetched = [];
  return {
    sent,
    fetched,
    deps: {
      now: () => NOW,
      sendEmail: async (msg) => {
        sent.push(msg);
        if (sendImpl) await sendImpl(msg);
      },
      fetch: async (url, init) => {
        fetched.push({ url, init });
        return fetchImpl ? fetchImpl(url, init) : new Response("{}", { status: 200 });
      },
    },
  };
}

async function call(reqOpts, env = baseEnv(), depOpts) {
  const ctx = makeDeps(depOpts);
  const res = await handleGuestRequest(makeRequest(reqOpts), env, ctx.deps);
  const json = await res.json();
  return { res, json, ...ctx };
}

const failingSend = async () => {
  throw new Error("boom");
};

// Silence expected console.error output from failure-path tests.
let originalError;
beforeEach(() => {
  originalError = console.error;
  console.error = () => {};
});
afterEach(() => {
  console.error = originalError;
});

describe("request gating", () => {
  test("GET returns 405 with Allow header", async () => {
    const { res, json } = await call({ method: "GET" });
    assert.equal(res.status, 405);
    assert.equal(res.headers.get("allow"), "POST");
    assert.equal(json.ok, false);
  });

  test("responses carry no-store and nosniff", async () => {
    const { res } = await call({});
    assert.equal(res.headers.get("cache-control"), "no-store");
    assert.equal(res.headers.get("x-content-type-options"), "nosniff");
    assert.match(res.headers.get("content-type"), /application\/json/);
  });

  test("cross-origin POST returns 403", async () => {
    const { res, sent } = await call({ origin: "https://evil.example" });
    assert.equal(res.status, 403);
    assert.equal(sent.length, 0);
  });

  test("missing Origin returns 403", async () => {
    const { res } = await call({ origin: null });
    assert.equal(res.status, 403);
  });

  test("localhost origin only allowed when ALLOW_LOCAL_ORIGINS is 1", async () => {
    const denied = await call({ origin: "http://localhost:8787" });
    assert.equal(denied.res.status, 403);
    const allowed = await call(
      { origin: "http://127.0.0.1:8787" },
      baseEnv({ ALLOW_LOCAL_ORIGINS: "1" })
    );
    assert.equal(allowed.res.status, 200);
    const stillDenied = await call(
      { origin: "http://localhost.evil.example" },
      baseEnv({ ALLOW_LOCAL_ORIGINS: "1" })
    );
    assert.equal(stillDenied.res.status, 403);
  });

  test("wrong content type returns 415", async () => {
    const { res } = await call({ contentType: "application/x-www-form-urlencoded", rawBody: "a=b" });
    assert.equal(res.status, 415);
  });

  test("JSON with charset parameter is accepted", async () => {
    const { res } = await call({ contentType: "application/json; charset=utf-8" });
    assert.equal(res.status, 200);
  });

  test("oversized body returns 413", async () => {
    const { res, sent } = await call({ body: validBody({ story: "x".repeat(9000) }) });
    assert.equal(res.status, 413);
    assert.equal(sent.length, 0);
  });

  test("chunked oversized body with no content-length is cut off and returns 413", async () => {
    const CHUNK = new Uint8Array(1024).fill(120);
    const TOTAL_CHUNKS = 20_000; // about 20 MB if read in full
    let pulled = 0;
    let cancelled = false;
    const stream = new ReadableStream({
      pull(controller) {
        pulled += 1;
        if (pulled > TOTAL_CHUNKS) controller.close();
        else controller.enqueue(CHUNK);
      },
      cancel() {
        cancelled = true;
      },
    });
    const request = new Request(ENDPOINT, {
      method: "POST",
      headers: { origin: ORIGIN, "content-type": "application/json" },
      body: stream,
      duplex: "half",
    });
    assert.equal(request.headers.get("content-length"), null);
    const { deps, sent } = makeDeps();
    const res = await handleGuestRequest(request, baseEnv(), deps);
    assert.equal(res.status, 413);
    assert.equal(sent.length, 0);
    assert.ok(cancelled, "stream should be cancelled once the cap is passed");
    assert.ok(pulled < 50, `read ${pulled} chunks; should stop near 8 KB`);
  });

  test("invalid JSON returns 400", async () => {
    const { res, json } = await call({ rawBody: "{not json" });
    assert.equal(res.status, 400);
    assert.equal(json.ok, false);
  });

  test("JSON array body returns 400", async () => {
    const { res } = await call({ rawBody: "[1,2]" });
    assert.equal(res.status, 400);
  });
});

describe("bot traps", () => {
  test("filled honeypot returns fake success and sends nothing", async () => {
    const { res, json, sent } = await call({ body: validBody({ nickname: "bot" }) });
    assert.equal(res.status, 200);
    assert.deepEqual(json, { ok: true });
    assert.equal(sent.length, 0);
  });

  test("submit under 3 seconds returns fake success and sends nothing", async () => {
    const { res, json, sent } = await call({ body: validBody({ t: NOW - 1500 }) });
    assert.equal(res.status, 200);
    assert.deepEqual(json, { ok: true });
    assert.equal(sent.length, 0);
  });

  test("missing timestamp returns fake success and sends nothing", async () => {
    const { res, sent } = await call({ body: validBody({ t: undefined }) });
    assert.equal(res.status, 200);
    assert.equal(sent.length, 0);
  });
});

describe("validation", () => {
  const cases = [
    ["name", { name: "  " }],
    ["name", { name: "n".repeat(101) }],
    ["name", { name: 42 }],
    ["email", { email: "not-an-email" }],
    ["email", { email: `${"a".repeat(250)}@example.com` }],
    ["companyRole", { companyRole: "" }],
    ["companyRole", { companyRole: "c".repeat(151) }],
    ["link", { link: "javascript:alert(1)" }],
    ["link", { link: "ftp://example.com" }],
    ["link", { link: "not a url" }],
    ["link", { link: `https://example.com/${"p".repeat(300)}` }],
    ["story", { story: "too short" }],
    ["story", { story: "s".repeat(1501) }],
  ];

  for (const [field, override] of cases) {
    test(`400 for invalid ${field}: ${JSON.stringify(override).slice(0, 50)}`, async () => {
      const { res, json, sent } = await call({ body: validBody(override) });
      assert.equal(res.status, 400);
      assert.equal(json.ok, false);
      assert.equal(json.field, field);
      assert.ok(typeof json.error === "string" && json.error.length > 0);
      assert.equal(sent.length, 0);
    });
  }

  test("empty link is allowed (optional)", async () => {
    const { res } = await call({ body: validBody({ link: "" }) });
    assert.equal(res.status, 200);
  });

  test("normalizeLink prefixes bare domains with https", () => {
    assert.equal(normalizeLink("linkedin.com/in/jane"), "https://linkedin.com/in/jane");
    assert.equal(normalizeLink("http://acme.co"), "http://acme.co/");
    assert.equal(normalizeLink("localhost"), null);
    assert.equal(normalizeLink(""), "");
  });
});

describe("rate limit and config", () => {
  test("rate limited returns 429 and sends nothing", async () => {
    const keys = [];
    const env = baseEnv({
      GUEST_RL: {
        limit: async ({ key }) => {
          keys.push(key);
          return { success: false };
        },
      },
    });
    const { res, sent } = await call({ headers: { "cf-connecting-ip": "203.0.113.9" } }, env);
    assert.equal(res.status, 429);
    assert.deepEqual(keys, ["203.0.113.9"]);
    assert.equal(sent.length, 0);
  });

  test("rate limiter allowing passes through", async () => {
    const env = baseEnv({ GUEST_RL: { limit: async () => ({ success: true }) } });
    const { res } = await call({}, env);
    assert.equal(res.status, 200);
  });

  test("missing GUEST_REQUEST_TO returns 503", async () => {
    const { res, json, sent } = await call({}, baseEnv({ GUEST_REQUEST_TO: undefined }));
    assert.equal(res.status, 503);
    assert.match(json.error, /temporarily unavailable/);
    assert.equal(sent.length, 0);
  });

  test("missing GUEST_MAIL binding returns 503", async () => {
    const { res } = await call({}, baseEnv({ GUEST_MAIL: undefined }));
    assert.equal(res.status, 503);
  });
});

describe("delivery", () => {
  test("success sends one email with correct addresses and stripped headers", async () => {
    const body = validBody({
      name: "Jane\r\nBcc: victim@example.com",
      companyRole: "Founder\nX-Injected: yes",
      story: "Line one of my story.\r\nLine two goes here.",
    });
    const { res, json, sent } = await call({ body, headers: { "user-agent": "TestAgent/1.0" } });
    assert.equal(res.status, 200);
    assert.deepEqual(json, { ok: true });
    assert.equal(sent.length, 1);
    const msg = sent[0];
    assert.equal(msg.to, "inbox@example.org");
    assert.equal(msg.from, "guest-requests@themakingofhostedbyjackpitts.com");
    assert.equal(msg.replyTo, "jane@example.com");
    assert.doesNotMatch(msg.subject, /[\r\n]/);
    assert.equal(msg.subject, "Guest request: Jane Bcc: victim@example.com (Founder X-Injected: yes)");
    assert.match(msg.text, /Line one of my story\.\nLine two goes here\./);
    assert.match(msg.text, /Link: https:\/\/linkedin\.com\/in\/janedoe/);
    assert.match(msg.text, /User agent: TestAgent\/1\.0/);
  });

  test("email with CRLF injection attempt is rejected by validation", async () => {
    const { res, json } = await call({ body: validBody({ email: "a@b.co\r\nBcc: x@y.z" }) });
    assert.equal(res.status, 400);
    assert.equal(json.field, "email");
  });

  test("send failure without Resend returns 502", async () => {
    const { res, json } = await call({}, baseEnv(), { sendImpl: failingSend });
    assert.equal(res.status, 502);
    assert.match(json.error, /try again in a minute\./);
    assert.doesNotMatch(json.error, /LinkedIn/);
  });

  test("send failure falls back to Resend when configured", async () => {
    const env = baseEnv({ RESEND_API_KEY: "test-key", RESEND_FROM: "Show <show@example.net>" });
    const { res, fetched } = await call({}, env, { sendImpl: failingSend });
    assert.equal(res.status, 200);
    assert.equal(fetched.length, 1);
    assert.equal(fetched[0].url, "https://api.resend.com/emails");
    const payload = JSON.parse(fetched[0].init.body);
    assert.deepEqual(payload.to, ["inbox@example.org"]);
    assert.equal(payload.reply_to, "jane@example.com");
    assert.equal(payload.from, "Show <show@example.net>");
    assert.equal(fetched[0].init.headers.authorization, "Bearer test-key");
  });

  test("send and Resend both failing returns 502", async () => {
    const env = baseEnv({ RESEND_API_KEY: "test-key", RESEND_FROM: "show@example.net" });
    const { res } = await call({}, env, {
      sendImpl: failingSend,
      fetchImpl: async () => new Response("nope", { status: 500 }),
    });
    assert.equal(res.status, 502);
  });

  test("story text is never logged on failure", async () => {
    const logged = [];
    console.error = (...args) => logged.push(args.join(" "));
    const story = "My very private story that must stay out of logs.";
    await call({ body: validBody({ story }) }, baseEnv(), { sendImpl: failingSend });
    assert.ok(logged.length > 0);
    assert.ok(logged.every((line) => !line.includes(story)));
  });
});

describe("MIME builder", () => {
  test("builds required headers with CRLF and sender-domain Message-ID", () => {
    const raw = buildMimeMessage({
      from: "guest-requests@themakingofhostedbyjackpitts.com",
      fromName: "The Making Of Hosted By Jack Pitts",
      to: "inbox@example.org",
      replyTo: "jane@example.com",
      subject: "Guest request: Jane\r\nBcc: x@y.z",
      text: "Hello",
      date: new Date(Date.UTC(2026, 9, 28, 12, 0, 0)),
    });
    const [head, body] = raw.split("\r\n\r\n");
    const lines = head.split("\r\n");
    assert.ok(
      lines.includes(
        'From: "The Making Of Hosted By Jack Pitts" <guest-requests@themakingofhostedbyjackpitts.com>'
      )
    );
    assert.ok(lines.includes("To: <inbox@example.org>"));
    assert.ok(lines.includes("Reply-To: <jane@example.com>"));
    assert.ok(lines.includes("Subject: Guest request: Jane Bcc: x@y.z"));
    assert.ok(lines.includes("Date: Wed, 28 Oct 2026 12:00:00 +0000"));
    assert.ok(lines.includes("MIME-Version: 1.0"));
    assert.ok(lines.includes("Content-Type: text/plain; charset=utf-8"));
    assert.ok(lines.includes("Content-Transfer-Encoding: quoted-printable"));
    assert.ok(
      lines.some((l) => /^Message-ID: <[0-9a-f-]+@themakingofhostedbyjackpitts\.com>$/.test(l))
    );
    assert.ok(!lines.some((l) => l.startsWith("Bcc:")));
    assert.equal(body, "Hello\r\n");
  });

  test("RFC 2047 encodes non-ASCII subjects", () => {
    const raw = buildMimeMessage({
      from: "a@example.com",
      to: "b@example.com",
      subject: "Guest request: José Müller",
      text: "x",
    });
    const subjectLine = raw.split("\r\n").find((l) => l.startsWith("Subject:"));
    assert.match(subjectLine, /^Subject: =\?UTF-8\?B\?[A-Za-z0-9+/=]+\?=$/);
    const encoded = subjectLine.match(/\?B\?(.+)\?=/)[1];
    assert.equal(
      Buffer.from(encoded, "base64").toString("utf8"),
      "Guest request: José Müller"
    );
  });

  test("quoted-printable keeps lines at most 76 chars and round-trips", () => {
    const text = "café = good\n" + "word ".repeat(60).trim() + "\ntrailing space ";
    const qp = encodeQuotedPrintable(text);
    for (const line of qp.split("\r\n")) {
      assert.ok(line.length <= 76, `line too long: ${line.length}`);
    }
    const decoded = Buffer.from(
      qp
        .replace(/=\r\n/g, "")
        .replace(/\r\n/g, "\n")
        .replace(/=([0-9A-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16))),
      "latin1"
    ).toString("utf8");
    assert.equal(decoded, text);
  });
});
