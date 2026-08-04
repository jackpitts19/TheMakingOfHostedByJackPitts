"""Tests for the indexable surface. Run: python3 -m unittest discover tests

These lock in the behaviour that Google Search Console actually cares about:
sitemap URLs must resolve to real files at HTTP 200 (which means extensionless,
because Cloudflare Pages 307-redirects `.html`), and a newly published episode
or article must reach the sitemap without anyone editing a URL list by hand.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_sitemap import build_sitemap, load_episodes
from seo_urls import (
    BASE_URL,
    episode_path,
    episode_slug,
    public_paths,
    source_file_for,
    to_url,
)
from validate_seo import run_checks, sitemap_locs

SYNTHETIC_EPISODE = {
    "date": "2099-01-15",
    "dateLabel": "January 15, 2099",
    "title": "The Making Of Jane Doe: Building Something",
    "guest": "Jane Doe",
    "description": "A synthetic episode used only by the test suite.",
    "duration": "58 min",
}


class SeoUrlTests(unittest.TestCase):
    def test_episode_path_is_extensionless_and_slugified(self):
        self.assertEqual(episode_path(SYNTHETIC_EPISODE), "/episodes/jane-doe")

    def test_episode_slug_falls_back_to_title_when_guest_missing(self):
        # Arrange
        ep = {k: v for k, v in SYNTHETIC_EPISODE.items() if k != "guest"}

        # Act
        slug = episode_slug(ep)

        # Assert
        self.assertEqual(slug, "jane-doe")

    def test_to_url_uses_the_canonical_production_domain(self):
        self.assertEqual(to_url("/episodes"), f"{BASE_URL}/episodes")

    def test_public_paths_contains_no_duplicates(self):
        paths = public_paths(load_episodes())
        self.assertEqual(len(paths), len(set(paths)))

    def test_every_public_path_has_a_file_behind_it(self):
        missing = [p for p in public_paths(load_episodes()) if not source_file_for(p).is_file()]
        self.assertEqual(missing, [], f"public paths with no file: {missing}")


class SitemapTests(unittest.TestCase):
    def test_committed_sitemap_lists_every_public_page(self):
        expected = {to_url(p) for p in public_paths(load_episodes())}
        self.assertEqual(set(sitemap_locs()), expected)

    def test_no_sitemap_url_keeps_the_html_suffix(self):
        # `.html` URLs 307-redirect on Cloudflare Pages, so Search Console
        # records them as "Page with redirect" instead of indexing them.
        offenders = [loc for loc in sitemap_locs() if loc.endswith(".html")]
        self.assertEqual(offenders, [])

    def test_every_sitemap_url_is_on_the_canonical_domain(self):
        offenders = [loc for loc in sitemap_locs() if not loc.startswith(BASE_URL + "/")]
        self.assertEqual(offenders, [])

    def test_archive_and_homepage_are_listed(self):
        locs = set(sitemap_locs())
        self.assertIn(f"{BASE_URL}/", locs)
        self.assertIn(f"{BASE_URL}/episodes", locs)
        self.assertIn(f"{BASE_URL}/articles", locs)

    def test_a_newly_published_episode_lands_in_the_sitemap(self):
        # Arrange: episodes.js gains a new entry at the front, as the sync does.
        episodes = [SYNTHETIC_EPISODE] + load_episodes()

        # Act
        xml = build_sitemap(episodes)

        # Assert
        self.assertIn(f"<loc>{BASE_URL}/episodes/jane-doe</loc>", xml)
        self.assertIn("<lastmod>2099-01-15</lastmod>", xml)

    def test_every_article_file_on_disk_is_in_the_sitemap(self):
        articles_dir = Path(__file__).parent.parent / "articles"
        on_disk = {f"{BASE_URL}/articles/{p.stem}" for p in articles_dir.glob("*.html")}
        self.assertTrue(
            on_disk <= set(sitemap_locs()), "an article file is missing from the sitemap"
        )


class IndexabilityTests(unittest.TestCase):
    def test_no_indexing_problems(self):
        problems = run_checks()
        self.assertEqual(problems, [], "\n".join(["", *problems]))


if __name__ == "__main__":
    unittest.main()
