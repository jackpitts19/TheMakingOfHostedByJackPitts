// Minimal, dependency-free RFC 5322 plain-text message builder for the
// Cloudflare send_email binding (EmailMessage takes a raw MIME string).
// The body is UTF-8 quoted-printable so long lines and non-ASCII text are safe.

const CRLF = "\r\n";
const QP_MAX_LINE = 76;
const ENCODED_WORD_MAX_BYTES = 45; // 45 bytes -> 60 base64 chars, under the 75-char limit

const encoder = new TextEncoder();

/** Remove CR, LF, NUL and other control characters from a header value. */
export function stripHeaderBreaks(value) {
  return String(value ?? "")
    .replace(/[\u0000-\u001f\u007f]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function isAscii(value) {
  return /^[\x20-\x7e]*$/.test(value);
}

function bytesToBase64(bytes) {
  let binary = "";
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary);
}

/** RFC 2047 encode a header value if it contains non-ASCII characters. */
export function encodeHeaderValue(value) {
  const clean = stripHeaderBreaks(value);
  if (isAscii(clean)) return clean;

  const words = [];
  let chunk = "";
  for (const ch of clean) {
    const next = chunk + ch;
    if (encoder.encode(next).length > ENCODED_WORD_MAX_BYTES) {
      words.push(chunk);
      chunk = ch;
    } else {
      chunk = next;
    }
  }
  if (chunk) words.push(chunk);

  return words
    .map((w) => `=?UTF-8?B?${bytesToBase64(encoder.encode(w))}?=`)
    .join(CRLF + " ");
}

function qpEncodeLine(line) {
  const bytes = encoder.encode(line);
  const tokens = [];
  bytes.forEach((b, i) => {
    const isWhitespace = b === 32 || b === 9;
    const isLast = i === bytes.length - 1;
    const isPrintable = b >= 33 && b <= 126 && b !== 61; // 61 is "="
    if (isPrintable || (isWhitespace && !isLast)) {
      tokens.push(String.fromCharCode(b));
    } else {
      tokens.push("=" + b.toString(16).toUpperCase().padStart(2, "0"));
    }
  });

  const out = [];
  let current = "";
  for (const token of tokens) {
    // Reserve one character for the soft-break "=".
    if (current.length + token.length > QP_MAX_LINE - 1) {
      out.push(current + "=");
      current = "";
    }
    current += token;
  }
  out.push(current);
  return out.join(CRLF);
}

/** Quoted-printable encode a UTF-8 text body with CRLF line endings. */
export function encodeQuotedPrintable(text) {
  return String(text ?? "")
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map(qpEncodeLine)
    .join(CRLF);
}

function formatDate(date) {
  return date.toUTCString().replace(/ GMT$/, " +0000");
}

function domainOf(address) {
  const at = address.lastIndexOf("@");
  return at === -1 ? "localhost" : address.slice(at + 1);
}

function formatMailbox(address, displayName) {
  const addr = stripHeaderBreaks(address);
  if (!displayName) return `<${addr}>`;
  const name = stripHeaderBreaks(displayName);
  const encodedName = isAscii(name)
    ? `"${name.replace(/["\\]/g, "\\$&")}"`
    : encodeHeaderValue(name);
  return `${encodedName} <${addr}>`;
}

/**
 * Build a raw RFC 5322 message.
 * @param {{from:string, fromName?:string, to:string, replyTo?:string,
 *   subject:string, text:string, date?:Date, messageId?:string}} opts
 */
export function buildMimeMessage({
  from,
  fromName,
  to,
  replyTo,
  subject,
  text,
  date = new Date(),
  messageId,
}) {
  const id =
    messageId || `<${crypto.randomUUID()}@${domainOf(stripHeaderBreaks(from))}>`;

  const headers = [
    `From: ${formatMailbox(from, fromName)}`,
    `To: <${stripHeaderBreaks(to)}>`,
    ...(replyTo ? [`Reply-To: <${stripHeaderBreaks(replyTo)}>`] : []),
    `Subject: ${encodeHeaderValue(subject)}`,
    `Date: ${formatDate(date)}`,
    `Message-ID: ${id}`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=utf-8",
    "Content-Transfer-Encoding: quoted-printable",
  ];

  return headers.join(CRLF) + CRLF + CRLF + encodeQuotedPrintable(text) + CRLF;
}
