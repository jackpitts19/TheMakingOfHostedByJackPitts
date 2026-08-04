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
from pathlib import Path

ROOT = Path(__file__).parent
EPISODES_DIR = ROOT / "episodes"
ARTICLES_DIR = ROOT / "articles"

BASE_URL = "https://themakingofhostedbyjackpitts.com"

# Public, canonical, indexable pages that are not generated from episode or
# article data. Each entry is a site-root-relative path whose source file is
# resolved by `source_file_for()`.
#   "/"          -> index.html      (homepage)
#   "/episodes"  -> episodes.html   (episode archive)
#   "/articles"  -> articles.html   (article archive)
STATIC_PATHS: tuple[str, ...] = ("/", "/episodes", "/articles")

# Deliberately NOT separate URLs: the press, press-kit, about, and guest/booking
# sections live on the homepage as #press, #press-kit, #about, and #guests.
# Fragments are not distinct URLs to a crawler -- listing them would just repeat
# the homepage in the sitemap. They are covered by "/".
HOMEPAGE_SECTIONS: tuple[str, ...] = ("press", "press-kit", "about", "guests", "listen")


def slugify(name: str) -> str:
    """Lowercase, non-alphanumeric-to-hyphen slug. Matches existing filenames."""
    s = re.sub(r"[^a-z0-9]+", "-", str(name or "").lower())
    s = re.sub(r"^-+|-+$", "", s)
    return s or "episode"


def extract_guest_name(title: str) -> str:
    """Best-effort guest name from an episode title, for entries with no `guest`."""
    t = title or ""
    t = re.sub(r"^In\s+The\s+Making\s+Of:\s*", "", t, flags=re.I)
    t = re.sub(r"^The\s+Making\s+(Of|of)\s+", "", t, flags=re.I)
    t = re.split(r":|\s+with\s+|\s+from\s+", t, maxsplit=1, flags=re.I)[0]
    t = re.sub(r"^[\"“”'\s]+|[\"“”'\s]+$", "", t)
    return t or (title or "")


def episode_slug(ep: dict) -> str:
    """Slug for an episode. Shared by the page, share card, and sitemap."""
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
