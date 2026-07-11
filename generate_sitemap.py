#!/usr/bin/env python3
"""
Generate sitemap.xml from episodes.js and the articles/ directory.

The sitemap lists every public page on the site: the homepage, the articles
index, each article, and one page per episode. It reads episodes.js (the
source of truth for the episode list) so it stays correct when the daily
episode sync adds a new episode. Run it after generate_episode_pages.py.

Safe to run repeatedly; output is deterministic for a given episodes.js.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"
ARTICLES_DIR = ROOT / "articles"
SITEMAP_XML = ROOT / "sitemap.xml"

BASE_URL = "https://themakingofhostedbyjackpitts.com"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(name or "").lower())
    s = re.sub(r"^-+|-+$", "", s)
    return s or "episode"


def extract_guest_name(title: str) -> str:
    t = title or ""
    t = re.sub(r"^In\s+The\s+Making\s+Of:\s*", "", t, flags=re.I)
    t = re.sub(r"^The\s+Making\s+(Of|of)\s+", "", t, flags=re.I)
    t = re.split(r":|\s+with\s+|\s+from\s+", t, maxsplit=1, flags=re.I)[0]
    t = re.sub(r"^[\"“”'\s]+|[\"“”'\s]+$", "", t)
    return t or (title or "")


def load_episodes() -> list[dict]:
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;\s*$", text, re.S)
    if not m:
        raise RuntimeError("Could not parse window.EPISODES block in episodes.js")
    return json.loads(m.group(1))


def episode_url(ep: dict) -> str:
    guest = ep.get("guest") or extract_guest_name(ep.get("title", ""))
    return f"{BASE_URL}/episodes/{slugify(guest)}.html"


def url_entry(loc: str, lastmod: str | None = None) -> str:
    lines = ["  <url>", f"    <loc>{loc}</loc>"]
    if lastmod:
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("  </url>")
    return "\n".join(lines)


def main() -> int:
    episodes = load_episodes()
    if not episodes:
        raise RuntimeError("episodes.js has no episodes")

    newest_date = episodes[0].get("date") or None

    entries = [
        url_entry(f"{BASE_URL}/", newest_date),
        url_entry(f"{BASE_URL}/articles.html"),
    ]

    for article in sorted(ARTICLES_DIR.glob("*.html")):
        entries.append(url_entry(f"{BASE_URL}/articles/{article.name}"))

    for ep in episodes:
        entries.append(url_entry(episode_url(ep), ep.get("date") or None))

    body = "\n".join(entries)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    SITEMAP_XML.write_text(xml, encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(entries)} URLs.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
