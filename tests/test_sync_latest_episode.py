"""Tests for sync_latest_episode.py helpers. Run: python3 -m unittest discover tests"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sync_latest_episode import truncate_at_word, extract_guest_name, normalize_duration
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


class ExtractGuestNameTests(unittest.TestCase):
    def test_in_the_making_of_prefix(self):
        self.assertEqual(extract_guest_name("In The Making Of: Nishank Gite"), "Nishank Gite")

    def test_company_title_with_colon(self):
        self.assertEqual(
            extract_guest_name("Concentrate AI: The LLM Gateway for Fast-Growing Teams"),
            "Concentrate AI",
        )


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
