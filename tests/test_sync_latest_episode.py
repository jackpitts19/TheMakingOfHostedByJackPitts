"""Tests for sync_latest_episode.py helpers. Run: python3 -m unittest discover tests"""

import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))

import resolve_episode_links
import sync_latest_episode
from sync_latest_episode import (
    SHOW_NAME,
    extract_guest_name,
    merge_new_episodes,
    normalize_duration,
    normalize_show_name,
    parse_feed_items,
    strip_tags,
    truncate_at_word,
)
from resolve_episode_links import norm_title, apply_apple_data


class NormTitleTests(unittest.TestCase):
    def test_curly_vs_straight_quotes_match(self):
        self.assertEqual(
            norm_title('The Making Of Dave “Laundromat Millionaire” Menz'),
            norm_title('The Making Of Dave "Laundromat Millionaire" Menz'),
        )

    def test_case_insensitive(self):
        self.assertEqual(
            norm_title("The Making of Kris Carlson: From Sales to Seafood"),
            norm_title("The Making Of Kris Carlson: From Sales to Seafood"),
        )


class ApplyAppleDataTests(unittest.TestCase):
    def _apple_item(self):
        return {
            "trackId": 1000000000001,
            "trackName": "In The Making Of: Test Guest",
            "trackViewUrl": "https://podcasts.apple.com/us/podcast/test/id123?i=1000000000001",
            "description": "A full, untruncated description of the conversation.",
        }

    def test_fills_apple_id_url_and_full_description(self):
        ep = {
            "title": "In The Making Of: Test Guest",
            "description": "A full, untruncated…",
            "links": {"apple": "https://podcasts.apple.com/us/podcast/show/id123"},
        }
        changed = apply_apple_data(ep, self._apple_item())
        self.assertTrue(changed)
        self.assertEqual(ep["appleEpisodeId"], "1000000000001")
        self.assertIn("?i=1000000000001", ep["links"]["apple"])
        self.assertEqual(
            ep["description"], "A full, untruncated description of the conversation."
        )

    def test_keeps_longer_handwritten_description(self):
        ep = {
            "title": "In The Making Of: Test Guest",
            "description": "A carefully hand-written description that is longer than "
            "the Apple one and should therefore be preserved as-is by the resolver.",
            "links": {},
        }
        apply_apple_data(ep, self._apple_item())
        self.assertTrue(ep["description"].startswith("A carefully hand-written"))

    def test_idempotent(self):
        ep = {
            "title": "In The Making Of: Test Guest",
            "description": "short…",
            "links": {},
        }
        apply_apple_data(ep, self._apple_item())
        self.assertFalse(apply_apple_data(ep, self._apple_item()))


class TruncateAtWordTests(unittest.TestCase):
    def test_short_text_is_unchanged(self):
        self.assertEqual(truncate_at_word("A short summary.", 400), "A short summary.")

    def test_long_text_never_cuts_mid_word(self):
        text = "word " * 200  # 1000 chars
        result = truncate_at_word(text, 400)
        self.assertLessEqual(len(result), 401)  # limit + ellipsis
        self.assertTrue(result.endswith("…"))
        self.assertEqual(result[:-1].rstrip().split()[-1], "word")

    def test_never_ends_mid_word(self):
        text = ("x" * 380) + " building a hard-tech startup from scratch"
        result = truncate_at_word(text, 400)
        self.assertTrue(result.endswith("…"))
        # Everything before the ellipsis must be whole words of the source.
        for token in result[:-1].split():
            self.assertIn(token, text.split())

    def test_exact_limit_no_ellipsis(self):
        text = "a" * 400
        self.assertEqual(truncate_at_word(text, 400), text)

    def test_trailing_punctuation_stripped_before_ellipsis(self):
        text = ("word " * 79) + "ends with, trailing comma here"
        result = truncate_at_word(text, 400)
        self.assertFalse(result[:-1].endswith(","))

    def test_prefers_complete_sentence_over_mid_sentence_cut(self):
        sentence = "This is one complete sentence about the guest and the company. "
        text = sentence * 20
        result = truncate_at_word(text, 400)
        self.assertTrue(result.endswith("."))
        self.assertFalse(result.endswith("…"))
        self.assertLessEqual(len(result), 400)

    def test_ignores_sentence_end_when_it_is_too_early(self):
        text = "Short. " + ("word " * 200)
        result = truncate_at_word(text, 400)
        self.assertTrue(result.endswith("…"))

    def test_sentence_boundary_not_triggered_by_decimal_points(self):
        text = "Raised $5.1 million and " + ("word " * 200)
        result = truncate_at_word(text, 400)
        self.assertTrue(result.endswith("…"))


