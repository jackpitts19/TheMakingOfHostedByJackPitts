"""Tests for check_crawler_access.py's decisions. No network.

Run: python3 -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from check_crawler_access import disallowed_agents, page_problem


class PageProblemTests(unittest.TestCase):
    def test_real_page_passes(self):
        self.assertIsNone(page_problem(200, "<html><h1>Episodes</h1></html>"))

    def test_blocked_status_fails(self):
        self.assertEqual(page_problem(403, ""), "HTTP 403")

    def test_cloudflare_challenge_fails_even_with_200(self):
        body = "<html><title>Just a moment...</title><h1>x</h1></html>"
        self.assertEqual(page_problem(200, body), "got a bot challenge page")

    def test_page_without_h1_fails(self):
        self.assertIn("no <h1>", page_problem(200, "<html><p>hello</p></html>"))


class RobotsTests(unittest.TestCase):
    def test_current_robots_txt_allows_everyone(self):
        robots = (Path(__file__).parent.parent / "robots.txt").read_text(encoding="utf-8")
        self.assertEqual(disallowed_agents(robots), [])

    def test_ai_block_appended_by_a_managed_robots_txt_is_caught(self):
        robots = "User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nUser-agent: ClaudeBot\nDisallow: /\n"
        self.assertEqual(disallowed_agents(robots), ["ClaudeBot", "GPTBot"])

    def test_site_wide_block_catches_every_crawler(self):
        self.assertIn("Googlebot", disallowed_agents("User-agent: *\nDisallow: /\n"))

    def test_partial_disallow_is_not_a_site_block(self):
        self.assertEqual(disallowed_agents("User-agent: *\nDisallow: /private\n"), [])


if __name__ == "__main__":
    unittest.main()
