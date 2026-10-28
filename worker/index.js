// Worker entry for frosty-pond-4366. The site itself is static assets; this
// script only runs first for /api/* (see run_worker_first in wrangler.toml).
// Everything else is handed straight to the static assets binding.

import { EmailMessage } from "cloudflare:email";
import { handleGuestRequest, jsonResponse } from "./guest-request.js";
import { buildMimeMessage } from "./mime.js";

const SHOW_NAME = "The Making Of Hosted By Jack Pitts";

function makeSendEmail(env) {
  return async ({ from, to, replyTo, subject, text }) => {
    const raw = buildMimeMessage({ from, fromName: SHOW_NAME, to, replyTo, subject, text });
    await env.GUEST_MAIL.send(new EmailMessage(from, to, raw));
  };
}

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);

    if (pathname === "/api/guest-request") {
      try {
        return await handleGuestRequest(request, env, { sendEmail: makeSendEmail(env) });
      } catch (err) {
        console.error("guest-request: unhandled error", err instanceof Error ? err.message : String(err));
        return jsonResponse(500, {
          ok: false,
          error: "Something went wrong. Please try again in a minute.",
        });
      }
    }

    if (pathname === "/api" || pathname.startsWith("/api/")) {
      return jsonResponse(404, { ok: false, error: "Not found." });
    }

    return env.ASSETS.fetch(request);
  },
};
