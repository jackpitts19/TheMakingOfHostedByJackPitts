#!/usr/bin/env python3
"""
Single source of truth for the site's public URLs.

WHY THIS FILE EXISTS
--------------------
Cloudflare Pages serves this site's `.html` files at *extensionless* paths and
307-redirects the `.html` form. Verified against production:

    /articles.html                 -> 307 -> /articles
    /episodes/adam-stevenson.html  -> 307 -> /episodes/adam-stevenson
    /index.html                    -> 307 -> /

So any URL we emit with a `.html` suffix is a redirect, not a page. Google
Search Console reports those as "Page with redirect" and does not index them.
Every URL the site publishes -- sitemap entries, canonical tags, Open Graph
URLs, JSON-LD, and internal links -- must therefore use the extensionless form.

Every generator imports from here so the sitemap, the pages, and the internal
links cannot drift apart. Add a public page in one place: `STATIC_PATHS`.
"""

from __future__ import annotations

import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent
EPISODES_DIR = ROOT / "episodes"
ARTICLES_DIR = ROOT / "articles"

BASE_URL = "https://themakingofhostedbyjackpitts.com"

# Public, canonical, indexable pages that are not generated from episode or
# article data. Each entry is a site-root-relative path whose source file is
# resolved by `source_file_for()`.
#   "/"            -> index.html       (homepage)
#   "/episodes"    -> episodes.html    (episode archive)
#   "/articles"    -> articles.html    (article archive)
#   "/about"       -> about.html       (the host)
#   "/press"       -> press.html       (press coverage and press kit)
#   "/be-a-guest"  -> be-a-guest.html  (how to come on the show, by email)
#   "/privacy"     -> privacy.html     (privacy policy)
#   "/terms"       -> terms.html       (terms and disclaimer)
STATIC_PATHS: tuple[str, ...] = (
    "/", "/episodes", "/articles", "/about", "/press", "/be-a-guest", "/privacy", "/terms",
)

# The homepage keeps one in-page anchor that other pages link to: the listen
# strip (/#listen). Fragments are not distinct URLs to a crawler, so it is
# covered by "/". Press, press kit, about and guests used to be homepage
# sections; they are now their own pages above.
HOMEPAGE_SECTIONS: tuple[str, ...] = ("listen",)


def slugify(name: str) -> str:
    """Lowercase, non-alphanumeric-to-hyphen slug. Matches existing filenames."""
    s = re.sub(r"[^a-z0-9]+", "-", str(name or "").lower())
    s = re.sub(r"^-+|-+$", "", s)
    return s or "episode"


def _strip_quotes(text: str) -> str:
    return re.sub(r"^[\"“”'\s]+|[\"“”'\s]+$", "", text)


def extract_guest_name(title: str) -> str:
    """Best-effort guest name from an episode title.

    Handles every title format the show has published:
      "Topic | Name"                 -> Name (text after the LAST pipe)
      "From X to Y: Name"            -> Name (topic-first titles)
      "In The Making Of: Name"       -> Name
      "The Making Of Name: Topic"    -> Name
      "Name of Company: Topic"       -> Name
    Falls back to the whole title when nothing matches.
    """
    original = title or ""
    t = original.strip()
    if "|" in t:
        return _strip_quotes(t.rsplit("|", 1)[1]) or original
    if re.match(r"^From\s", t, flags=re.I):
        parts = re.split(r":|\s+with\s+", t, flags=re.I)
        return _strip_quotes(parts[-1]) if len(parts) > 1 else original
    t = re.sub(r"^In\s+The\s+Making\s+Of:\s*", "", t, flags=re.I)
    t = re.sub(r"^The\s+Making\s+(Of|of)\s+", "", t, flags=re.I)
    t = re.split(r":|\s+with\s+|\s+from\s+", t, maxsplit=1, flags=re.I)[0]
    t = re.split(r"\s+of\s+", t, maxsplit=1)[0]
    t = _strip_quotes(t)
    return t or original


def episode_slug(ep: dict) -> str:
    """Slug for an episode. Shared by the page, share card, and sitemap.

    A pinned `slug` in episodes.js always wins, so correcting a guest name
    never moves a live URL or share-card path. Entries without one fall back
    to the slugified guest name.
    """
    pinned = str(ep.get("slug") or "").strip()
    if pinned:
        return pinned
    return slugify(ep.get("guest") or extract_guest_name(ep.get("title", "")))


def episode_path(ep: dict) -> str:
    return f"/episodes/{episode_slug(ep)}"


def article_paths() -> list[str]:
    """Every article page on disk, discovered rather than hard-coded."""
    if not ARTICLES_DIR.is_dir():
        return []
    return sorted(
        f"/articles/{p.stem}"
        for p in ARTICLES_DIR.glob("*.html")
        if p.stem != "index"
    )


def article_pages() -> list[tuple[str, str]]:
    """Every article as (path, title), title read from the file's own <h1>.

    Read from disk rather than listed here so a new articles/*.html file shows
    up in episode pages' related-reading strip with no code change. The visible
    H1 is used, not the <title>, so link text matches the headline readers see
    on the article and the homepage (the <title> can be a shorter SEO variant).
    Falls back to the <title> when an article has no H1.
    """
    pages: list[tuple[str, str]] = []
    for path in article_paths():
        html = source_file_for(path).read_text(encoding="utf-8")
        title = _article_heading(html)
        if title:
            pages.append((path, title))
    return pages


def _article_heading(html: str) -> str:
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S | re.I)
    if h1:
        text = re.sub(r"<[^>]+>", "", h1.group(1))
    else:
        match = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        if not match:
            return ""
        # Titles are "<article title> | <site name>"; keep the article half.
        text = match.group(1).split("|")[0]
    # Unescape so callers get plain text and escape once for their own
    # context. Returning the raw tag content would double-encode any title
    # containing an entity, e.g. "&amp;" rendering as "&amp;amp;".
    return unescape(re.sub(r"\s+", " ", text).strip())


def article_lastmod(path: str) -> str | None:
    """An article's dateModified, read from its own JSON-LD.

    Lets the sitemap carry a real <lastmod> for articles instead of leaving
    them undated, without keeping a second copy of the date anywhere.
    """
    file = source_file_for(path)
    if not file.is_file():
        return None
    match = re.search(
        r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', file.read_text(encoding="utf-8")
    )
    return match.group(1) if match else None


def to_url(path: str) -> str:
    """Site-root-relative path -> absolute canonical URL."""
    if not path.startswith("/"):
        raise ValueError(f"path must start with '/': {path!r}")
    return BASE_URL + path


def source_file_for(path: str) -> Path:
    """The repo file Cloudflare Pages serves for a given public path."""
    if path == "/":
        return ROOT / "index.html"
    return ROOT / (path.lstrip("/") + ".html")


def public_paths(episodes: list[dict]) -> list[str]:
    """Every public, canonical, indexable path, in sitemap order.

    Order: homepage, archives, articles, then episodes newest-first (the order
    they appear in episodes.js).
    """
    paths = list(STATIC_PATHS)
    paths.extend(article_paths())
    paths.extend(episode_path(ep) for ep in episodes)

    seen: set[str] = set()
    unique: list[str] = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique
