"""Tests for the ranked podcast listicles. Run: python3 -m unittest discover tests

The listicles name other people's shows, so the rules that matter most are
about honesty and consistency: our own show is first and disclosed, the rest
are alphabetical and unnumbered (only the disclosed pick is a ranking), FAQ
structured data says exactly what the page says, every headline signal
matches the visible H1, the lists do not repeat each other's prose, every
link resolves, and the committed pages match their source content.
"""

import json
import re
import sys
import unittest
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_listicles import related_for
from listicle_render import all_shows, anchor, render
from listicles import ALL
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SHOW_NAME
from seo_urls import BASE_URL, UNLISTED_MARKER, article_pages

ROOT = Path(__file__).parent.parent
JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def _rendered(data):
    return render(data, related_for(data["slug"]))


def _json_ld(html):
    blocks = []
    for raw in JSON_LD_RE.findall(html):
        parsed = json.loads(raw)
        blocks.extend(parsed if isinstance(parsed, list) else [parsed])
    return {block["@type"]: block for block in blocks}


def _sort_key(name):
    return re.sub(r"^the\s+|[^a-z0-9 ]", "", name.lower())


# Prose shared on purpose: the disclosure and market context sections and the
# one-line table intro that repeats the disclosure. Shared show overviews are
# cited facts kept in listicles/shows.py, so they are exempt as well.
PARAGRAPH_RE = re.compile(r"<(p|li)\b[^>]*>(.*?)</\1>", re.S)
MIN_DUPLICATE_LENGTH = 80


def _paragraphs(html_fragment):
    for _, inner in PARAGRAPH_RE.findall(html_fragment):
        text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", inner))).strip()
        if len(text) > MIN_DUPLICATE_LENGTH:
            yield text


def _own_prose(data):
    """Every paragraph on a list that is meant to be written for that list."""
    chunks = [data["answer"], f"<p>{data['tldr_close']}</p>"]
    chunks += [body for heading, body in data["sections_before"] + data["sections_after"]
               if body not in (DISCLOSURE, MARKET_CONTEXT[1])]
    for show in all_shows(data):
        chunks += [body for heading, body in show["sections"] if heading != "Overview"]
    chunks += [f"<p>{answer}</p>" for _, answer in data["faqs"]]
    return [p for chunk in chunks for p in _paragraphs(f"<p>{chunk}</p>" if not chunk.startswith("<") else chunk)]