class ExtractGuestNameTests(unittest.TestCase):
    def test_in_the_making_of_prefix(self):
        self.assertEqual(extract_guest_name("In The Making Of: Nishank Gite"), "Nishank Gite")

    def test_company_title_with_colon(self):
        self.assertEqual(
            extract_guest_name("Concentrate AI: The LLM Gateway for Fast-Growing Teams"),
            "Concentrate AI",
        )

    def test_topic_pipe_name_takes_the_name_after_the_pipe(self):
        self.assertEqual(
            extract_guest_name(
                "From Selling Ice to Building a 140-Person Pet Care Business | Scott Burnley"
            ),
            "Scott Burnley",
        )

    def test_topic_pipe_two_names(self):
        self.assertEqual(
            extract_guest_name(
                "How Four Veterans Built Four Branches Bourbon | Rick Franco & Mike Trott"
            ),
            "Rick Franco & Mike Trott",
        )

    def test_uses_the_last_pipe(self):
        self.assertEqual(extract_guest_name("Part One | Topic | Jane Doe"), "Jane Doe")

    def test_from_prefix_takes_the_name_after_the_colon(self):
        self.assertEqual(
            extract_guest_name("From Selling Ice to Pet Care: Scott Burnley"),
            "Scott Burnley",
        )

    def test_from_prefix_takes_the_name_after_with(self):
        self.assertEqual(
            extract_guest_name("From Lawyer to Disney Entrepreneur with Lou Mongello"),
            "Lou Mongello",
        )

    def test_name_of_company_keeps_only_the_name(self):
        self.assertEqual(
            extract_guest_name(
                "Davies Hood of Induron Protective Coatings: Building an 80-Year Family Business"
            ),
            "Davies Hood",
        )

    def test_real_titles_from_episodes_js(self):
        cases = {
            "Dave Moorman: Building an MSP, Scaling Through M&A & Exiting Twice": "Dave Moorman",
            "The Making Of Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas": "Alex Dixon",
            "In The Making Of: Niilo Pirttij\u00e4rvi": "Niilo Pirttij\u00e4rvi",
            "The Making of Kris Carlson: From Sales to Seafood": "Kris Carlson",
            "The Making Of Lou Mongello: From Lawyer to Disney Entrepreneur": "Lou Mongello",
            "The Making of Doug Taylor: Taylor's Candy": "Doug Taylor",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                self.assertEqual(extract_guest_name(title), expected)

    def test_sync_and_seo_urls_share_one_implementation(self):
        import seo_urls

        self.assertIs(sync_latest_episode.extract_guest_name, seo_urls.extract_guest_name)


class ShowNameNormalizationTests(unittest.TestCase):
    def test_comma_and_lowercase_by_variant(self):
        self.assertEqual(
            normalize_show_name("In this episode of The Making Of, Hosted by Jack Pitts, I sit down"),
            f"In this episode of {SHOW_NAME}, I sit down",
        )

    def test_stray_space_before_comma(self):
        self.assertEqual(
            normalize_show_name("of The Making Of, Hosted by Jack Pitts , I sit down"),
            f"of {SHOW_NAME}, I sit down",
        )

    def test_lowercase_by_without_comma(self):
        self.assertEqual(
            normalize_show_name("of The Making Of Hosted by Jack Pitts, I sit down"),
            f"of {SHOW_NAME}, I sit down",
        )

    def test_bare_show_name_followed_by_comma(self):
        self.assertEqual(
            normalize_show_name("In this episode of The Making Of, I sit down with Alex Dixon"),
            f"In this episode of {SHOW_NAME}, I sit down with Alex Dixon",
        )

    def test_already_correct_text_is_unchanged(self):
        text = f"On this episode of {SHOW_NAME}, Shane Crocker shares his journey."
        self.assertEqual(normalize_show_name(text), text)

    def test_titles_with_making_of_a_guest_are_untouched(self):
        text = "The Making of Kris Carlson: From Sales to Seafood"
        self.assertEqual(normalize_show_name(text), text)

    def test_strip_tags_applies_the_normalization(self):
        self.assertEqual(
            strip_tags("<p>In this episode of The Making Of, Hosted by Jack Pitts, I sit down</p>"),
            f"In this episode of {SHOW_NAME}, I sit down",
        )

    def test_episodes_js_descriptions_are_already_normalized(self):
        _, episodes = sync_latest_episode.load_episodes()
        for ep in episodes:
            for field in ("description", "appleDescription"):
                text = ep.get(field) or ""
                with self.subTest(title=ep["title"], field=field):
                    self.assertEqual(normalize_show_name(text), text)
                    self.assertNotIn("The Making Of,", text)
                    self.assertNotIn("Hosted by Jack", text)


RSS_NS = 'xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"'


def rss_item(title, pub_date, guid=None, description="A description of the episode.",
             duration="3780"):
    guid_xml = f"<guid>{guid}</guid>" if guid else ""
    return (
        f"<item><title>{title}</title><pubDate>{pub_date}</pubDate>{guid_xml}"
        f"<description>{description}</description>"
        f"<itunes:duration>{duration}</itunes:duration></item>"
    )


def rss(*items):
    return f'<rss {RSS_NS}><channel><title>Show</title>{"".join(items)}</channel></rss>'


def existing_episode(title, date, guest, slug=None, guid=None):
    ep = {"date": date, "title": title, "guest": guest, "slug": slug or guest.lower().replace(" ", "-")}
    if guid:
        ep["guid"] = guid
    return ep


class ParseFeedItemsTests(unittest.TestCase):
    def test_parses_every_item_with_guid_guest_and_pinned_slug(self):
        xml = rss(
            rss_item("Topic Two | Jane Doe", "Wed, 21 Oct 2026 10:00:00 +0000", guid="g-2"),
            rss_item("The Making Of John Roe: A Story", "Wed, 07 Oct 2026 10:00:00 +0000", guid="g-1"),
        )
        items = parse_feed_items(xml)
        self.assertEqual([i["guest"] for i in items], ["Jane Doe", "John Roe"])
        self.assertEqual([i["slug"] for i in items], ["jane-doe", "john-roe"])
        self.assertEqual([i["guid"] for i in items], ["g-2", "g-1"])
        self.assertEqual(items[0]["date"], "2026-10-21")
        self.assertEqual(items[0]["dateLabel"], "October 21, 2026")
        self.assertEqual(items[0]["duration"], "1h 3m")

    def test_date_is_taken_in_utc(self):
        xml = rss(rss_item("Topic | Jane Doe", "Wed, 21 Oct 2026 23:30:00 -0500"))
        self.assertEqual(parse_feed_items(xml)[0]["date"], "2026-10-22")

    def test_normalizes_show_name_and_em_dashes_at_ingestion(self):
        xml = rss(rss_item(
            "Topic \u2014 More | Jane Doe",
            "Wed, 21 Oct 2026 10:00:00 +0000",
            description="In this episode of The Making Of, Hosted by Jack Pitts, I sit down with Jane \u2014 a founder.",
        ))
        item = parse_feed_items(xml)[0]
        self.assertNotIn("\u2014", item["title"])
        self.assertNotIn("\u2014", item["description"])
        self.assertIn(SHOW_NAME + ",", item["description"])

    def test_zero_items_is_refused(self):
        with self.assertRaises(RuntimeError):
            parse_feed_items(rss())

    def test_missing_channel_is_refused(self):
        with self.assertRaises(RuntimeError):
            parse_feed_items("<rss></rss>")


class MergeNewEpisodesTests(unittest.TestCase):
    def setUp(self):
        self.existing = [
            existing_episode("The Making Of Dave \u201cLaundromat Millionaire\u201d Menz", "2026-04-09", "Dave Menz"),
            existing_episode("In The Making Of: Ian Hicks", "2026-02-05", "Ian Hicks"),
        ]

    def _item(self, title, date, guest, guid=None):
        return {"title": title, "date": date, "guest": guest, "slug": guest.lower().replace(" ", "-"),
                "guid": guid or f"guid-{guest}"}

    def test_nothing_new_returns_the_same_entries(self):
        items = [
            self._item('The Making Of Dave "Laundromat Millionaire" Menz', "2026-04-09", "Dave Menz"),
            self._item("In The Making Of: Ian Hicks", "2026-02-05", "Ian Hicks"),
        ]
        merged, added = merge_new_episodes(self.existing, items)
        self.assertEqual(added, [])
        self.assertEqual([e["title"] for e in merged], [e["title"] for e in self.existing])

    def test_title_match_ignores_case_quotes_dashes_and_whitespace(self):
        items = [
            self._item("the making of dave 'laundromat millionaire' menz ", "2026-04-09", "Dave Menz"),
            self._item("In The Making Of \u2013 Ian  Hicks", "2026-02-05", "Ian Hicks"),
        ]
        _, added = merge_new_episodes(self.existing, items)
        self.assertEqual(added, [])

    def test_matches_by_guid_even_when_the_title_was_edited(self):
        existing = [existing_episode("Old Title | Jane Doe", "2026-05-01", "Jane Doe", guid="abc")]
        items = [self._item("Totally New Title", "2026-05-03", "Someone Else", guid="abc")]
        _, added = merge_new_episodes(existing, items)
        self.assertEqual(added, [])

    def test_matches_by_date_and_guest_when_the_title_changed(self):
        items = [self._item("Ian Hicks: A Retitled Episode", "2026-02-05", "Ian Hicks", guid="new-guid")]
        _, added = merge_new_episodes(self.existing, items)
        self.assertEqual(added, [])

    def test_backfills_guid_on_matched_entries_without_mutating_input(self):
        items = [self._item("In The Making Of: Ian Hicks", "2026-02-05", "Ian Hicks", guid="ian-guid")]
        merged, _ = merge_new_episodes(self.existing, items)
        self.assertEqual(merged[1]["guid"], "ian-guid")
        self.assertNotIn("guid", self.existing[1])

    def test_adds_every_new_item_newest_first(self):
        items = [
            self._item("Topic B | Bea Two", "2026-10-21", "Bea Two"),
            self._item("Topic A | Al One", "2026-10-07", "Al One"),
            self._item("In The Making Of: Ian Hicks", "2026-02-05", "Ian Hicks"),
        ]
        merged, added = merge_new_episodes(self.existing, items)
        self.assertEqual([e["guest"] for e in added], ["Al One", "Bea Two"])
        self.assertEqual(
            [e["guest"] for e in merged], ["Bea Two", "Al One", "Dave Menz", "Ian Hicks"]
        )
        self.assertEqual(merged[0]["slug"], "bea-two")

    def test_new_slug_that_collides_gets_the_date_appended(self):
        items = [
            self._item("Round Two | Ian Hicks", "2026-10-21", "Ian Hicks", guid="second"),
            self._item("In The Making Of: Dave Menz", "2026-04-09", "Dave Menz"),
        ]
        merged, added = merge_new_episodes(self.existing, items)
        self.assertEqual(len(added), 1)
        self.assertEqual(merged[0]["slug"], "ian-hicks-2026-10-21")

    def test_caps_new_items_per_run_keeping_the_newest(self):
        items = [
            self._item(f"Topic {n} | Guest {n}", f"2026-10-{n:02d}", f"Guest {n}")
            for n in range(20, 0, -1)
        ] + [self._item("In The Making Of: Ian Hicks", "2026-02-05", "Ian Hicks")]
        with mock.patch("sys.stderr"):
            merged, added = merge_new_episodes(self.existing, items, max_new=10)
        self.assertEqual(len(added), 10)
        self.assertEqual(merged[0]["guest"], "Guest 20")
        self.assertEqual(merged[9]["guest"], "Guest 11")

    def test_refuses_when_several_items_are_new_and_none_match(self):
        items = [
            self._item("Topic B | Bea Two", "2026-10-21", "Bea Two"),
            self._item("Topic A | Al One", "2026-10-07", "Al One"),
        ]
        with self.assertRaises(RuntimeError):
            merge_new_episodes(self.existing, items)


class FetchTextRetryTests(unittest.TestCase):
    def test_retries_then_succeeds(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b"ok"
        calls = [urllib.error.URLError("down"), TimeoutError("slow"), response]
        with mock.patch("sync_latest_episode.urllib.request.urlopen", side_effect=calls) as m, \
                mock.patch("sync_latest_episode.time.sleep") as sleep:
            self.assertEqual(sync_latest_episode.fetch_text("https://example.com"), "ok")
        self.assertEqual(m.call_count, 3)
        self.assertEqual(sleep.call_count, 2)
        self.assertIn("timeout", m.call_args.kwargs)

    def test_gives_up_after_three_attempts(self):
        with mock.patch("sync_latest_episode.urllib.request.urlopen",
                        side_effect=urllib.error.URLError("down")) as m, \
                mock.patch("sync_latest_episode.time.sleep"):
            with self.assertRaises(RuntimeError):
                sync_latest_episode.fetch_text("https://example.com")
        self.assertEqual(m.call_count, 3)


class TempEpisodesFileMixin:
    PREFIX = "// header\nwindow.EPISODES = "

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "episodes.js"
        self.episodes = [
            existing_episode("Topic | Old Guest", "2026-09-01", "Old Guest", guid="old"),
        ]
        self.path.write_text(self.PREFIX + json.dumps(self.episodes, indent=2) + ";\n", encoding="utf-8")
        self.original = self.path.read_bytes()
        patcher = mock.patch.object(sync_latest_episode, "EPISODES_JS", self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)


class SaveEpisodesGuardTests(TempEpisodesFileMixin, unittest.TestCase):
    def test_refuses_to_shrink_the_list(self):
        with self.assertRaises(RuntimeError):
            sync_latest_episode.save_episodes(self.PREFIX, [])
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_writes_a_longer_list(self):
        longer = [existing_episode("Topic | New", "2026-10-01", "New")] + self.episodes
        sync_latest_episode.save_episodes(self.PREFIX, longer)
        _, saved = sync_latest_episode.load_episodes()
        self.assertEqual(len(saved), 2)


class SyncMainTests(TempEpisodesFileMixin, unittest.TestCase):
    def test_feed_outage_exits_nonzero_without_writing(self):
        def broken():
            raise RuntimeError("feed down")
        with mock.patch("sys.stderr"):
            code = sync_latest_episode.run(fetch_items=broken)
        self.assertNotEqual(code, 0)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_empty_feed_exits_nonzero_without_writing(self):
        with mock.patch("sys.stderr"):
            code = sync_latest_episode.run(fetch_items=lambda: parse_feed_items(rss()))
        self.assertNotEqual(code, 0)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_no_new_episode_leaves_file_byte_identical(self):
        xml = rss(rss_item("Topic | Old Guest", "Tue, 01 Sep 2026 10:00:00 +0000", guid="old"))
        with mock.patch("sys.stdout"):
            code = sync_latest_episode.run(fetch_items=lambda: parse_feed_items(xml))
        self.assertEqual(code, 0)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_new_episodes_are_written_with_slug_and_guid(self):
        xml = rss(
            rss_item("Second Story | Bea Two", "Wed, 21 Oct 2026 10:00:00 +0000", guid="b"),
            rss_item("First Story | Al One", "Wed, 07 Oct 2026 10:00:00 +0000", guid="a"),
            rss_item("Topic | Old Guest", "Tue, 01 Sep 2026 10:00:00 +0000", guid="old"),
        )
        with mock.patch("sys.stdout"):
            code = sync_latest_episode.run(fetch_items=lambda: parse_feed_items(xml))
        self.assertEqual(code, 0)
        text = self.path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(self.PREFIX))
        _, saved = sync_latest_episode.load_episodes()
        self.assertEqual([e["guest"] for e in saved], ["Bea Two", "Al One", "Old Guest"])
        self.assertEqual(saved[0]["slug"], "bea-two")
        self.assertEqual(saved[0]["guid"], "b")


class DiscoverFeedUrlTests(unittest.TestCase):
    def test_falls_back_to_the_known_feed_when_apple_lookup_fails(self):
        def fetch(url):
            raise RuntimeError("apple down")
        with mock.patch("sys.stderr"):
            url = sync_latest_episode.discover_feed_url(fetch=fetch)
        self.assertEqual(url, sync_latest_episode.FEED_URL_FALLBACK)

    def test_uses_apple_feed_url_when_available(self):
        payload = json.dumps({"results": [{"feedUrl": "https://feeds.example.com/show.rss"}]})
        url = sync_latest_episode.discover_feed_url(fetch=lambda u: payload)
        self.assertEqual(url, "https://feeds.example.com/show.rss")


class ResolveAppleOutageTests(TempEpisodesFileMixin, unittest.TestCase):
    def test_apple_failure_is_a_warning_and_leaves_data_intact(self):
        def broken():
            raise RuntimeError("apple down")
        with mock.patch("sys.stderr"), mock.patch("sys.stdout"):
            code = resolve_episode_links.main(fetch=broken)
        self.assertEqual(code, 0)
        self.assertEqual(self.path.read_bytes(), self.original)


class NormalizeDurationTests(unittest.TestCase):
    def test_seconds(self):
        self.assertEqual(normalize_duration("3780"), "1h 3m")

    def test_hms(self):
        self.assertEqual(normalize_duration("1:03:00"), "1h 3m")

    def test_hms_under_one_hour_has_no_zero_hours(self):
        self.assertEqual(normalize_duration("00:31:07"), "31 min")

    def test_seconds_under_one_hour(self):
        self.assertEqual(normalize_duration("1860"), "31 min")


if __name__ == "__main__":
    unittest.main()
