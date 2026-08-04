#!/usr/bin/env python3
"""
Generate episodes.html: the crawlable episode archive served at /episodes.

Before this page existed, /episodes and /episodes/ both returned 404 -- the
episode directory had no parent, so every episode page was an orphan reachable
only from the homepage. This page gives the catalog a real, indexable home,
links to every episode without JavaScript, and gives episode breadcrumbs a
genuine second level to point at.

It is named episodes.html rather than episodes/index.html on purpose: Cloudflare
Pages serves a root-level `foo.html` at `/foo` with HTTP 200, which is the
pattern articles.html already uses successfully. A directory index would depend
on trailing-slash normalisation we have not verified in production.

Reads episodes.js (source of truth). Run after generate_episode_pages.py and
before generate_sitemap.py. Safe to run repeatedly; deterministic output.
"""

from __future__ import annotations

import json
import sys
from html import escape

from generate_episode_pages import CSS, json_ld_script, load_episodes
from seo_urls import BASE_URL, ROOT, episode_path, to_url
from sync_latest_episode import truncate_at_word

OUT_FILE = ROOT / "episodes.html"

SITE = "The Making Of Hosted By Jack Pitts"
BOOK_CAL = "https://calendar.app.google/8s9JEAriAqG2qS7MA"

PAGE_TITLE = "All Episodes | The Making Of Hosted By Jack Pitts"
PAGE_DESC = (
    "Every episode of The Making Of Hosted By Jack Pitts: long-form "
    "entrepreneurship interviews with founders, operators, and family-business "
    "builders on what it actually took."
)

ARCHIVE_CSS = r"""
.archive-intro {
  font-family: 'Fraunces', serif; font-weight: 400;
  font-size: 20px; line-height: 1.6; color: var(--ink-soft);
  max-width: 640px; margin: 0 0 44px;
}
.ep-list { list-style: none; margin: 0; padding: 0; }
.ep-list li { border-top: 1px solid var(--line); }
.ep-list li:last-child { border-bottom: 1px solid var(--line); }
.ep-row {
  display: block; text-decoration: none; color: var(--ink);
  padding: 26px 0; transition: background .15s, padding-left .15s;
}
.ep-row:hover { background: rgba(255,255,255,0.4); padding-left: 12px; }
.ep-row .row-meta {
  font-family: 'Inter', sans-serif; font-size: 11.5px;
  letter-spacing: 0.16em; text-transform: uppercase; font-weight: 700;
  color: var(--ink-soft); margin-bottom: 9px;
  display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
}
.ep-row .row-issue { color: var(--orange-dark); }
.ep-row .row-title {
  font-family: 'Fraunces', serif; font-weight: 700;
  font-size: clamp(21px, 2.6vw, 27px); line-height: 1.24;
  letter-spacing: -0.015em; margin: 0 0 9px;
}
.ep-row .row-desc {
  font-family: 'Fraunces', serif; font-size: 17px; line-height: 1.5;
  color: var(--ink-soft); margin: 0; max-width: 680px;
}
"""

PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#f3e8cf" />
<title>{page_title}</title>
<meta name="description" content="{page_desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{site}" />
<meta property="og:title" content="{page_title}" />
<meta property="og:description" content="{page_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{page_title}" />
<meta name="twitter:description" content="{page_desc}" />
<meta name="twitter:image" content="{og_image}" />
<link rel="icon" type="image/svg+xml" href='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%23f3e8cf"/><text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-weight="900" font-size="42" fill="%23d87a2c">M</text></svg>' />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<script type="application/ld+json">{json_ld}</script>
<style>{css}</style>
</head>
<body>

<nav class="topnav">
  <div class="wrap">
    <a class="mark" href="/">The Making <span>Of</span> Hosted By Jack Pitts</a>
    <a class="back" href="/">Home</a>
  </div>
</nav>

