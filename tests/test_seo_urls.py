"""Tests for seo_urls episode slugs. Run: python3 -m unittest discover tests"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from seo_urls import EPISODES_DIR, episode_slug
from sync_latest_episode import load_episodes

# The live URLs as of October 2026. Every one is already shared, indexed and
# used as a share-card path, so none may ever change.
FROZEN_SLUGS = {
    "From Selling Ice to Building a 140-Person Pet Care Business | Scott Burnley":
        "from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
    "How Four Veterans Built Four Branches Bourbon | Rick Franco & Mike Trott":
        "how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott",
    "Dave Moorman: Building an MSP, Scaling Through M&A & Exiting Twice": "dave-moorman",
    "Davies Hood of Induron Protective Coatings: Building an 80-Year Family Business":
        "davies-hood-of-induron-protective-coatings",
    "Concentrate AI: The LLM Gateway for Fast-Growing Teams": "concentrate-ai",
    "In The Making Of: Nishank Gite": "nishank-gite",
    "The Making Of Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas": "alex-dixon",
    "The Making Of David Sauers: Building Royal Restrooms Into a Nationwide Franchise": "david-sauers",
    "In The Making Of: Jesse Choe": "jesse-choe",
    "The Making Of Shane Crocker: From Family Business to Multi-Industry Operator": "shane-crocker",
    'The Making Of Dave "Laundromat Millionaire" Menz': "dave-menz",
    "The Making Of Lou Mongello: From Lawyer to Disney Entrepreneur": "lou-mongello",
    "In The Making Of: Niilo Pirttijärvi": "niilo-pirttij-rvi",
    "The Making of Kris Carlson: From Sales to Seafood": "kris-carlson",
    "In The Making Of: Ian Hicks": "ian-hicks",
    "The Making of Robbie Ferman: From Brokerage to Building Sollevare Group": "robbie-ferman",
    "The Making of Doug Taylor: Taylor's Candy": "doug-taylor",
    "The Making of Adam Stevenson: From Flipping Burgers to Building Businesses": "adam-stevenson",
    "The Making of Mammoth Holdings with Gary Dennis": "gary-dennis",
}


class EpisodeSlugTests(unittest.TestCase):
    def test_pinned_slug_wins_over_guest(self):
        ep = {"title": "Topic | Jane Doe", "guest": "Jane Doe", "slug": "topic-jane-doe"}
        self.assertEqual(episode_slug(ep), "topic-jane-doe")

    def test_falls_back_to_slugified_guest_without_a_pin(self):
        self.assertEqual(episode_slug({"title": "X", "guest": "Jane Doe"}), "jane-doe")

    def test_empty_slug_falls_back_to_guest(self):
        self.assertEqual(episode_slug({"title": "X", "guest": "Jane Doe", "slug": ""}), "jane-doe")

    def test_pipe_title_without_guest_uses_the_name(self):
        self.assertEqual(episode_slug({"title": "A Long Topic | Jane Doe"}), "jane-doe")


class LiveSlugFreezeTests(unittest.TestCase):
    def setUp(self):
        _, self.episodes = load_episodes()

    def test_every_episode_pins_its_slug(self):
        for ep in self.episodes:
            with self.subTest(title=ep["title"]):
                self.assertTrue(ep.get("slug"))

    def test_existing_live_slugs_never_change(self):
        by_title = {ep["title"]: episode_slug(ep) for ep in self.episodes}
        for title, slug in FROZEN_SLUGS.items():
            with self.subTest(title=title):
                self.assertEqual(by_title.get(title), slug)

    def test_every_episode_has_a_page_on_disk(self):
        for ep in self.episodes:
            with self.subTest(title=ep["title"]):
                self.assertTrue((EPISODES_DIR / f"{episode_slug(ep)}.html").is_file())

    def test_guest_is_a_person_not_the_title(self):
        for ep in self.episodes:
            with self.subTest(title=ep["title"]):
                self.assertNotEqual(ep.get("guest"), ep["title"])
                self.assertNotIn("|", ep.get("guest", ""))


if __name__ == "__main__":
    unittest.main()
