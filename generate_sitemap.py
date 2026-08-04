#!/usr/bin/env python3
"""
Generate sitemap.xml from episodes.js and the articles/ directory.

The sitemap lists every public, canonical, indexable page: the homepage, the
episode archive, the article archive, each article, and one page per episode.
Routes come from seo_urls.public_paths(), which derives episode URLs from
episodes.js (the source of truth) and discovers articles by globbing
articles/*.html -- nothing here is hard-coded, so a new episode or a new
article file lands in the sitemap automatically.

URLs are extensionless because Cloudflare Pages 307-redirects the `.html`
form; see seo_urls.py for the verification. Run after generate_episode_pages.py
and generate_episode_archive.py.

Safe to run repeatedly; output is deterministic for a given episodes.js.
"""

from __future__ import annotations

import json
import re
import sys

from seo_urls import ROOT, episode_path, public_paths, source_file_for, to_url

EPISODES_JS = ROOT / "episodes.js"
SITEMAP_XML = ROOT / "sitemap.xml"


def load_episodes() -> list[dict]:
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;\s*$", text, re.S)
    if not m:
        raise RuntimeError("Could not parse window.EPISODES block in episodes.js")
    return json.loads(m.group(1))


def build_lastmods(episodes: list[dict]) -> dict[str, str]:
    """Map path -> lastmod. Only pages with a real publication date get one.

    The homepage and the episode archive both change whenever a new episode
    lands, so they inherit the newest episode's date.
    """
    newest = episodes[0].get("date") or ""
    lastmods: dict[str, str] = {}
    if newest:
        lastmods["/"] = newest
        lastmods["/episodes"] = newest
    for ep in episodes:
        date = ep.get("date")
        if date:
            lastmods[episode_path(ep)] = date
    return lastmods


def url_entry(loc: str, lastmod: str | None = None) -> str:
    lines = ["  <url>", f"    <loc>{loc}</loc>"]
    if lastmod:
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("  </url>")
    return "\n".join(lines)


def build_sitemap(episodes: list[dict]) -> str:
    paths = public_paths(episodes)
    lastmods = build_lastmods(episodes)
    body = "\n".join(url_entry(to_url(p), lastmods.get(p)) for p in paths)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


def main() -> int:
    episodes = load_episodes()
    if not episodes:
        raise RuntimeError("episodes.js has no episodes")

    paths = public_paths(episodes)

    # A sitemap URL with no file behind it 404s for Googlebot. Fail loudly here
    # rather than shipping a sitemap full of dead links.
    missing = [p for p in paths if not source_file_for(p).is_file()]
    if missing:
        raise RuntimeError(
            "No source file for: " + ", ".join(missing)
            + " (run generate_episode_pages.py and generate_episode_archive.py first)"
        )

    SITEMAP_XML.write_text(build_sitemap(episodes), encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(paths)} URLs.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