class ListicleContentTests(unittest.TestCase):
    def test_our_show_ranks_first_with_a_badge(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertEqual(all_shows(data)[0]["name"], SHOW_NAME)
                self.assertTrue(data["our_show"]["badge"])

    def test_other_shows_are_alphabetical(self):
        for data in ALL:
            names = [s["name"] for s in data["shows"]]
            with self.subTest(slug=data["slug"]):
                self.assertEqual(names, sorted(names, key=_sort_key))

    def test_no_show_is_listed_twice(self):
        for data in ALL:
            names = [s["name"] for s in all_shows(data)]
            with self.subTest(slug=data["slug"]):
                self.assertEqual(len(names), len(set(names)))

    def test_slugs_titles_and_descriptions_are_unique(self):
        for field in ("slug", "title_tag", "meta_description", "headline"):
            values = [d[field] for d in ALL]
            with self.subTest(field=field):
                self.assertEqual(len(values), len(set(values)))

    def test_title_and_description_fit_search_snippets(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertLessEqual(len(data["meta_description"]), 160)
                self.assertLessEqual(len(data["title_tag"]), 65)

    def test_headline_matches_the_visible_h1(self):
        # Article.headline, the breadcrumb, the ItemList name, og:title,
        # related links, and llms.txt all read data["headline"].
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertEqual(data["headline"], f"{data['h1']} {data['h1_em']}")
                self.assertLessEqual(len(data["headline"]), 110)

    def test_lists_do_not_repeat_each_others_prose(self):
        seen = {}
        for data in ALL:
            for text in set(_own_prose(data)):
                with self.subTest(slug=data["slug"], text=text[:60]):
                    self.assertFalse(text in seen, f"{text!r} is also on {seen.get(text)}")
                seen.setdefault(text, data["slug"])

    def test_every_listicle_cites_sources(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertGreaterEqual(len(data["sources"]), len(all_shows(data)) - 1)
                for _, url in data["sources"]:
                    self.assertTrue(url.startswith("https://"), url)


class ListicleRenderTests(unittest.TestCase):
    def test_exactly_one_h1(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertEqual(_rendered(data).count("<h1"), 1)

    def test_disclosure_section_is_present(self):
        for data in ALL:
            html = _rendered(data)
            with self.subTest(slug=data["slug"]):
                self.assertIn('id="disclosure-and-methodology"', html)
                self.assertIn("ranks itself first", html)

    def test_item_list_matches_ranked_order(self):
        for data in ALL:
            item_list = _json_ld(_rendered(data))["ItemList"]
            names = [i["name"] for i in item_list["itemListElement"]]
            with self.subTest(slug=data["slug"]):
                self.assertEqual(names, [s["name"] for s in all_shows(data)])
                self.assertEqual(item_list["numberOfItems"], len(names))

    def test_only_the_disclosed_pick_is_numbered(self):
        # The others are alphabetical, so neither the page nor the schema may
        # imply a No. 2 or No. 3.
        for data in ALL:
            html = _rendered(data)
            graph = _json_ld(html)
            with self.subTest(slug=data["slug"]):
                self.assertEqual(graph["ItemList"]["itemListOrder"], "https://schema.org/ItemListUnordered")
                self.assertEqual(re.findall(r"No\. (\d+)", html), ["1"])
                self.assertNotIn("Ranked", data["title_tag"] + data["headline"])

    def test_headline_signals_agree(self):
        for data in ALL:
            graph = _json_ld(_rendered(data))
            with self.subTest(slug=data["slug"]):
                self.assertEqual(graph["Article"]["headline"], data["headline"])
                self.assertEqual(graph["BreadcrumbList"]["itemListElement"][-1]["name"], data["headline"])
                self.assertEqual(graph["ItemList"]["name"], data["headline"])

    def test_faq_structured_data_matches_visible_text(self):
        for data in ALL:
            html = _rendered(data)
            faq = _json_ld(html)["FAQPage"]
            visible = unescape(html)
            with self.subTest(slug=data["slug"]):
                self.assertEqual(len(faq["mainEntity"]), len(data["faqs"]))
                for entry in faq["mainEntity"]:
                    self.assertIn(entry["name"], visible)
                    self.assertIn(entry["acceptedAnswer"]["text"], visible)

    def test_every_fragment_link_has_a_target(self):
        for data in ALL:
            html = _rendered(data)
            ids = set(re.findall(r'id="([^"]+)"', html))
            with self.subTest(slug=data["slug"]):
                for frag in re.findall(r'href="#([^"]+)"', html):
                    self.assertIn(frag, ids)

    def test_internal_links_resolve_to_files(self):
        for data in ALL:
            html = _rendered(data)
            for href in re.findall(r'href="(/[^"#]*)', html):
                path = href.rstrip("/")
                if path in ("", "/"):
                    continue
                with self.subTest(slug=data["slug"], href=href):
                    self.assertTrue((ROOT / f"{path.lstrip('/')}.html").is_file(), href)

    def test_links_to_at_least_one_episode(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertIn('href="/episodes/', _rendered(data))

    def test_no_em_dashes(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertNotIn("—", _rendered(data))

    def test_anchor_is_url_safe(self):
        self.assertEqual(anchor("The $100 MBA Show"), "the-100-mba-show")
        self.assertEqual(anchor("Q&A Time"), "q-and-a-time")


class CommittedPagesAreFreshTests(unittest.TestCase):
    def test_articles_match_their_source_content(self):
        # Editing listicles/*.py without re-running generate_listicles.py
        # would ship stale pages; this catches it before the push.
        for data in ALL:
            path = ROOT / "articles" / f"{data['slug']}.html"
            with self.subTest(slug=data["slug"]):
                self.assertTrue(path.is_file(), f"run python3 generate_listicles.py ({path.name} missing)")
                self.assertEqual(
                    path.read_text(encoding="utf-8"), _rendered(data),
                    f"{path.name} is stale: run python3 generate_listicles.py",
                )



class UnlistedButIndexedTests(unittest.TestCase):
    """The lists exist for search: indexable and in the sitemap, but no
    regular page on the site links to them (only the lists link each other)."""

    def _site_pages(self):
        listicle_files = {f"{d['slug']}.html" for d in ALL}
        pages = [ROOT / "articles.html", ROOT / "index.html", ROOT / "episodes.html"]
        pages += sorted((ROOT / "episodes").glob("*.html"))
        pages += [p for p in (ROOT / "articles").glob("*.html") if p.name not in listicle_files]
        pages += [ROOT / n for n in ("about.html", "press.html", "be-a-guest.html", "404.html")]
        return [p for p in pages if p.is_file()]

    def test_no_regular_page_links_to_a_listicle(self):
        for page in self._site_pages():
            html = page.read_text(encoding="utf-8")
            for data in ALL:
                with self.subTest(page=page.name, slug=data["slug"]):
                    self.assertNotIn(f'/articles/{data["slug"]}"', html)

    def test_listicles_are_marked_unlisted(self):
        for data in ALL:
            with self.subTest(slug=data["slug"]):
                self.assertIn(UNLISTED_MARKER, _rendered(data))

    def test_related_reading_skips_listicles(self):
        paths = {path for path, _ in article_pages()}
        for data in ALL:
            self.assertNotIn(f"/articles/{data['slug']}", paths)

    def test_listicles_stay_indexable_and_in_the_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for data in ALL:
            html = _rendered(data)
            with self.subTest(slug=data["slug"]):
                self.assertIn(f"{BASE_URL}/articles/{data['slug']}</loc>", sitemap)
                self.assertNotIn("noindex", html)


if __name__ == "__main__":
    unittest.main()
