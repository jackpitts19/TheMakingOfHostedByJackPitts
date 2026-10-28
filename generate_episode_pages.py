#!/usr/bin/env python3
"""
Generate one polished page per episode of The Making Of Hosted By Jack Pitts.

Reads episodes.js, writes ./episodes/<slug>.html for each entry. Each page is
self-contained editorial HTML: oversized serif headline, Spotify embed, lede,
guest LinkedIn CTA (when known), share-card hero image, and a "More from the
show" related-episodes strip at the bottom.

Pages share the slug system used by generate_share_cards.py so the OG image
URL (../share-cards/<slug>.png) always matches.
"""

import json
import re
from html import escape
from urllib.parse import quote

from seo_urls import BASE_URL as SITE_URL
from seo_urls import ROOT, article_pages, episode_path, episode_slug, to_url
from seo_titles import GUEST_LINES, SEO_TITLES
from sync_latest_episode import truncate_at_word

from episode_page_template import CSS, PAGE_TMPL  # noqa: F401  (CSS is re-exported for the archive)

EPISODES_JS = ROOT / "episodes.js"
OUT_DIR = ROOT / "episodes"
OUT_DIR.mkdir(exist_ok=True)

SITE = "The Making Of Hosted By Jack Pitts"
# Longest episode title that can still take the " | <show name>" suffix and
# leave the <title> tag inside Google's ~60-character display budget.
SUFFIX_BUDGET_CHARS = 24
SHOW_SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
SHOW_APPLE = "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
APPLE_PODCAST_ID = "1853933144"
SHOW_YT = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
JACK_LI = "https://www.linkedin.com/in/jack-pitts"
JACK_SITE = "https://thejackpitts.com/"  # the person's canonical page; LinkedIn is a sameAs
# Every guest CTA goes to the request form on the homepage, same tab.
GUEST_REQUEST = "/#guest-request"
META_DESC_LIMIT = 160
# A sentence end earlier than this makes a stub description (Google shows
# ~155 chars), so cut at a word boundary instead.
META_DESC_SENTENCE_FLOOR = 110
FALLBACK_DESCRIPTION = "Jack talks with a business owner about how they got started and how they grew."

# Feed descriptions open with show boilerplate ("In this episode of The Making
# Of, Hosted by Jack Pitts, I sit down with ..."). It eats half the snippet
# before the guest's company appears, so meta descriptions drop the show-name
# clause and keep the rest as a full sentence, with "I" named as Jack Pitts.
BOILERPLATE_LEAD_RE = re.compile(
    r"^(?:in|on)\s+this\s+(?:episode|conversation)"
    r"(?:\s+of\s+the\s+making\s+of(?:\s*,?\s*hosted\s+by\s+jack\s+pitts)?)?\s*,\s*",
    re.I,
)
FIRST_PERSON_LEAD_RE = re.compile(r"^I\s+(sit|sat)\s+down\s+with", re.I)
# Words that mark a guest string as a company or a title rather than a person,
# so it is not emitted as a schema.org Person.
NON_PERSON_WORDS = {"ai", "inc", "llc", "co", "group", "holdings", "company", "of", "the"}
PERSON_NAME_RE = re.compile(r"^[A-Z][\w'’.-]+(?: [A-Z][\w'’.-]+){1,2}$")


def load_episodes():
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise RuntimeError("Could not parse episodes.js")
    return json.loads(m.group(1))


def page_title(episode_title):
    """The <title> tag for an episode page.

    Google truncates around 60 characters, and the " | <show name>" suffix is
    36 of them. Appending it unconditionally pushed all sixteen pages past 60
    (up to 117) and repeated the brand twice whenever the episode title already
    opened with "The Making Of ...".

    So the suffix is added only when it earns its place: the title does not
    already carry the show name, and it is short enough that the result still
    fits. The show name is never abbreviated, per house style. Titles that run
    long on their own are left alone rather than rewritten, since they are the
    episode titles as published.
    """
    title = episode_title or ""
    if re.match(r"^(In\s+)?The\s+Making\s+Of\b", title, re.I):
        return title
    if len(title) > SUFFIX_BUDGET_CHARS:
        return title
    return f"{title} | {SITE}"


