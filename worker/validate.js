// Normalization and validation for guest-request submissions.
// Pure functions only, so they are easy to test under node --test.

export const LIMITS = Object.freeze({
  nameMax: 100,
  emailMax: 254,
  companyRoleMax: 150,
  linkMax: 300,
  storyMin: 20,
  storyMax: 1500,
});

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/** Turn any input into a string; non-strings (objects, numbers, null) become "". */
function asString(value) {
  return typeof value === "string" ? value : "";
}

function charLength(value) {
  return [...value].length;
}

/** Single-line field: strip control chars, collapse all whitespace, trim. */
export function normalizeLine(value) {
  return asString(value)
    .replace(/[\u0000-\u001f\u007f-\u009f]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

/** Multi-line field: keep line breaks, strip other control chars, tidy spacing. */
export function normalizeMultiline(value) {
  return asString(value)
    .replace(/\r\n?/g, "\n")
    .replace(/[\u0000-\u0009\u000b-\u001f\u007f-\u009f]+/g, " ")
    .replace(/[^\S\n]+/g, " ")
    .replace(/ *\n */g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/**
 * Accept full http(s) URLs plus bare domains like "linkedin.com/in/jane" by
 * prefixing https://. Returns the normalized URL string, "" when empty
 * (the link is optional), or null if invalid.
 */
export function normalizeLink(value) {
  if (!value) return "";
  const withScheme = /^[a-z][a-z0-9+.-]*:/i.test(value) ? value : `https://${value}`;
  try {
    const url = new URL(withScheme);
    const isHttp = url.protocol === "http:" || url.protocol === "https:";
    if (!isHttp || !url.hostname.includes(".") || url.username || url.password) {
      return null;
    }
    return url.toString();
  } catch {
    return null;
  }
}

function fail(field, error) {
  return { ok: false, field, error };
}

/**
 * Validate a parsed JSON body.
 * @param {Record<string, unknown>} body
 * @returns {{ok:true, value:{name:string,email:string,companyRole:string,link:string,story:string}}
 *   | {ok:false, field:string, error:string}}
 */
export function validateGuestRequest(body) {
  const name = normalizeLine(body.name);
  const email = normalizeLine(body.email).replace(/\s/g, "");
  const companyRole = normalizeLine(body.companyRole);
  const rawLink = normalizeLine(body.link);
  const story = normalizeMultiline(body.story);

  if (!name) return fail("name", "Please add your name.");
  if (charLength(name) > LIMITS.nameMax) {
    return fail("name", "Please keep your name under 100 characters.");
  }

  if (email.length > LIMITS.emailMax || !EMAIL_PATTERN.test(email)) {
    return fail("email", "Please enter a valid email address so I can reply.");
  }

  if (!companyRole) return fail("companyRole", "Please add your company and role.");
  if (charLength(companyRole) > LIMITS.companyRoleMax) {
    return fail("companyRole", "Please keep your company and role under 150 characters.");
  }

  const link = normalizeLink(rawLink);
  if (link === null || charLength(rawLink) > LIMITS.linkMax || charLength(link) > LIMITS.linkMax) {
    return fail(
      "link",
      "Please enter a valid link, like your LinkedIn profile or company website."
    );
  }

  const storyLength = charLength(story);
  if (storyLength < LIMITS.storyMin) {
    return fail("story", "Please tell me a little more about your story (at least 20 characters).");
  }
  if (storyLength > LIMITS.storyMax) {
    return fail("story", "Please keep your story under 1,500 characters.");
  }

  return { ok: true, value: { name, email, companyRole, link, story } };
}
