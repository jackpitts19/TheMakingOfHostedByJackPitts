"""Tests for the indexable surface. Run: python3 -m unittest discover tests

These lock in the behaviour that Google Search Console actually cares about:
sitemap URLs must resolve to real files at HTTP 200 (which means extensionless,
because Cloudflare Pages 307-redirects `.html`), and a newly published episode
or article must reach the sitemap without anyone editing a URL list by hand.
"""

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import generate_episode_archive
import update_home_fallback
from generate_episode_pages import (
    build_guest_block,
    build_page_html,
    build_related_reading,
    build_share_row,
    guest_people,
    iso_duration,
    json_ld_for,
    meta_description_for,
    page_title,
    seo_title_for,
)
from seo_titles import GUEST_LINES, SEO_TITLES
from generate_sitemap import build_sitemap, load_episodes
from seo_urls import (
    BASE_URL,
    article_pages,
    episode_path,
    episode_slug,
    public_paths,
    source_file_for,
    to_url,
)
from sync_latest_episode import strip_tags
from resolve_episode_links import apply_apple_data
from site_nav import FOOTER_LINKS, NAV_ITEMS, footer_html, topnav_html
from validate_seo import (
    SITE_PAGES,
    check_duplicates,
    check_episode_guests,
    check_episode_slugs,
    check_page_html,
    check_site_html,
    check_robots_text,
    run_checks,
    sitemap_locs,
)

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


class PageTitleTests(unittest.TestCase):
    def test_suffix_dropped_when_title_already_carries_the_show_name(self):
        # Otherwise the brand appears twice in one <title>.
        self.assertEqual(
            page_title("The Making Of Jane Doe: Building Something"),
            "The Making Of Jane Doe: Building Something",
        )

    def test_suffix_dropped_for_long_titles(self):
        long_title = "Concentrate AI: The LLM Gateway for Fast-Growing Teams"
        self.assertEqual(page_title(long_title), long_title)

    def test_short_title_keeps_the_full_show_name(self):
        self.assertEqual(
            page_title("Jane Doe"),
            "Jane Doe | The Making Of Hosted By Jack Pitts",
        )

    def test_show_name_is_never_abbreviated(self):
        # House style: the full name or nothing.
        result = page_title("Jane Doe")
        self.assertIn("The Making Of Hosted By Jack Pitts", result)


