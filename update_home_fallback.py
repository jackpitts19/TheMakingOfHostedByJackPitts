#!/usr/bin/env python3
"""
Regenerate the crawlable (no-JS) fallback content in index.html from episodes.js.

The homepage renders Featured / From the Catalog / Recent Episodes with JS, but
ships real HTML underneath so search engines and AI crawlers that do not run JS
still see the latest episodes. That fallback used to be hand-written and went
stale whenever sync_latest_episode.py added a new episode. This script keeps it
in sync with episodes.js so the fallback always mirrors the newest episodes.

It updates four zones in index.html:
  - Featured: the data-fe-* fields (newest episode).
  - From the Catalog: pins between FALLBACK:CATALOG:START/END markers.
  - Recent Episodes: cards between FALLBACK:RECENT:START/END markers.
  - Footer archive: links to every episode page between
    FALLBACK:ARCHIVE:START/END markers, so search engines can reach the
    whole catalog from the homepage without running JS.

Safe to run repeatedly; output is deterministic for a given episodes.js.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime

from seo_urls import ROOT, episode_path
from sync_latest_episode import truncate_at_word

EPISODES_JS = ROOT / "episodes.js"
INDEX_HTML = ROOT / "index.html"

SHOW_LINKS = {
    "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
    "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
    "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg",
}

# Mirrors the TAG_LABELS map and pickPinned() order in index.html's render layer.
TAG_META = {
    "press": {"corner": "II", "label": "Press Pick, Riverside-Brookfield Landmark"},
    "first": {"corner": "01", "label": "Episode 01, The Origin Story"},
    "pick": {"corner": "", "label": "Editor's Pick"},
}
PIN_ORDER = ["press", "first"]


def esc(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def pad(n: int) -> str:
    return f"0{n}" if n < 10 else str(n)


def page_href(ep: dict) -> str:
    """Root-absolute, extensionless episode link.

    Root-absolute so the same string is correct from any page, and extensionless
    because Cloudflare Pages 307-redirects the `.html` form (see seo_urls.py).
    """
    return episode_path(ep)


def load_episodes() -> list[dict]:
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;\s*$", text, re.S)
    if not m:
        raise RuntimeError("Could not parse window.EPISODES block in episodes.js")
    return json.loads(m.group(1))


def platform_pills(ep: dict, include_connect: bool) -> str:
    links = ep.get("links") or {}
    sp = links.get("spotify") or SHOW_LINKS["spotify"]
    ap = links.get("apple") or SHOW_LINKS["apple"]
    yt = links.get("youtube") or SHOW_LINKS["youtube"]
    rows = [
        f'          <a class="ep-platform is-spotify" href="{sp}" target="_blank" rel="noopener">Spotify</a>',
        f'          <a class="ep-platform is-apple" href="{ap}" target="_blank" rel="noopener">Apple</a>',
        f'          <a class="ep-platform is-youtube" href="{yt}" target="_blank" rel="noopener">YouTube</a>',
    ]
    li = (ep.get("guestLinkedIn") or "").strip()
    if include_connect and li:
        rows.append(
            f'          <a class="ep-platform is-linkedin" href="{li}" target="_blank" rel="noopener">Connect</a>'
        )
    return "\n".join(rows)


def build_catalog(all_eps: list[dict]) -> str:
    by_tag: dict[str, dict] = {}
    for ep in all_eps:
        tag = ep.get("tag")
        if tag and tag not in by_tag:
            by_tag[tag] = ep
    pins = [by_tag[t] for t in PIN_ORDER if t in by_tag]
    articles = []
    for ep in pins:
        meta = TAG_META.get(ep.get("tag"), {"corner": "", "label": "Highlight"})
        href = page_href(ep)
        corner = (
            f'\n        <span class="pin-corner" aria-hidden="true">{meta["corner"]}</span>'
            if meta["corner"]
            else ""
        )
        articles.append(
            f"""      <article class="pin">{corner}
        <div class="pin-tag">{esc(meta["label"])}</div>
        <div class="pin-date">{esc(ep.get("dateLabel", ""))}</div>
        <h3><a class="ep-title-link" href="{href}">{esc(ep.get("title", ""))}</a></h3>
        <p>{esc(truncate_at_word(ep.get("description", "")))}</p>
        <div class="ep-platforms">
{platform_pills(ep, include_connect=True)}
        </div>
        <a class="ep-read" href="{href}">Read the full issue <span aria-hidden="true">&rarr;</span></a>
      </article>"""
        )
    return "\n".join(articles)


def build_recent(all_eps: list[dict], total: int) -> str:
    recent = all_eps[1:4]
    last_idx = len(recent) - 1
    cards = []
    for i, ep in enumerate(recent):
        issue = pad(total - (i + 1))
        span = ' style="grid-column: 1 / -1;"' if (i == last_idx and len(recent) % 2 != 0) else ""
        href = page_href(ep)
        cards.append(
            f"""      <article class="ep fade-up is-in"{span}>
        <span class="ep-numeral" aria-hidden="true">{issue}</span>
        <div class="ep-issue">Issue No. {issue}</div>
        <div class="ep-num">{esc(ep.get("dateLabel", ""))}</div>
        <h3><a class="ep-title-link" href="{href}">{esc(ep.get("title", ""))}</a></h3>
        <p>{esc(truncate_at_word(ep.get("description", "")))}</p>
        <div class="ep-meta"><span>{esc(ep.get("duration", ""))}</span><span>Full episode</span></div>
        <div class="ep-platforms">
{platform_pills(ep, include_connect=True)}
        </div>
        <a class="ep-read" href="{href}">Read the full issue <span aria-hidden="true">&rarr;</span></a>
      </article>"""
        )
    return "\n".join(cards)


def build_archive(all_eps: list[dict]) -> str:
    items = []
    for ep in all_eps:
        href = page_href(ep)
        items.append(f'        <li><a href="{href}">{esc(ep.get("title", ""))}</a></li>')
    return "      <ul>\n" + "\n".join(items) + "\n      </ul>"


def replace_between(html: str, name: str, inner: str) -> str:
    pattern = re.compile(
        r"(<!-- FALLBACK:" + name + r":START[^>]*-->)(.*?)(<!-- FALLBACK:" + name + r":END -->)",
        re.S,
    )
    if not pattern.search(html):
        raise RuntimeError(f"Missing FALLBACK:{name} markers in index.html")
    return pattern.sub(lambda m: m.group(1) + "\n" + inner + "\n      " + m.group(3), html)


def set_text(html: str, open_tag: str, close_tag: str, value: str) -> str:
    pat = re.compile(re.escape(open_tag) + r".*?" + re.escape(close_tag))
    return pat.sub(open_tag + value + close_tag, html, count=1)


def set_attr_href(html: str, marker: str, url: str) -> str:
    pat = re.compile("(" + re.escape(marker) + r'\s+href=")[^"]*(")')
    return pat.sub(lambda m: m.group(1) + url + m.group(2), html, count=1)


def main() -> int:
    episodes = load_episodes()
    if not episodes:
        raise RuntimeError("episodes.js has no episodes")
    total = len(episodes)
    featured = episodes[0]

    html = INDEX_HTML.read_text(encoding="utf-8")

    # Masthead: issue number tracks episode count, month tracks the newest episode.
    html = set_text(html, "<strong data-mast-issue>", "</strong>", f"ISSUE NO. {pad(total)}")
    try:
        mast_month = datetime.strptime(featured.get("date", ""), "%Y-%m-%d").strftime("%B %Y").upper()
        html = set_text(html, "<span data-mast-date>", "</span>", mast_month)
    except ValueError:
        print(f"WARNING: could not parse featured date {featured.get('date')!r}; masthead month left as-is")

    # Featured (newest episode) fields.
    html = set_text(html, "<span data-fe-date>", "</span>", esc(featured.get("dateLabel", "")))
    html = set_text(html, "<span data-fe-duration>", "</span>", esc(featured.get("duration", "")))
    html = set_text(html, '<h2 class="fe-title" data-fe-title>', "</h2>", esc(featured.get("title", "")))
    html = set_text(html, '<p class="fe-desc" data-fe-desc>', "</p>", esc(truncate_at_word(featured.get("description", ""))))
    html = set_text(html, "<span data-fe-issue>", "</span>", pad(total))
    feat_spotify = (featured.get("links") or {}).get("spotify") or SHOW_LINKS["spotify"]
    html = set_attr_href(html, "data-fe-link-spotify", feat_spotify)
    html = set_attr_href(html, "data-fe-read-link", page_href(featured))

    # Catalog + Recent zones.
    html = replace_between(html, "CATALOG", build_catalog(episodes))
    html = replace_between(html, "RECENT", build_recent(episodes, total))
    html = replace_between(html, "ARCHIVE", build_archive(episodes))

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"Updated index.html fallback. Featured: {featured.get('title')} (issue {pad(total)})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
