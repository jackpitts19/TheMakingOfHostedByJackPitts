"""Tests for the link-preview cards and the og:image rules that point at them.

Run: python3 -m unittest discover tests
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))

import card_type
import generate_share_cards as cards
from validate_seo import check_social_image, png_size

SHOW = "https://themakingofhostedbyjackpitts.com/share-cards/show.png"


def social_head(image=SHOW, width="1200", height="630", alt="Alt", card="summary_large_image", twitter=None):
    return (
        f'<meta property="og:image" content="{image}" />'
        f'<meta property="og:image:width" content="{width}" />'
        f'<meta property="og:image:height" content="{height}" />'
        f'<meta property="og:image:alt" content="{alt}" />'
        f'<meta name="twitter:card" content="{card}" />'
        f'<meta name="twitter:image" content="{twitter or image}" />'
    )


class CardTopicTests(unittest.TestCase):
    def test_topic_pipe_guest_title_uses_topic(self):
        ep = {"title": "How Four Veterans Built Four Branches Bourbon | Rick Franco & Mike Trott",
              "guest": "Rick Franco & Mike Trott"}
        self.assertEqual(cards.card_topic(ep), "How Four Veterans Built Four Branches Bourbon")

    def test_making_of_title_uses_part_after_colon(self):
        ep = {"title": "The Making Of Jane Doe: From Lawyer to Founder", "guest": "Jane Doe"}
        self.assertEqual(cards.card_topic(ep), "From Lawyer to Founder")

    def test_brand_ahead_of_colon_is_kept(self):
        ep = {"title": "Acme AI: The Gateway for Teams", "guest": "Jane Doe & John Roe"}
        self.assertEqual(cards.card_topic(ep), "Acme AI: The Gateway for Teams")

    def test_guest_of_company_keeps_company_not_guest(self):
        ep = {"title": "Jane Doe of Acme Coatings: Building a Family Business", "guest": "Jane Doe"}
        self.assertEqual(cards.card_topic(ep), "Acme Coatings: Building a Family Business")

    def test_name_only_title_falls_back_to_seo_title(self):
        ep = {"title": "In The Making Of: Jane Doe", "guest": "Jane Doe",
              "seoTitle": "Jane Doe of Acme: From Physics to Robotics"}
        self.assertEqual(cards.card_topic(ep), "Acme: From Physics to Robotics")

    def test_name_only_title_without_seo_title_has_no_topic(self):
        ep = {"title": "In The Making Of: Jane Doe", "guest": "Jane Doe", "slug": "jane-doe"}
        self.assertEqual(cards.card_topic(ep), "")

    def test_show_name_prefix_is_dropped_from_topic(self):
        ep = {"title": "The Making of Mammoth Holdings with Gary Dennis", "guest": "Gary Dennis"}
        self.assertEqual(cards.card_topic(ep), "Mammoth Holdings")

    def test_topic_that_spells_out_the_guest_falls_back(self):
        ep = {"title": 'The Making Of Jane "The Closer" Doe', "guest": "Jane Doe",
              "seoTitle": "Jane Doe of Acme: Selling to Banks"}
        self.assertEqual(cards.card_topic(ep), "Acme: Selling to Banks")

    def test_topic_that_spells_out_the_guest_uses_quoted_phrase_without_seo(self):
        ep = {"title": 'The Making Of Jane "The Closer" Doe', "guest": "Jane Doe", "slug": "jane-doe"}
        self.assertEqual(cards.card_topic(ep), "\u201cThe Closer\u201d")

    def test_company_named_after_guest_surname_is_kept(self):
        ep = {"title": "The Making of Doug Taylor: Taylor's Candy", "guest": "Doug Taylor"}
        self.assertEqual(cards.card_topic(ep), "Taylor\u2019s Candy")

    def test_published_episodes_never_repeat_the_guest_or_show_name(self):
        for ep in cards.load_episodes():
            topic = cards.card_topic(ep)
            guest = cards.clean_text(ep.get("guest"))
            self.assertFalse(topic.lower().startswith("the making of"), topic)
            self.assertFalse(cards._names_person(topic, guest), topic)

    def test_entities_decode_and_quotes_curl(self):
        self.assertEqual(cards.clean_text("Rick &amp; Mike's \"Big\" Day"),
                         "Rick & Mike’s “Big” Day")

    def test_meta_line_formats_issue_date_and_duration(self):
        meta = cards.card_meta(7, {"dateLabel": "March 12, 2026", "duration": "1h 9m"})
        self.assertEqual(meta, "EPISODE 07  ·  MARCH 12, 2026  ·  1 HR 9 MIN")


class TypeTests(unittest.TestCase):
    def test_display_type_is_kerned(self):
        f = cards.face("display", 104)
        self.assertLess(f.length("Ta"), f.length("T") + f.length("a") - 3)

    def test_untracked_text_uses_fi_and_fl_ligatures(self):
        f = cards.face("italic", 36)
        self.assertEqual(f._prepare("Bidflow Profit"), "Bid\ufb02ow Pro\ufb01t")

    def test_tracked_labels_never_ligate(self):
        self.assertEqual(cards.face("label", 19, 2.4)._prepare("fit"), "fit")

    def test_missing_kerning_file_fails_loudly(self):
        with mock.patch.object(card_type, "KERNING_FILE", cards.FONT_DIR / "nope.json"):
            with self.assertRaises(cards.MissingFontError):
                card_type.check_fonts()


class CardLayoutTests(unittest.TestCase):
    def measure(self, size=None):
        return cards.face("italic", size or cards.TOPIC_SIZE).length

    def test_duo_wraps_at_ampersand_with_italic_brown_ampersand(self):
        lines, size = cards.fit_name("Rick Franco & Mike Trott", cards.COL_W)
        self.assertEqual(lines, ["Rick Franco &", "Mike Trott"])
        self.assertLessEqual(size, cards.NAME_MAX_TWO_LINES)
        runs = cards.name_runs(lines[0], size)
        self.assertEqual([(f.role, text, fill) for f, text, fill in runs][-1], ("italic", "&", cards.BROWN))

    def test_short_name_stays_on_one_large_line(self):
        lines, size = cards.fit_name("Ian Hicks", cards.COL_W)
        self.assertEqual(lines, ["Ian Hicks"])
        self.assertEqual(size, cards.NAME_MAX)

    def test_long_topic_clamps_to_two_lines_with_ellipsis(self):
        measure = self.measure()
        lines = cards.clamp_lines("word " * 80, measure, cards.TOPIC_W, 2)
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[-1].endswith("…"))
        self.assertTrue(all(measure(line) <= cards.TOPIC_W for line in lines))

    def test_short_brand_before_colon_does_not_get_its_own_line(self):
        lines = cards.topic_lines_for("Bidflow: Raising $1M at 19 and Getting Into YC", cards.TOPIC_SIZE)
        self.assertEqual(len(lines), 2)
        self.assertNotEqual(lines[0], "Bidflow:")

    def test_balanced_colon_still_breaks_at_colon(self):
        lines = cards.topic_lines_for("Induron Protective Coatings: Building an 80-Year Family Business",
                                      cards.TOPIC_SIZE)
        self.assertEqual(lines, ["Induron Protective Coatings:", "Building an 80-Year Family Business"])

    def test_lines_never_end_on_a_small_word(self):
        for ep in cards.load_episodes():
            for line in cards.topic_lines_for(cards.card_topic(ep), cards.TOPIC_SIZE)[:-1]:
                self.assertNotIn(line.rsplit(" ", 1)[-1].lower(), cards.SMALL_WORDS, line)

    def test_show_deck_is_never_truncated(self):
        lines = cards.topic_lines_for(cards.SHOW_DECK, cards.SHOW_DECK_SIZE, max_w=cards.COL_W,
                                      max_lines=cards.SHOW_DECK_LINES)
        self.assertEqual(" ".join(lines), cards.SHOW_DECK)

    def test_name_starts_at_the_same_height_on_every_card(self):
        one = cards.headline_layout(["Ian Hicks"], 104, ["A topic"], cards.TOPIC_SIZE)[0][0]
        two = cards.headline_layout(["Rick Franco &", "Mike Trott"], 84, ["A", "B"], cards.TOPIC_SIZE)[0][0]
        self.assertEqual(one - round(104 * 0.70), cards.NAME_TOP)
        self.assertEqual(two - round(84 * 0.70), cards.NAME_TOP)

    def test_every_published_headline_clears_the_band(self):
        for ep in cards.load_episodes():
            name = cards.clean_text(ep.get("guest")) or cards.clean_text(ep.get("title"))
            name_lines, size = cards.fit_name(name, cards.COL_W)
            topic = cards.topic_lines_for(cards.card_topic(ep), cards.TOPIC_SIZE)
            name_ys, topic_ys = cards.headline_layout(name_lines, size, topic, cards.TOPIC_SIZE)
            self.assertLessEqual((topic_ys or name_ys)[-1], cards.TEXT_BOTTOM, name)

    def test_logo_tile_sits_on_the_rule(self):
        self.assertEqual(cards.ART_Y, cards.RULE_Y)

    def test_missing_font_fails_loudly(self):
        missing = dict(cards.FONT_FILES, display=cards.FONT_DIR / "nope" / "Missing.ttf")
        with mock.patch.dict(cards.FONT_FILES, missing):
            with self.assertRaises(cards.MissingFontError) as ctx:
                cards.check_fonts()
        self.assertIn("Missing.ttf", str(ctx.exception))

    def test_rendered_cards_are_1200_by_630(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "card.png"
            cards.render_card({"title": "A Topic | Jane Doe", "guest": "Jane Doe",
                               "dateLabel": "May 1, 2026", "duration": "40 min"}, 3, out)
            self.assertEqual(png_size(out), (1200, 630))
            show = Path(tmp) / "show.png"
            cards.render_show_card(show)
            self.assertEqual(png_size(show), (1200, 630))


class SocialImageRuleTests(unittest.TestCase):
    def errors_for(self, html, size=(1200, 630)):
        errors = []
        check_social_image(errors, "page.html", html, image_size=lambda url: size)
        return errors

    def test_complete_tags_pass(self):
        self.assertEqual(self.errors_for(social_head()), [])

    def test_missing_file_fails(self):
        self.assertTrue(any("does not exist" in e for e in self.errors_for(social_head(), size=False)))

    def test_declared_size_must_match_file(self):
        self.assertTrue(any("1024x1024" in e for e in self.errors_for(social_head(), size=(1024, 1024))))

    def test_small_twitter_card_fails(self):
        self.assertTrue(any("summary_large_image" in e for e in self.errors_for(social_head(card="summary"))))

    def test_mismatched_twitter_image_fails(self):
        html = social_head(twitter="https://themakingofhostedbyjackpitts.com/logo.png")
        self.assertTrue(any("does not match" in e for e in self.errors_for(html)))

    def test_missing_alt_fails(self):
        self.assertTrue(any("og:image:alt" in e for e in self.errors_for(social_head(alt=""))))

    def test_missing_og_image_fails(self):
        self.assertEqual(self.errors_for("<title>x</title>"), ["page.html: missing og:image"])


if __name__ == "__main__":
    unittest.main()
