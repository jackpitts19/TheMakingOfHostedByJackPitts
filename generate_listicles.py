#!/usr/bin/env python3
"""
Write the podcast listicles into articles/.

Content lives in listicles/*.py; rendering in listicle_render.py. Each
listicle links to the other listicles and to the hand-written guides, so
they reinforce each other in search.

Run after editing any listicle, then run generate_sitemap.py and
validate_seo.py (the sitemap picks the pages up from articles/ by itself).
Output is deterministic, so re-running without changes leaves git clean.
"""

from __future__ import annotations

import sys

from listicle_render import article_path, render
from listicles import ALL
from seo_urls import ARTICLES_DIR

# Hand-written guides every listicle points readers to after the list.
GUIDES = (
    ("/articles/best-entrepreneurship-podcasts-for-founders-2026",
     "How to Choose an Entrepreneurship Podcast: What Founders Should Look For"),
    ("/articles/how-to-choose-the-right-podcast-to-tell-your-founder-story",
     "How to Choose the Right Podcast to Tell Your Founder Story"),
)


def related_for(slug: str) -> list[tuple[str, str]]:
    others = [(article_path(d["slug"]), d["headline"]) for d in ALL if d["slug"] != slug]
    return [*others, *GUIDES, ("/articles", "All articles")]


def main() -> int:
    slugs = [d["slug"] for d in ALL]
    if len(set(slugs)) != len(slugs):
        print(f"duplicate listicle slugs: {slugs}", file=sys.stderr)
        return 1
    for data in ALL:
        out = ARTICLES_DIR / f"{data['slug']}.html"
        out.write_text(render(data, related_for(data["slug"])), encoding="utf-8")
        print(f"wrote {out.relative_to(ARTICLES_DIR.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
