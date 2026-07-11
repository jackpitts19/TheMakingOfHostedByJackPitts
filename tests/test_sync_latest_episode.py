"""Tests for sync_latest_episode.py helpers. Run: python3 -m unittest discover tests"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sync_latest_episode import truncate_at_word, extract_guest_name, normalize_duration


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