<main class="wrap">
  <div class="masthead">
    <span class="issue">THE ARCHIVE</span>
    <span class="dot"></span>
    <span>{count} EPISODES</span>
    <span class="dot"></span>
    <span>HOSTED BY JACK PITTS</span>
  </div>

  <h1 class="hero-title">Every <em>episode</em>.</h1>
  <p class="archive-intro">Long-form conversations with founders, operators, and
  family-business builders about how the thing actually got made. No highlight
  reels. Newest first.</p>

  <ul class="ep-list">
{rows}
  </ul>

  <aside class="book-strip" aria-label="Be a guest">
    <div>
      <h3>Have a story like this? <em>Come on the show.</em></h3>
      <p>Sixty to seventy-five minutes, remote, no prep deck. Pick a time and we'll figure out the angle together.</p>
    </div>
    <a href="{book_cal}" target="_blank" rel="noopener">Book a guest call</a>
  </aside>
</main>

<footer>
  <div class="wrap">
    <div class="mark">The Making <span>Of</span> Hosted By Jack Pitts</div>
    <small>&copy; 2026 Jack Pitts. Every conversation is a long one. <a href="/articles" style="color: var(--orange); text-decoration: underline;">Read the articles.</a></small>
  </div>
</footer>

</body>
</html>
"""


def pad(n: int) -> str:
    return f"{n:02d}"


def build_row(ep: dict, issue_no: int) -> str:
    path = episode_path(ep)
    meta_bits = [f'<span class="row-issue">Issue No. {pad(issue_no)}</span>']
    if ep.get("dateLabel"):
        meta_bits.append(f'<span>{escape(ep["dateLabel"])}</span>')
    if ep.get("duration"):
        meta_bits.append(f'<span>{escape(ep["duration"])}</span>')
    desc = escape(truncate_at_word(ep.get("description", "")))
    return (
        f'    <li><a class="ep-row" href="{path}">\n'
        f'      <div class="row-meta">{"".join(meta_bits)}</div>\n'
        f'      <h2 class="row-title">{escape(ep.get("title", ""))}</h2>\n'
        f'      <p class="row-desc">{desc}</p>\n'
        f"    </a></li>"
    )


def build_json_ld(episodes: list[dict]) -> str:
    canonical = to_url("/episodes")
    collection = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "All Episodes",
        "description": PAGE_DESC,
        "url": canonical,
        "isPartOf": {"@type": "PodcastSeries", "name": SITE, "url": to_url("/")},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(episodes),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "url": to_url(episode_path(ep)),
                    "name": ep.get("title", ""),
                }
                for i, ep in enumerate(episodes)
            ],
        },
    }
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE, "item": to_url("/")},
            {"@type": "ListItem", "position": 2, "name": "Episodes", "item": canonical},
        ],
    }
    # Same escaping as the episode pages: an unescaped "<" in a title would
    # close the <script> early and take the whole entity with it.
    return json_ld_script([collection, breadcrumbs])


def build_page(episodes: list[dict]) -> str:
    total = len(episodes)
    rows = "\n".join(build_row(ep, total - i) for i, ep in enumerate(episodes))
    newest_slug = episode_path(episodes[0]).rsplit("/", 1)[-1]
    return PAGE_TMPL.format(
        page_title=escape(PAGE_TITLE),
        page_desc=escape(PAGE_DESC),
        canonical=to_url("/episodes"),
        site=escape(SITE),
        og_image=f"{BASE_URL}/share-cards/{newest_slug}.png",
        json_ld=build_json_ld(episodes),
        css=CSS + ARCHIVE_CSS,
        count=total,
        rows=rows,
        book_cal=BOOK_CAL,
    )


def main() -> int:
    episodes = load_episodes()
    if not episodes:
        raise RuntimeError("episodes.js has no episodes")
    OUT_FILE.write_text(build_page(episodes), encoding="utf-8")
    print(f"Wrote episodes.html with {len(episodes)} episodes -> {to_url('/episodes')}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