def split_title(title):
    """Pull the strong half ('The Making Of Alex Dixon') from the subtitle."""
    if ":" in title:
        head, sub = title.split(":", 1)
        return head.strip(), sub.strip()
    return title.strip(), ""


def seo_title_for(ep):
    """Search title: episodes.js seoTitle, else seo_titles.py, else the published title."""
    return (ep.get("seoTitle") or "").strip() or SEO_TITLES.get(episode_slug(ep)) or ep.get("title", "")


def fit_description(text, limit=META_DESC_LIMIT, floor=META_DESC_SENTENCE_FLOOR):
    """Trim to at most `limit` chars: a full sentence if one ends late enough,
    otherwise the last whole word plus an ellipsis."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sentence_ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", cut)]
    if sentence_ends and sentence_ends[-1] >= floor:
        return cut[: sentence_ends[-1]]
    cut = cut[: limit - 1]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,;:.-") + "…"


def meta_description_for(ep):
    """Meta description that opens with the episode, not the show boilerplate."""
    override = (ep.get("metaDescription") or "").strip()
    if override:
        return fit_description(override)
    text = (ep.get("description") or "").strip()
    stripped = BOILERPLATE_LEAD_RE.sub("", text)
    if stripped and stripped != text:
        text = stripped[0].upper() + stripped[1:]
    # Out of context, a search snippet's "I" is nobody, so name the host.
    text = FIRST_PERSON_LEAD_RE.sub(
        lambda m: "Jack Pitts sat down with" if m.group(1).lower() == "sat" else "Jack Pitts sits down with",
        text,
    )
    return fit_description(text or FALLBACK_DESCRIPTION)


def guest_people(ep):
    """Guest names that look like people, for schema.org Person entities.

    "Rick Franco & Mike Trott" gives two people; "Concentrate AI" gives none.
    A guest string that is really the episode title gives none either.
    """
    guest = (ep.get("guest") or "").strip()
    if not guest or guest == (ep.get("title") or "").strip() or "|" in guest:
        return []
    parts = [p.strip() for p in re.split(r"\s+(?:&|and)\s+", guest) if p.strip()]
    people = []
    for part in parts:
        words = {w.lower() for w in part.split()}
        if PERSON_NAME_RE.match(part) and not (words & NON_PERSON_WORDS):
            people.append(part)
    return people


def iso_duration(label):
    """'1h 9m' -> 'PT1H9M', '39 min' -> 'PT39M'. None when not parseable."""
    m = re.fullmatch(r"\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*m(?:in)?)?\s*", label or "", re.I)
    if not m or not (m.group(1) or m.group(2)):
        return None
    hours = f"{int(m.group(1))}H" if m.group(1) else ""
    minutes = f"{int(m.group(2))}M" if m.group(2) else ""
    return f"PT{hours}{minutes}"


def nowrap_hyphenated(html_text):
    """Keep hyphenated words ("140-Person") on one line in big headlines.

    Runs on already-escaped text that may contain <em> tags; neither tags nor
    entities contain hyphens, so only words are wrapped.
    """
    return re.sub(r"\w+(?:-\w+)+", lambda m: f'<span class="nb">{m.group(0)}</span>', html_text)


def spotify_embed_src(spotify_url):
    if not spotify_url:
        return None
    m = re.search(r"episode/([A-Za-z0-9]+)", spotify_url)
    if m:
        return f"https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&theme=0"
    m = re.search(r"show/([A-Za-z0-9]+)", spotify_url)
    if m:
        return f"https://open.spotify.com/embed/show/{m.group(1)}?utm_source=generator&theme=0"
    return None


def issue_label(n):
    return f"No. {n:02d}"


def build_player(ep):
    """The embed for this episode and the accessible name of its wrapper."""
    spotify_url = (ep.get("links") or {}).get("spotify") or SHOW_SPOTIFY
    embed = spotify_embed_src(spotify_url)

    # Prefer a player that plays THIS episode. A Spotify *episode* URL wins;
    # otherwise Apple's per-episode player (resolved by resolve_episode_links.py).
    # The show-level Spotify player surfaces the latest episode, not this one,
    # so it is only a last resort.
    is_episode_embed = bool(embed and "/embed/episode/" in embed)
    apple_id = str(ep.get("appleEpisodeId") or "").strip()
    if not is_episode_embed and apple_id:
        return "Apple Podcasts player", (
            f'<iframe title="Play this episode on Apple Podcasts" '
            f'src="https://embed.podcasts.apple.com/us/podcast/id{APPLE_PODCAST_ID}?i={apple_id}&amp;theme=auto" '
            f'height="175" frameBorder="0" '
            f'allow="autoplay *; encrypted-media *; clipboard-write" '
            f'sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation" '
            f'loading="lazy"></iframe>'
        )

    if not embed:
        return "Episode player", ""
    return "Spotify player", (
        f'<iframe title="Play this episode on Spotify" src="{embed}" '
        f'height="232" frameBorder="0" allowfullscreen="" '
        f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" '
        f'loading="lazy"></iframe>'
    )


def guest_line_for(ep, issue_no):
    """One line for the guest card: a factual line from seo_titles.GUEST_LINES,
    else a short neutral line. Never generated from a template of claims."""
    line = (ep.get("guestLine") or "").strip() or GUEST_LINES.get(episode_slug(ep))
    if line:
        return line
    return f"Jack's guest on Issue {issue_label(issue_no)}. Listen to the full conversation using the links above."


def build_guest_block(ep, issue_no):
    name = (ep.get("guest") or "").strip()
    li = (ep.get("guestLinkedIn") or "").strip()
    if not name:
        return ""
    cta = ""
    if li:
        cta = (
            f'<a class="gc-cta" href="{escape(li)}" target="_blank" rel="noopener">'
            '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM0 8h5v16H0V8zm7.5 0H12v2.2h.07c.63-1.18 2.17-2.43 4.47-2.43C21.4 7.77 24 10.1 24 14.73V24h-5v-8.2c0-1.96-.04-4.48-2.73-4.48-2.74 0-3.16 2.13-3.16 4.34V24h-5V8z"/></svg>'
            f'Connect with {escape(name)} on LinkedIn'
            "</a>"
        )
    else:
        cta = ""
    pitch = escape(guest_line_for(ep, issue_no))
    return (
        '<div class="guest-card">'
        '<div class="gc-eyebrow">About the guest</div>'
        f'<h2>{escape(name)}</h2>'
        f'<p>{pitch}</p>'
        f'{cta}'
        '</div>'
    )


def build_share_row(canonical, social_title, guest_label):
    """Plain share links plus a copy-link button. No third-party scripts."""
    url = quote(canonical, safe="")
    text = quote(social_title, safe="")
    subject = quote(f"Worth a listen: {social_title}", safe="")
    body = quote(f"Thought you'd like this episode of {SITE} with {guest_label}:\n\n{canonical}", safe="")
    return (
        '<div class="share-row" role="group" aria-label="Share this episode">\n'
        '    <span class="share-label">Share</span>\n'
        f'    <a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener">LinkedIn</a>\n'
        f'    <a href="https://twitter.com/intent/tweet?url={url}&amp;text={text}" target="_blank" rel="noopener">X</a>\n'
        f'    <a href="mailto:?subject={subject}&amp;body={body}">Email</a>\n'
        f'    <button type="button" data-copy-link="{escape(canonical)}" hidden>Copy link</button>\n'
        '    <span class="share-status" data-copy-status aria-live="polite"></span>\n'
        '  </div>'
    )


# Shown only when JS runs (the button starts hidden). Uses the async clipboard
# API, falls back to a prompt the reader can copy from.
SHARE_SCRIPT = """<script>
(function () {
  var btn = document.querySelector("[data-copy-link]");
  var status = document.querySelector("[data-copy-status]");
  if (!btn) return;
  btn.hidden = false;
  function say(msg) {
    if (!status) return;
    status.textContent = msg;
    setTimeout(function () { status.textContent = ""; }, 2500);
  }
  btn.addEventListener("click", function () {
    var link = btn.getAttribute("data-copy-link");
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(link).then(
        function () { say("Link copied"); },
        function () { window.prompt("Copy this link:", link); }
      );
    } else {
      window.prompt("Copy this link:", link);
    }
  });
})();
</script>"""


def build_related_cards(all_eps, current_idx, total):
    out = []
    pool = []
    # Show 3 nearest by index, skipping current.
    for offset in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
        i = current_idx + offset
        if 0 <= i < len(all_eps) and i != current_idx:
            pool.append((i, all_eps[i]))
        if len(pool) >= 3:
            break
    for i, ep in pool:
        ep_issue = total - i
        title = escape(ep.get("title", "") or "")
        dur = escape(ep.get("duration", "") or "")
        out.append(
            f'<a class="r-card" href="{episode_path(ep)}">'
            f'<div class="r-issue">ISSUE {issue_label(ep_issue)}</div>'
            f'<div class="r-title">{title}</div>'
            f'<div class="r-dur">{dur}</div>'
            '</a>'
        )
    return "\n".join(out) or '<p style="color: var(--ink-soft);">More episodes coming soon.</p>'


def build_related_reading(idx):
    """Links from an episode page to the guides, plus the article archive.

    Articles are read from disk, so a new articles/*.html file appears here on
    the next regeneration with no code change. The three shown rotate by
    episode index rather than being identical on all sixteen pages, which
    spreads internal links across the whole article set.
    """
    pages = article_pages()
    if not pages:
        return '<a href="/articles">Read the guides for founders <span class="read-arrow" aria-hidden="true">&rarr;</span></a>'

    picks = [pages[(idx + offset) % len(pages)] for offset in range(min(3, len(pages)))]
    out = [
        f'<a href="{path}">{escape(title)} '
        f'<span class="read-arrow" aria-hidden="true">&rarr;</span></a>'
        for path, title in picks
    ]
    out.append(
        '<a href="/articles">All articles for founders '
        '<span class="read-arrow" aria-hidden="true">&rarr;</span></a>'
    )
    return "\n      ".join(out)


def json_ld_script(payload):
    """Serialise JSON-LD safely for embedding in a <script> block.

    json.dumps does not escape `<`, so a title containing `</script` would end
    the script element early: the rest of the JSON becomes live HTML and Google
    drops every entity on the page. Escaping the three HTML-significant
    characters as \\u sequences keeps the JSON valid and inert.
    """
    return (
        json.dumps(payload)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def json_ld_for(ep, issue_no, slug):
    canonical = to_url(episode_path(ep))
    links = ep.get("links") or {}
    # Word-safe, not a raw slice: a hard [:500] cut 15 of 16 pages mid-word, so
    # the structured data contradicted the full text rendered on the same page.
    description = truncate_at_word(ep.get("description") or "", 500)
    host = {"@type": "Person", "name": "Jack Pitts", "url": JACK_SITE, "sameAs": [JACK_LI]}
    obj = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "@id": canonical,
        "name": ep.get("title", ""),
        "description": description,
        "url": canonical,
        "image": f"{SITE_URL}/share-cards/{slug}.png",
        "partOfSeries": {
            "@type": "PodcastSeries",
            "name": SITE,
            "url": to_url("/"),
        },
        "author": host,
    }
    if ep.get("date"):
        obj["datePublished"] = ep["date"]

    # Only per-episode platform pages are "the same thing" as this page. Most
    # episodes carry the show-level Spotify/YouTube URL, which is not.
    same_as = []
    apple = links.get("apple") or ""
    if "?i=" in apple or "&i=" in apple:
        same_as.append(apple)
    spotify = links.get("spotify") or ""
    if "/episode/" in spotify:
        same_as.append(spotify)
    if same_as:
        obj["sameAs"] = same_as

    # The audio itself: duration from the data, and the per-episode embed.
    # No contentUrl, because none of the links on file is an audio file.
    duration = iso_duration(ep.get("duration", ""))
    apple_id = str(ep.get("appleEpisodeId") or "").strip()
    embed = None
    if "/episode/" in spotify:
        embed = spotify_embed_src(spotify)
    elif apple_id:
        embed = f"https://embed.podcasts.apple.com/us/podcast/id{APPLE_PODCAST_ID}?i={apple_id}"
    if duration or embed:
        media = {"@type": "AudioObject"}
        if duration:
            media["duration"] = duration
        if embed:
            media["embedUrl"] = embed
        obj["associatedMedia"] = media
    if duration:
        obj["timeRequired"] = duration

    people = guest_people(ep)
    if people:
        obj["actor"] = [{"@type": "Person", "name": n} for n in people]

    crumb_name = " & ".join(people) if people else ep.get("title", "")
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE, "item": to_url("/")},
            {"@type": "ListItem", "position": 2, "name": "Episodes", "item": to_url("/episodes")},
            {"@type": "ListItem", "position": 3, "name": crumb_name, "item": canonical},
        ],
    }
    return json_ld_script([obj, breadcrumbs])


def long_description_for(ep):
    """Use the existing short description as a confident standfirst.
    Pages stay clean even when only one sentence is on file."""
    desc = (ep.get("description") or "").strip()
    if not desc:
        return FALLBACK_DESCRIPTION
    return desc


def build_page_html(idx, ep, all_eps, total):
    """The full HTML for one episode page. Pure, so tests can inspect it."""
    slug = episode_slug(ep)
    issue_no = total - idx
    title = ep.get("title", "")
    head, sub = split_title(title)
    guest = ep.get("guest") or ""
    headline_html = escape(head)
    # If it's a "The Making Of NAME" pattern, italicize the name for visual rhythm
    if guest and guest in head and guest != head:
        headline_html = escape(head).replace(escape(guest), f"<em>{escape(guest)}</em>")
    headline_html = nowrap_hyphenated(headline_html)
    subhead_block = f'<p class="hero-sub">{nowrap_hyphenated(escape(sub))}</p>' if sub else ""

    description_long = escape(long_description_for(ep))

    links = ep.get("links") or {}
    canonical = to_url(episode_path(ep))
    social_title = seo_title_for(ep)
    guest_label = guest or title
    player_label, player_html = build_player(ep)

    page = PAGE_TMPL.format(
        page_title=escape(page_title(social_title)),
        social_title=escape(social_title),
        meta_desc=escape(meta_description_for(ep)),
        canonical=canonical,
        share_card_url=f"{SITE_URL}/share-cards/{slug}.png",
        json_ld=json_ld_for(ep, issue_no, slug),
        css=CSS,
        issue=issue_label(issue_no),
        date_label=escape(ep.get("dateLabel", "")),
        duration=escape(ep.get("duration", "")),
        headline_html=headline_html,
        subhead_block=subhead_block,
        player_label=player_label,
        player_html=player_html,
        guest_label=escape(guest_label),
        share_row=build_share_row(canonical, social_title, guest_label),
        share_script=SHARE_SCRIPT,
        spotify=escape(links.get("spotify") or SHOW_SPOTIFY),
        apple=escape(links.get("apple") or SHOW_APPLE),
        youtube=escape(links.get("youtube") or SHOW_YT),
        description_long=description_long,
        guest_block=build_guest_block(ep, issue_no),
        slug=slug,
        # `or` not dict.get(k, default): an empty-string or null link is present
        # as a key, so get()'s default never fires and the page ships href=""
        # or href="None". escape() because links.apple comes from Apple's API,
        # and a quote in a URL would inject an arbitrary attribute.
        related_cards=build_related_cards(all_eps, idx, total),
        related_reading=build_related_reading(idx),
        guest_request=GUEST_REQUEST,
        jack_site=JACK_SITE,
    )
    return page


def render_page(idx, ep, all_eps, total):
    out = OUT_DIR / f"{episode_slug(ep)}.html"
    out.write_text(build_page_html(idx, ep, all_eps, total), encoding="utf-8")
    return out


def main():
    eps = load_episodes()
    total = len(eps)
    print(f"Generating {total} episode pages...")
    for idx, ep in enumerate(eps):
        path = render_page(idx, ep, eps, total)
        print(f"  wrote {path.name}")
    print("Done.")


if __name__ == "__main__":
    main()