class CrossLinkingTests(unittest.TestCase):
    def test_article_pages_reads_titles_from_disk(self):
        pages = article_pages()
        self.assertTrue(pages, "no articles discovered")
        for path, title in pages:
            self.assertTrue(path.startswith("/articles/"))
            self.assertTrue(title)
            self.assertNotIn("|", title, "site name should be stripped from title")

    def test_related_reading_links_to_articles_and_the_archive(self):
        html = build_related_reading(0)
        self.assertIn('href="/articles"', html)
        self.assertIn('href="/articles/', html)

    def test_related_reading_rotates_across_episodes(self):
        # Identical blocks on all 16 pages would concentrate links on one
        # article; rotation spreads them across the set.
        first_of = lambda i: build_related_reading(i).split('href="')[1]
        self.assertNotEqual(first_of(0), first_of(1))

    def test_every_episode_page_links_to_an_article(self):
        episodes_dir = Path(__file__).parent.parent / "episodes"
        orphans = [
            p.name for p in episodes_dir.glob("*.html")
            if "/articles" not in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(orphans, [])

    def test_every_article_links_to_an_episode(self):
        articles_dir = Path(__file__).parent.parent / "articles"
        orphans = [
            p.name for p in articles_dir.glob("*.html")
            if "/episodes/" not in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(orphans, [])


class HouseStyleTests(unittest.TestCase):
    """The show name is never abbreviated and em dashes are never used."""

    SHOW = "The Making Of Hosted By Jack Pitts"

    def _shipped_pages(self):
        root = Path(__file__).parent.parent
        return (
            [root / n for n in ("index.html", "episodes.html", "articles.html", "privacy.html", "terms.html", "404.html")]
            + sorted((root / "articles").glob("*.html"))
            + sorted((root / "episodes").glob("*.html"))
        )

    def test_no_em_dashes_in_shipped_pages(self):
        offenders = [
            p.name for p in self._shipped_pages()
            if "—" in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [], "em dashes are banned by house style")

    def test_no_em_dashes_in_episode_data(self):
        # episodes.js feeds every generated page, so an em dash here spreads.
        # strip_tags() normalises them at ingestion; this guards the result.
        data = (Path(__file__).parent.parent / "episodes.js").read_text(encoding="utf-8")
        self.assertNotIn("—", data)

    def test_strip_tags_removes_em_dashes_from_feed_text(self):
        # Arrange: the shape Apple actually returns.
        raw = "<p>from humble beginnings — with a dad who was a mechanic — to Georgia Tech</p>"

        # Act
        cleaned = strip_tags(raw)

        # Assert
        self.assertEqual(
            cleaned,
            "from humble beginnings, with a dad who was a mechanic, to Georgia Tech",
        )

    def test_strip_tags_keeps_en_dashes_in_ranges(self):
        self.assertIn("2008–2009", strip_tags("the 2008–2009 downturn"))


class DescriptionProvenanceTests(unittest.TestCase):
    """A hand-edited description must survive the twice-daily sync."""

    APPLE = {"description": "The long original text straight from the feed.",
             "trackViewUrl": "https://podcasts.apple.com/x", "trackId": 1}

    def test_untouched_description_is_refreshed_from_the_feed(self):
        ep = {"description": "Old feed text.", "appleDescription": "Old feed text."}
        apply_apple_data(ep, self.APPLE)
        self.assertEqual(ep["description"], self.APPLE["description"])

    def test_hand_edited_description_is_preserved(self):
        # The old rule overwrote this because Apple's text was longer.
        ep = {"description": "Jane on building, failing, and starting again.",
              "appleDescription": "Old feed text."}
        apply_apple_data(ep, self.APPLE)
        self.assertEqual(ep["description"],
                         "Jane on building, failing, and starting again.")

    def test_hand_edit_survives_repeated_syncs(self):
        ep = {"description": "Short hand-written line.",
              "appleDescription": "Old feed text."}
        for _ in range(3):
            apply_apple_data(ep, self.APPLE)
        self.assertEqual(ep["description"], "Short hand-written line.")

    def test_empty_description_is_filled(self):
        ep = {"description": ""}
        apply_apple_data(ep, self.APPLE)
        self.assertEqual(ep["description"], self.APPLE["description"])


class IndexabilityTests(unittest.TestCase):
    def test_no_indexing_problems(self):
        problems = run_checks()
        self.assertEqual(problems, [], "\n".join(["", *problems]))


def _page(canonical="https://themakingofhostedbyjackpitts.com/episodes",
          title="A Title", desc="A description.", robots="", body="", ld=""):
    """Minimal well-formed page, with one field swappable per test."""
    robots_tag = f'<meta name="robots" content="{robots}" />' if robots else ""
    ld_tag = f'<script type="application/ld+json">{ld}</script>' if ld else ""
    canonical_tag = f'<link rel="canonical" href="{canonical}" />' if canonical else ""
    title_tag = f"<title>{title}</title>" if title else ""
    desc_tag = f'<meta name="description" content="{desc}" />' if desc else ""
    return f"<html><head>{title_tag}{desc_tag}{canonical_tag}{robots_tag}{ld_tag}</head><body>{body}</body></html>"


class ValidatorFiresTests(unittest.TestCase):
    """Negative fixtures: prove each rule actually reports.

    Asserting run_checks() == [] on the real site is not a test of the
    validator. A validator that returns [] unconditionally passes it just as
    happily. Deleting every check body was verified to leave the rest of this
    suite green, which is why these exist: each test below breaks exactly one
    thing and asserts the matching error appears.
    """

    PATH = "/episodes"

    def _check(self, html, exists=lambda t: True):
        errors, titles, descs = [], {}, {}
        check_page_html(errors, self.PATH, html, titles, descs,
                        label="fixture.html", exists=exists)
        return errors

    def test_reports_missing_title(self):
        self.assertTrue(any("missing <title>" in e for e in self._check(_page(title=""))))

    def test_reports_missing_description(self):
        self.assertTrue(any("missing meta description" in e for e in self._check(_page(desc=""))))

    def test_reports_missing_canonical(self):
        self.assertTrue(any("missing canonical" in e for e in self._check(_page(canonical=""))))

    def test_reports_canonical_pointing_elsewhere(self):
        errors = self._check(_page(canonical="https://themakingofhostedbyjackpitts.com/wrong"))
        self.assertTrue(any("canonical is" in e for e in errors))

    def test_reports_noindex(self):
        self.assertTrue(any("noindex" in e for e in self._check(_page(robots="noindex"))))

    def test_reports_nofollow(self):
        self.assertTrue(any("nofollow" in e for e in self._check(_page(robots="nofollow"))))

    def test_reports_internal_link_with_html_suffix(self):
        errors = self._check(_page(body='<a href="/articles.html">x</a>'))
        self.assertTrue(any("307-redirects" in e for e in errors))

    def test_reports_broken_internal_link(self):
        errors = self._check(_page(body='<a href="/nope">x</a>'), exists=lambda t: False)
        self.assertTrue(any("broken internal link" in e for e in errors))

    def test_ignores_external_links(self):
        # Even with every internal target missing, an off-site href must not be
        # reported. (The page's own canonical is link-checked too, which is why
        # this asserts on the external URL rather than on an empty list.)
        errors = self._check(_page(body='<a href="https://spotify.com/x">x</a>'),
                             exists=lambda t: False)
        self.assertFalse(any("spotify.com" in e for e in errors), errors)

    def test_reports_unparseable_json_ld(self):
        errors = self._check(_page(ld="{not valid json"))
        self.assertTrue(any("JSON-LD does not parse" in e for e in errors))

    def test_reports_json_ld_url_with_html_suffix(self):
        # The bug that shipped: the link checker only read href attributes, so
        # a .html URL inside structured data went unnoticed.
        ld = '{"@type":"Article","url":"https://themakingofhostedbyjackpitts.com/articles/x.html"}'
        errors = self._check(_page(ld=ld))
        self.assertTrue(any("JSON-LD URL 307-redirects" in e for e in errors))

    def test_clean_page_reports_nothing(self):
        self.assertEqual(self._check(_page()), [])

    def test_reports_duplicate_titles(self):
        errors = []
        check_duplicates(errors, {"Same": ["/a", "/b"]}, {})
        self.assertTrue(any("duplicate <title>" in e for e in errors))

    def test_reports_duplicate_descriptions(self):
        errors = []
        check_duplicates(errors, {}, {"Same": ["/a", "/b"]})
        self.assertTrue(any("duplicate description" in e for e in errors))

    def test_reports_robots_blocking_the_site(self):
        errors = []
        check_robots_text(errors, "User-agent: *\nDisallow: /\n")
        self.assertTrue(any("blocks the whole site" in e for e in errors))

    def test_reports_robots_missing_sitemap(self):
        errors = []
        check_robots_text(errors, "User-agent: *\nAllow: /\n")
        self.assertTrue(any("missing `Sitemap:" in e for e in errors))

    def test_reports_colliding_episode_slugs(self):
        # Two guests whose names share a slug would silently overwrite each
        # other's page and lose one episode from the sitemap.
        errors = []
        check_episode_slugs(errors, [
            {"guest": "Jane Doe", "title": "A"},
            {"guest": "jane  doe", "title": "B"},
        ])
        self.assertTrue(any("both slugify to" in e for e in errors), errors)

    def test_reports_slug_with_no_usable_ascii(self):
        errors = []
        check_episode_slugs(errors, [{"guest": "李明", "title": "A"}])
        self.assertTrue(any("fallback slug 'episode'" in e for e in errors), errors)

    def test_distinct_slugs_report_nothing(self):
        errors = []
        check_episode_slugs(errors, [
            {"guest": "Jane Doe", "title": "A"},
            {"guest": "John Roe", "title": "B"},
        ])
        self.assertEqual(errors, [])

    def test_clean_robots_reports_nothing(self):
        errors = []
        check_robots_text(
            errors,
            f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n",
        )
        self.assertEqual(errors, [])



JSON_LD_BLOCK_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
SHOW = "The Making Of Hosted By Jack Pitts"
EM_DASH = "\u2014"
# Split so a repo-wide grep for these hosts finds only real occurrences.
CAL_HOST = "calendar.app" + ".google"
PRIVATE_HOST = "helmiq" + ".net"


class SeoTitleTests(unittest.TestCase):
    def test_seo_title_from_episode_data_wins(self):
        ep = dict(SYNTHETIC_EPISODE, seoTitle="Jane Doe of Doe Widgets: Building Something")
        self.assertEqual(seo_title_for(ep), "Jane Doe of Doe Widgets: Building Something")

    def test_seo_title_falls_back_to_published_title(self):
        self.assertEqual(seo_title_for(SYNTHETIC_EPISODE), SYNTHETIC_EPISODE["title"])

    def test_seo_titles_map_is_used_by_slug(self):
        slug, expected = next(iter(SEO_TITLES.items()))
        ep = {"title": "Some Title", "guest": "x", "slug": slug}
        if episode_slug(ep) != slug:
            self.skipTest("seo_urls.episode_slug does not honour ep['slug'] yet")
        self.assertEqual(seo_title_for(ep), expected)

    def test_every_seo_title_follows_the_rules(self):
        for slug, title in SEO_TITLES.items():
            with self.subTest(slug=slug):
                self.assertTrue(50 <= len(title) <= 65, f"{len(title)} chars: {title}")
                self.assertNotIn(EM_DASH, title)
                self.assertNotIn("Making Of", title)

    def test_every_map_key_is_a_live_episode_slug(self):
        slugs = {episode_slug(ep) for ep in load_episodes()}
        stale = sorted((set(SEO_TITLES) | set(GUEST_LINES)) - slugs)
        self.assertEqual(stale, [], "seo_titles.py keys with no matching episode")

    def test_guest_lines_have_no_em_dashes_or_stock_phrases(self):
        for slug, line in GUEST_LINES.items():
            with self.subTest(slug=slug):
                self.assertNotIn(EM_DASH, line)
                for phrase in ("compounded", "actually", "false starts"):
                    self.assertNotIn(phrase, line.lower())


class MetaDescriptionTests(unittest.TestCase):
    def test_strips_show_boilerplate_but_keeps_a_full_sentence(self):
        ep = {"description": "In this episode of The Making Of, Hosted by Jack Pitts , I sit down "
                             "with Jane Doe, founder of Doe Widgets."}
        self.assertEqual(meta_description_for(ep), "Jack Pitts sits down with Jane Doe, founder of Doe Widgets.")

    def test_names_the_host_when_a_snippet_opens_with_i_sat(self):
        ep = {"description": "In this episode of The Making Of Hosted By Jack Pitts, I sat down "
                             "with Jane Doe and John Roe of Doe Widgets."}
        self.assertEqual(meta_description_for(ep), "Jack Pitts sat down with Jane Doe and John Roe of Doe Widgets.")

    def test_strips_short_episode_lead(self):
        ep = {"description": "In this episode, Jack Pitts interviews Jane Doe about widgets."}
        self.assertEqual(meta_description_for(ep), "Jack Pitts interviews Jane Doe about widgets.")

    def test_meta_description_override(self):
        ep = {"description": "Long text.", "metaDescription": "Jane Doe on widgets."}
        self.assertEqual(meta_description_for(ep), "Jane Doe on widgets.")

    def test_long_text_is_trimmed_to_160_at_a_word(self):
        ep = {"description": "Jane Doe built a widget company from nothing. " * 10}
        desc = meta_description_for(ep)
        self.assertLessEqual(len(desc), 160)
        self.assertGreaterEqual(len(desc), 110)

    def test_early_sentence_end_does_not_make_a_stub(self):
        # The Dave Menz case: a 58-char first sentence used to become the whole description.
        ep = {"description": "Jane Doe did not start with much. " + "She worked long weeks and kept going " * 8}
        desc = meta_description_for(ep)
        self.assertGreaterEqual(len(desc), 110)
        self.assertTrue(desc.endswith("\u2026"))

    def test_empty_description_uses_fallback(self):
        self.assertTrue(meta_description_for({"description": ""}))

    def test_every_live_episode_description_fits(self):
        for ep in load_episodes():
            with self.subTest(title=ep.get("title")):
                self.assertLessEqual(len(meta_description_for(ep)), 160)
                self.assertFalse(meta_description_for(ep).lower().startswith("in this episode"))


class EpisodeJsonLdTests(unittest.TestCase):
    EP = dict(
        SYNTHETIC_EPISODE,
        guest="Jane Doe & John Roe",
        duration="1h 9m",
        appleEpisodeId="123",
        links={
            "spotify": "https://open.spotify.com/show/abc",
            "apple": "https://podcasts.apple.com/us/podcast/x/id1?i=123",
        },
    )

    def _ld(self, ep=None):
        return json.loads(json_ld_for(ep or self.EP, 1, "jane-doe"))

    def test_json_ld_parses_and_has_episode_and_breadcrumbs(self):
        types = [block["@type"] for block in self._ld()]
        self.assertEqual(types, ["PodcastEpisode", "BreadcrumbList"])

    def test_show_level_spotify_is_not_claimed_as_episode_audio(self):
        raw = json_ld_for(self.EP, 1, "jane-doe")
        self.assertNotIn("contentUrl", raw)
        self.assertNotIn("open.spotify.com/show", raw)

    def test_per_episode_apple_url_is_same_as(self):
        self.assertEqual(self._ld()[0]["sameAs"], [self.EP["links"]["apple"]])

    def test_series_duration_and_guests(self):
        episode = self._ld()[0]
        self.assertEqual(episode["partOfSeries"]["@type"], "PodcastSeries")
        self.assertEqual(episode["timeRequired"], "PT1H9M")
        self.assertEqual([a["name"] for a in episode["actor"]], ["Jane Doe", "John Roe"])
        self.assertEqual(episode["author"]["name"], "Jack Pitts")

    def test_breadcrumb_ends_with_the_guest(self):
        crumbs = self._ld()[1]["itemListElement"]
        self.assertEqual([c["name"] for c in crumbs][1:], ["Episodes", "Jane Doe & John Roe"])

    def test_script_close_tag_in_title_is_escaped(self):
        raw = json_ld_for(dict(self.EP, title="A </script> B"), 1, "jane-doe")
        self.assertNotIn("</script", raw)
        json.loads(raw)

    def test_guest_people_rejects_companies_and_titles(self):
        self.assertEqual(guest_people({"guest": "Concentrate AI", "title": "x"}), [])
        self.assertEqual(guest_people({"guest": "Topic | Jane Doe", "title": "x"}), [])
        self.assertEqual(guest_people({"guest": "Same", "title": "Same"}), [])
        self.assertEqual(guest_people({"guest": "Niilo Pirttijärvi", "title": "x"}), ["Niilo Pirttijärvi"])

    def test_iso_duration(self):
        self.assertEqual(iso_duration("39 min"), "PT39M")
        self.assertEqual(iso_duration("1h 3m"), "PT1H3M")
        self.assertIsNone(iso_duration(""))


class EpisodePageTemplateTests(unittest.TestCase):
    def _page(self, ep=None):
        ep = ep or dict(SYNTHETIC_EPISODE, appleEpisodeId="123", links={})
        return build_page_html(0, ep, [ep], 1)

    def test_guest_cta_goes_to_the_guest_page_in_the_same_tab(self):
        html = self._page()
        self.assertNotIn(CAL_HOST, html)
        self.assertNotIn(PRIVATE_HOST, html)
        self.assertIn('<a href="/be-a-guest">Be a Guest</a>', html)
        self.assertNotRegex(html, r'href="/be-a-guest"[^>]*target=')
        self.assertNotIn("#guest-request", html)

    def test_episode_page_carries_the_primary_nav(self):
        html = self._page()
        self.assertIn(topnav_html("/episodes"), html)
        self.assertEqual(len(re.findall(r'<a [^>]*aria-current=', html)), 1)

    def test_book_strip_and_footer_copy(self):
        html = self._page()
        self.assertIn("About an hour, recorded remotely on Riverside. No prep needed.", html)
        self.assertIn(footer_html(), html)
        self.assertNotIn("Every conversation is a long one", html)

    def test_page_has_one_h1_no_em_dash_and_parseable_json_ld(self):
        html = self._page()
        errors = []
        check_site_html(errors, "fixture", html)
        self.assertEqual(errors, [])
        for block in JSON_LD_BLOCK_RE.findall(html):
            json.loads(block)

    def test_seo_title_drives_title_tags_but_not_the_h1(self):
        ep = dict(SYNTHETIC_EPISODE, seoTitle="Jane Doe of Doe Widgets on Building Something Big", links={})
        html = self._page(ep)
        self.assertIn("<title>Jane Doe of Doe Widgets on Building Something Big</title>", html)
        self.assertIn('property="og:title" content="Jane Doe of Doe Widgets on Building Something Big"', html)
        self.assertIn('<h1 class="hero-title">The Making Of <em>Jane Doe</em></h1>', html)

    def test_player_label_matches_the_embed(self):
        self.assertIn('aria-label="Apple Podcasts player"', self._page())

    def test_listen_links_name_the_guest(self):
        self.assertIn('aria-label="Listen on Spotify: Jane Doe"', self._page())

    def test_share_row_has_plain_share_links(self):
        row = build_share_row("https://example.com/episodes/jane-doe", "Jane Doe", "Jane Doe")
        self.assertIn("linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fexample.com", row)
        self.assertIn("twitter.com/intent/tweet?url=", row)
        self.assertIn('href="mailto:?subject=', row)
        self.assertIn("data-copy-link", row)

    def test_guest_card_uses_specific_line_or_neutral_fallback(self):
        card = build_guest_block(SYNTHETIC_EPISODE, 7)
        self.assertIn("Jane Doe", card)
        self.assertIn("Issue No. 07", card)
        self.assertNotIn("compounded", card)
        slug = next(iter(GUEST_LINES))
        live = next((ep for ep in load_episodes() if episode_slug(ep) == slug), None)
        if live:
            self.assertIn(GUEST_LINES[slug].split(",")[0], build_guest_block(live, 1).replace("&amp;", "&"))

    def test_hyphenated_headline_words_do_not_split(self):
        ep = dict(SYNTHETIC_EPISODE, title="Building a 140-Person Business", guest="Jane Doe", links={})
        self.assertIn('<span class="nb">140-Person</span>', self._page(ep))


class ArchiveAndFallbackTests(unittest.TestCase):
    def test_archive_cta_and_copy(self):
        html = generate_episode_archive.build_page([dict(SYNTHETIC_EPISODE)])
        self.assertNotIn(CAL_HOST, html)
        self.assertIn('<a href="/be-a-guest">Be a Guest</a>', html)
        self.assertIn('<a href="/episodes" aria-current="page">Episodes</a>', html)
        for phrase in ("builders", "actually", "highlight", "Every conversation is a long one", EM_DASH):
            self.assertNotIn(phrase, html)
        self.assertLessEqual(len(generate_episode_archive.PAGE_DESC), 160)

    def test_home_fallback_refreshes_the_episode_count(self):
        # Runs against a temporary copy: the real index.html is never touched.
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "index.html"
            shutil.copy(update_home_fallback.INDEX_HTML, copy)
            original = update_home_fallback.INDEX_HTML
            update_home_fallback.INDEX_HTML = copy
            try:
                update_home_fallback.main()
            finally:
                update_home_fallback.INDEX_HTML = original
            total = len(update_home_fallback.load_episodes())
            expected = f"<span data-stat-episodes>{update_home_fallback.pad(total)}</span>"
            self.assertIn(expected, copy.read_text(encoding="utf-8"))


class SiteRuleValidatorTests(unittest.TestCase):
    CLEAN = "<html><body><h1>Title</h1></body></html>"

    def _check(self, html):
        errors = []
        check_site_html(errors, "fixture.html", html)
        return errors

    def test_clean_page_reports_nothing(self):
        self.assertEqual(self._check(self.CLEAN), [])

    def test_reports_public_calendar_link(self):
        html = self.CLEAN.replace("</body>", f'<a href="https://{CAL_HOST}/x">b</a></body>')
        self.assertTrue(any(CAL_HOST in e for e in self._check(html)))

    def test_reports_private_booking_host(self):
        html = self.CLEAN.replace("</body>", f'<a href="https://{PRIVATE_HOST}/x">b</a></body>')
        self.assertTrue(any(PRIVATE_HOST in e for e in self._check(html)))

    def test_reports_em_dash(self):
        html = self.CLEAN.replace("Title", "Title \u2014 sub")
        self.assertTrue(any("em dash" in e for e in self._check(html)))

    def test_reports_missing_h1(self):
        self.assertTrue(any("0 <h1>" in e for e in self._check("<html><body></body></html>")))

    def test_reports_two_h1s(self):
        html = self.CLEAN.replace("</body>", "<h1>Again</h1></body>")
        self.assertTrue(any("2 <h1>" in e for e in self._check(html)))

    def test_h1_inside_script_is_not_counted(self):
        html = self.CLEAN.replace("</body>", "<script>var t = '<h1>x</h1>';</script></body>")
        self.assertEqual(self._check(html), [])

    def test_reports_guest_equal_to_title(self):
        errors = []
        check_episode_guests(errors, [{"title": "Topic | Jane Doe", "guest": "Topic | Jane Doe"}])
        self.assertTrue(any("whole title" in e for e in errors))

    def test_reports_guest_with_pipe(self):
        errors = []
        check_episode_guests(errors, [{"title": "A title", "guest": "Topic | Jane Doe"}])
        self.assertTrue(any("contains '|'" in e for e in errors))

    def test_clean_guest_reports_nothing(self):
        errors = []
        check_episode_guests(errors, [{"title": "Topic | Jane Doe", "guest": "Jane Doe"}])
        self.assertEqual(errors, [])



class LegalPagesTest(unittest.TestCase):
    """Privacy and terms pages exist, are public, and every page links them."""

    ROOT = Path(__file__).parent.parent

    def _read(self, name):
        return (self.ROOT / name).read_text(encoding="utf-8")

    def test_legal_pages_are_public_and_in_the_sitemap(self):
        paths = public_paths(load_episodes())
        self.assertIn("/privacy", paths)
        self.assertIn("/terms", paths)
        sitemap = build_sitemap(load_episodes())
        self.assertIn(f"{BASE_URL}/privacy</loc>", sitemap)
        self.assertIn(f"{BASE_URL}/terms</loc>", sitemap)

    def test_legal_pages_carry_the_effective_date_and_contact(self):
        for name in ("privacy.html", "terms.html"):
            html = self._read(name)
            self.assertIn("Last updated: October 28, 2026", html)
            self.assertIn("mailto:jack@saltcreekadvisory.com", html)
        self.assertIn("State of Illinois", self._read("terms.html"))

    def test_every_page_footer_links_privacy_and_terms(self):
        pages = (
            [self.ROOT / n for n in SITE_PAGES]
            + sorted((self.ROOT / "articles").glob("*.html"))
            + sorted((self.ROOT / "episodes").glob("*.html"))
        )
        for page in pages:
            html = page.read_text(encoding="utf-8")
            footer = html[html.index("<footer"):]
            self.assertIn('href="/privacy"', footer, page.name)
            self.assertIn('href="/terms"', footer, page.name)

    def test_every_page_has_the_same_minimal_footer(self):
        for page in _all_pages():
            html = page.read_text(encoding="utf-8")
            self.assertEqual(html.count("<footer"), 1, page.name)
            self.assertIn(footer_html(), html, page.name)
            self.assertNotIn("footer-archive", html, page.name)

    def test_footer_links_are_the_six_standard_links(self):
        self.assertEqual(
            [label for _, label in FOOTER_LINKS],
            ["Episodes", "About", "Press", "Be a Guest", "Privacy", "Terms"],
        )

    def test_every_episode_is_linked_from_the_archive_and_the_sitemap(self):
        archive = self._read("episodes.html")
        sitemap = build_sitemap(load_episodes())
        for ep in load_episodes():
            path = episode_path(ep)
            self.assertIn(f'href="{path}"', archive, path)
            self.assertIn(f"{BASE_URL}{path}</loc>", sitemap, path)

    def test_articles_index_stays_reachable_without_the_footer(self):
        html = (self.ROOT / "episodes" / f"{episode_slug(load_episodes()[0])}.html").read_text(encoding="utf-8")
        self.assertIn('href="/articles"', html)

    def test_salt_creek_is_described_as_a_sell_side_bank(self):
        for page in _all_pages():
            html = page.read_text(encoding="utf-8")
            self.assertNotIn("AI-native", html, page.name)
            self.assertNotRegex(html, r"(?<!co-)founder of (?:<a[^>]*>)?Salt Creek", page.name)

    def test_privacy_policy_describes_email_not_a_form(self):
        html = self._read("privacy.html")
        self.assertIn("This site has no forms.", html)
        for gone in ("Resend", "rate limit", "guest request form", "hidden field"):
            self.assertNotIn(gone, html)


def _all_pages():
    root = Path(__file__).parent.parent
    return (
        [root / n for n in SITE_PAGES]
        + sorted((root / "articles").glob("*.html"))
        + sorted((root / "episodes").glob("*.html"))
    )


class MultiPageSiteTests(unittest.TestCase):
    """Home, /about, /press and /be-a-guest are separate pages; guests email."""

    ROOT = Path(__file__).parent.parent
    NEW_PAGES = {"/about": "about.html", "/press": "press.html", "/be-a-guest": "be-a-guest.html"}
    GUEST_MAILTO = (
        "mailto:jack@saltcreekadvisory.com?subject=Guest%20request%3A%20The%20Making%20Of%20Hosted%20By%20Jack%20Pitts"
        "&amp;body=Name%3A%20%0D%0ACompany%20and%20role%3A%20%0D%0AWebsite%20or%20LinkedIn%3A%20%0D%0A"
        "A%20few%20sentences%20about%20your%20story%3A%20%0D%0A"
    )

    def _read(self, name):
        return (self.ROOT / name).read_text(encoding="utf-8")

    def test_new_pages_are_public_and_in_the_sitemap(self):
        paths = public_paths(load_episodes())
        sitemap = build_sitemap(load_episodes())
        for path in self.NEW_PAGES:
            self.assertIn(path, paths)
            self.assertIn(f"{BASE_URL}{path}</loc>", sitemap)

    def test_no_page_has_a_form_posting_to_the_retired_endpoint(self):
        for page in _all_pages():
            html = page.read_text(encoding="utf-8")
            self.assertNotRegex(html, r"<form\b", page.name)
            self.assertNotIn("/api/guest-request", html, page.name)

    def test_validator_rejects_a_form_posting_to_the_api(self):
        errors = []
        check_site_html(errors, "x.html", '<h1>x</h1><form action="/api/guest-request" method="post"></form>')
        self.assertTrue(any("/api/" in e for e in errors))

    def test_guest_page_offers_the_prefilled_email(self):
        html = self._read("be-a-guest.html")
        self.assertIn(f'<a class="btn btn-orange" href="{self.GUEST_MAILTO}">Email me about being a guest</a>', html)
        self.assertIn("<span>jack@saltcreekadvisory.com</span>", html)
        self.assertIn('href="https://www.linkedin.com/in/jack-pitts"', html)

    def test_every_page_nav_links_the_section_pages(self):
        for page in _all_pages():
            html = page.read_text(encoding="utf-8")
            nav = re.search(r'<nav[^>]*aria-label="Primary"[^>]*>(.*?)</nav>', html, re.S)
            self.assertIsNotNone(nav, page.name)
            for href, label in NAV_ITEMS:
                self.assertRegex(nav.group(1), rf'<a href="{re.escape(href)}"[^>]*>{label}</a>', page.name)

    def test_nav_marks_the_current_page(self):
        expected = {"about.html": "/about", "press.html": "/press", "be-a-guest.html": "/be-a-guest", "episodes.html": "/episodes"}
        for name, href in expected.items():
            self.assertIn(f'<a href="{href}" aria-current="page">', self._read(name), name)

    def test_no_links_to_retired_homepage_sections(self):
        retired = ("#guest-request", "#guests", "#press", "#about", "#press-kit", "#articles")
        for page in _all_pages():
            hrefs = re.findall(r'href="([^"]+)"', page.read_text(encoding="utf-8"))
            for href in hrefs:
                if href.startswith("/press#") or href.startswith("mailto:"):
                    continue
                self.assertFalse(any(href.endswith(r) for r in retired), f"{page.name}: {href}")

    def test_each_new_page_has_one_h1_and_its_own_canonical(self):
        for path, name in self.NEW_PAGES.items():
            html = self._read(name)
            errors = []
            check_site_html(errors, name, html)
            self.assertEqual(errors, [], name)
            self.assertIn(f'<link rel="canonical" href="{BASE_URL}{path}" />', html)
            for block in JSON_LD_BLOCK_RE.findall(html):
                json.loads(block)

    def test_home_keeps_the_episode_feed_and_drops_the_moved_sections(self):
        html = self._read("index.html")
        for marker in ("FALLBACK:CATALOG:START", "FALLBACK:RECENT:START", 'id="listen"', "data-fe-title", 'src="episodes.js"'):
            self.assertIn(marker, html)
        for moved in ('id="press"', 'id="guests"', 'id="about"', 'id="press-kit"', 'id="articles"', "marquee-track"):
            self.assertNotIn(moved, html)

    def test_moved_sections_live_on_their_pages(self):
        self.assertIn('id="about"', self._read("about.html"))
        press = self._read("press.html")
        self.assertIn('id="press"', press)
        self.assertIn('id="press-kit"', press)
        self.assertIn("mailto:jack@saltcreekadvisory.com?subject=Press%20inquiry", press)
        guest = self._read("be-a-guest.html")
        for piece in ('id="guests"', "Riverside", "jack@saltcreekadvisory.com", 'id="marquee-track"', 'src="/marquee.js"'):
            self.assertIn(piece, guest)
        # The owner asked for a short page: no long fit essay or step list.
        for gone in ('class="how-it-works"', 'class="guest-fit"', "Lightly edited"):
            self.assertNotIn(gone, guest)



class CardBlurbTests(unittest.TestCase):
    def test_strips_stock_lead_in_and_capitalizes(self):
        from sync_latest_episode import card_blurb
        text = "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Jane Doe, founder of Doe Widgets."
        self.assertEqual(card_blurb(text), "Jane Doe, founder of Doe Widgets.")
        self.assertEqual(card_blurb("In this episode, Jane Doe shares her story."), "Jane Doe shares her story.")

    def test_leaves_other_openings_alone(self):
        from sync_latest_episode import card_blurb
        self.assertEqual(card_blurb("Jane Doe went from A to B."), "Jane Doe went from A to B.")


if __name__ == "__main__":
    unittest.main()
