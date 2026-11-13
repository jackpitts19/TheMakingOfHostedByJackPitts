"""Tests for resolve_youtube_links.py. No network.

Run: python3 -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from resolve_youtube_links import apply_youtube, parse_feed, watch_url
from sync_latest_episode import SHOW_YOUTUBE, load_episodes

FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
  <entry><yt:videoId>NEW111</yt:videoId><title>The Making Of Jane Doe: Building Doe Widgets</title></entry>
  <entry><yt:videoId>SHORT22</yt:videoId><title>Hire for the skills you lack #Leadership</title></entry>
  <entry><yt:videoId>OLD333</yt:videoId><title>The Making Of Jane Doe: Building Doe Widgets</title></entry>
</feed>"""


def episode(title, youtube=SHOW_YOUTUBE):
    return {"title": title, "links": {"spotify": "s", "apple": "a", "youtube": youtube}}


class ParseFeedTests(unittest.TestCase):
    def test_newest_upload_wins_on_duplicate_title(self):
        videos = parse_feed(FEED)
        self.assertIn(watch_url("NEW111"), videos.values())
        self.assertNotIn(watch_url("OLD333"), videos.values())


class ApplyTests(unittest.TestCase):
    def test_episode_on_channel_url_gets_its_video(self):
        eps = [episode("The Making Of Jane Doe: Building Doe Widgets")]
        changed = apply_youtube(eps, parse_feed(FEED))
        self.assertEqual(changed, ["The Making Of Jane Doe: Building Doe Widgets"])
        self.assertEqual(eps[0]["links"]["youtube"], watch_url("NEW111"))
        self.assertEqual(eps[0]["links"]["spotify"], "s")

    def test_hand_set_watch_url_is_never_overwritten(self):
        eps = [episode("The Making Of Jane Doe: Building Doe Widgets", watch_url("MANUAL"))]
        self.assertEqual(apply_youtube(eps, parse_feed(FEED)), [])
        self.assertEqual(eps[0]["links"]["youtube"], watch_url("MANUAL"))

    def test_unmatched_episode_keeps_channel_url(self):
        eps = [episode("Somebody Else Entirely")]
        self.assertEqual(apply_youtube(eps, parse_feed(FEED)), [])
        self.assertEqual(eps[0]["links"]["youtube"], SHOW_YOUTUBE)

    def test_title_match_ignores_curly_quotes_and_punctuation(self):
        feed = FEED.replace("Jane Doe", "Jane “JD” Doe")
        eps = [episode('The Making Of Jane "JD" Doe: Building Doe Widgets')]
        self.assertEqual(len(apply_youtube(eps, parse_feed(feed))), 1)


class CatalogTests(unittest.TestCase):
    def test_every_episode_with_an_upload_links_its_own_video(self):
        # Adam Stevenson's episode has no YouTube upload yet (owner to publish);
        # every other episode must point at its own watch URL, not the channel.
        _, eps = load_episodes()
        on_channel = {e["slug"] for e in eps if e["links"].get("youtube") == SHOW_YOUTUBE}
        self.assertLessEqual(on_channel, {"adam-stevenson"})


if __name__ == "__main__":
    unittest.main()
