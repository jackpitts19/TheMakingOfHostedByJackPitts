#!/usr/bin/env python3
"""
Render a "best podcasts" listicle into a finished article page.

The content of each listicle lives in listicles/<name>.py as a `LISTICLE`
dict. This module turns one of those dicts into HTML that matches the
hand-written articles in articles/: same masthead, answer box, body type,
FAQ, guest strip, and the shared nav and footer from site_nav.py.

The format follows the Salt Creek Advisory comparison guides: our own show
is the disclosed top pick (the only numbered position), the rest follow
alphabetically and unnumbered, a comparison
table up top, a disclosure and methodology section, one profile per show,
an FAQ, and sources.

Pure functions, no I/O: generate_listicles.py does the writing.
"""

from __future__ import annotations

import json
import re
from html import escape

from seo_urls import BASE_URL, SHOW_CARD_ALT, SHOW_CARD_URL, UNLISTED_MARKER, to_url
from site_nav import CHROME_CSS, FOOTER_CSS, TOPNAV_CSS, footer_html, topnav_html

SITE = "The Making Of Hosted By Jack Pitts"
EXTERNAL = ' target="_blank" rel="noopener"'
SHOW_APPLE ="https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
SHOW_SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
SHOW_YOUTUBE = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"

# The same @ids index.html and about.html define, so the lists point at the
# one show and one host instead of anonymous copies.
SERIES_ID = f"{BASE_URL}/#podcast"
HOST_ID = f"{BASE_URL}/about#jack-pitts"
WEBSITE_ID = f"{BASE_URL}/#website"

AUTHOR = {
    "@type": "Person",
    "@id": HOST_ID,
    "name": "Jack Pitts",
    "url": "https://thejackpitts.com/",
    "sameAs": ["https://www.linkedin.com/in/jack-pitts", "https://saltcreekadvisory.com/team"],
}

FAVICON = (
    "data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\">"
    "<rect width=\"64\" height=\"64\" rx=\"14\" fill=\"%23f3e8cf\"/><text x=\"32\" y=\"46\" "
    "text-anchor=\"middle\" font-family=\"Georgia,serif\" font-weight=\"900\" font-size=\"42\" "
    "fill=\"%23d87a2c\">M</text></svg>"
)

# display=optional, not swap: these pages are cold search landers with a lot
# of text above the fold. With swap, a late web font re-flows the headline and
# answer box (measured CLS 0.13 to 0.27 on Lighthouse mobile, over the 0.1
# Core Web Vitals line). With optional, a slow first visit keeps the fallback
# serif for that view and the cached web font is used from the next page on.
FONTS_HREF = (
    "https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400..700"
    "&family=Newsreader:ital,wght@0,400..700;1,400..700&display=optional"
)

MONTHS = (
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
)

# Base article styles: identical to the hand-written articles in articles/.
SERIF = '"Newsreader", Georgia, "Times New Roman", serif'
ARTICLE_CSS = f"""
:root {{
  --cream: #f3e8cf;
  --cream-deep: #ecd9a8;
  --orange: #d87a2c;
  --orange-dark: #934c13;
  --ink: #14130f;
  --ink-soft: #3a352b;
  --line: rgba(20,19,15,0.12);
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: var(--cream); color: var(--ink); }}
body {{ font-family: "Libre Franklin", "Helvetica Neue", Arial, sans-serif; line-height: 1.55; }}
a {{ color: inherit; }}
img {{ max-width: 100%; display: block; }}
body::before {{
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 1;
  opacity: 0.045; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='nf'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23nf)'/%3E%3C/svg%3E");
}}
body > * {{ position: relative; z-index: 2; }}
.wrap {{ max-width: 760px; margin: 0 auto; padding: 0 28px; }}
.topnav .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
.topnav .mark {{ font-family: {SERIF}; font-weight: 700; font-size: 18px; letter-spacing: -0.01em; text-decoration: none; }}
.masthead {{ padding: 52px 0 16px; display: flex; flex-wrap: wrap; gap: 6px 30px; overflow: hidden; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-soft); font-weight: 600; }}
.masthead .kicker {{ color: var(--orange-dark); font-weight: 700; }}
/* Each item draws its own leading dot in a 30px slot. The first item on a
   wrapped line is pulled 30px left, so its dot is clipped by overflow:hidden
   and no line ever starts or ends with a stray dot. */
.masthead > span {{ position: relative; }}
.masthead > span::before {{ content: ''; position: absolute; left: -17px; top: 50%; width: 4px; height: 4px; margin-top: -2px; border-radius: 50%; background: var(--ink-soft); opacity: 0.6; }}
.hero-title {{ font-family: {SERIF}; font-weight: 700; line-height: 1.08; font-size: clamp(34px, 5.4vw, 60px); letter-spacing: -0.022em; margin: 0 0 22px; }}
.hero-title em {{ font-style: italic; color: var(--orange-dark); font-weight: 700; }}
.answer {{ font-family: {SERIF}; font-weight: 500; font-size: clamp(19px, 2.1vw, 23px); line-height: 1.45; color: var(--ink); margin: 0 0 40px; padding: 22px 24px; border-left: 3px solid var(--orange); background: rgba(236, 217, 168, 0.4); border-radius: 0 12px 12px 0; }}
.answer strong {{ font-weight: 700; }}
.body h2 {{ font-family: {SERIF}; font-weight: 700; font-size: clamp(24px, 3vw, 31px); letter-spacing: -0.01em; line-height: 1.15; margin: 44px 0 14px; scroll-margin-top: 20px; }}
.body h3 {{ font-family: {SERIF}; font-weight: 700; font-size: 20px; letter-spacing: -0.01em; margin: 26px 0 8px; }}
.body p {{ font-family: {SERIF}; font-weight: 400; font-size: 19px; line-height: 1.62; color: var(--ink); margin: 0 0 20px; letter-spacing: -0.003em; }}
.body ul, .body ol {{ margin: 0 0 22px; padding-left: 22px; }}
.body li {{ font-family: {SERIF}; font-size: 19px; line-height: 1.55; margin: 0 0 10px; }}
.body a {{ color: var(--orange-dark); font-weight: 600; text-decoration: underline; }}
.faq {{ border-top: 1px solid var(--line); margin-top: 56px; padding-top: 32px; }}
.faq h2 {{ font-family: {SERIF}; font-weight: 700; font-size: 30px; letter-spacing: -0.01em; margin: 0 0 8px; }}
.faq-eyebrow {{ font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--orange-dark); margin-bottom: 10px; }}
.faq-item {{ border-bottom: 1px solid var(--line); padding: 20px 0; }}
.faq-item h3 {{ font-family: {SERIF}; font-weight: 700; font-size: 20px; margin: 0 0 8px; letter-spacing: -0.01em; }}
.faq-item p {{ font-family: {SERIF}; font-size: 18px; line-height: 1.58; color: var(--ink-soft); margin: 0; }}
.book-strip {{ margin: 60px 0 34px; padding: 34px 30px; background: var(--ink); color: var(--cream); border-radius: 18px; display: flex; align-items: center; justify-content: space-between; gap: 26px; flex-wrap: wrap; }}
.book-strip .strip-title {{ font-family: {SERIF}; font-weight: 700; font-size: 23px; margin: 0 0 6px; max-width: none; line-height: 1.25; letter-spacing: -0.01em; color: var(--cream); }}
.book-strip .strip-title em {{ color: var(--orange); font-style: italic; }}
.book-strip p {{ margin: 0; font-size: 14.5px; color: rgba(243,232,207,0.78); max-width: 440px; }}
.book-strip a {{ background: var(--orange); color: var(--ink); padding: 14px 22px; border-radius: 999px; font-weight: 700; text-decoration: none; font-size: 14px; letter-spacing: 0.01em; white-space: nowrap; transition: transform .15s, background .15s; }}
.book-strip a:hover {{ transform: translateY(-2px); background: #ffb361; }}
.strip-actions {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.disclaimer {{ font-size: 13px; color: var(--ink-soft); line-height: 1.5; margin: 0 0 20px; opacity: 0.85; }}
.more-articles {{ border-top: 1px solid var(--line); padding-top: 26px; margin-top: 10px; }}
.more-articles .faq-eyebrow {{ margin-bottom: 14px; }}
.more-articles p {{ font-family: {SERIF}; font-size: 18px; line-height: 1.55; margin: 0 0 8px; }}
.more-articles a {{ display: block; font-family: {SERIF}; font-weight: 600; font-size: 18px; color: var(--ink); text-decoration: none; padding: 10px 0; border-bottom: 1px solid var(--line); letter-spacing: -0.01em; }}
.more-articles a:hover {{ color: var(--orange-dark); }}
footer {{ background: var(--ink); color: var(--cream); padding: 40px 0 36px; margin-top: 30px; }}
footer .wrap {{ display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; align-items: center; }}
footer .mark {{ font-family: {SERIF}; font-weight: 700; font-size: 18px; }}
footer .mark span {{ color: var(--orange); font-style: italic; font-weight: 600; }}
footer small {{ color: rgba(243,232,207,0.55); font-size: 12px; }}
h1, h2, h3 {{ text-wrap: balance; }}
p {{ text-wrap: pretty; }}
@media (max-width: 720px) {{
  .masthead {{ padding-top: 38px; }}
  .book-strip {{ padding: 26px 22px; }}
}}
@media (max-width: 480px) {{
  .wrap {{ padding: 0 16px; }}
}}
"""

# Listicle-only pieces: the quick-picks box, the table of contents, the
# comparison table, and the per-show profiles.
LISTICLE_CSS = f"""
/* Listicle (listicle_render.py) */
.picks {{ border: 1px solid var(--line); border-radius: 14px; padding: 22px 24px 8px; margin: 0 0 34px; background: rgba(255,255,255,0.28); }}
.picks-label, .toc-label {{ display: block; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--orange-dark); margin-bottom: 12px; }}
.body .picks ul {{ margin: 0 0 14px; padding-left: 22px; }}
.body .picks p {{ font-size: 17px; margin: 0 0 16px; }}
.body .picks li {{ font-size: 18px; line-height: 1.5; margin: 0 0 12px; }}
.body .picks li a {{ color: var(--ink); font-weight: 700; text-decoration: none; border-bottom: 1px solid var(--orange); }}
.badge {{ display: inline-block; font-family: "Libre Franklin", Arial, sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); background: var(--orange); border-radius: 999px; padding: 3px 9px; margin-right: 8px; vertical-align: 2px; white-space: nowrap; }}
.toc {{ border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 20px 0 10px; margin: 0 0 10px; }}
.body .toc ol {{ margin: 0; padding-left: 22px; columns: 2; column-gap: 32px; }}
.body .toc li {{ font-family: "Libre Franklin", Arial, sans-serif; font-size: 14.5px; margin: 0 0 8px; break-inside: avoid; }}
.body .toc a {{ color: var(--ink-soft); font-weight: 500; text-decoration: none; }}
.body .toc a:hover {{ color: var(--orange-dark); text-decoration: underline; }}
.table-wrap {{ overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 26px; border: 1px solid var(--line); border-radius: 12px; }}
.table-wrap table {{ border-collapse: collapse; width: 100%; min-width: 620px; font-size: 14.5px; line-height: 1.45; }}
.table-wrap thead th {{ text-align: left; font-size: 11.5px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-soft); background: rgba(236,217,168,0.55); padding: 12px 14px; }}
.table-wrap td {{ padding: 12px 14px; border-top: 1px solid var(--line); vertical-align: top; }}
.table-wrap tbody th {{ text-align: left; font-weight: 700; padding: 12px 14px; border-top: 1px solid var(--line); vertical-align: top; }}
.table-wrap tr.row-best th {{ background: rgba(216,122,44,0.10); }}
.table-wrap:focus-visible {{ outline: 2px solid var(--orange-dark); outline-offset: 2px; }}
.visually-hidden {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
.table-wrap tr.row-best td {{ background: rgba(216,122,44,0.10); }}
.profile {{ border-top: 1px solid var(--line); margin-top: 40px; }}
.body .profile h2 {{ margin-top: 6px; }}
.profile .rank {{ font-family: "Libre Franklin", Arial, sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--orange-dark); margin: 22px 0 0; }}
.facts {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 18px; margin: 0 0 20px; padding: 16px 18px; background: rgba(236,217,168,0.35); border-radius: 10px; font-size: 15px; }}
.facts dt {{ font-weight: 700; color: var(--ink-soft); }}
.facts dd {{ margin: 0; }}
.body .listen {{ font-family: "Libre Franklin", Arial, sans-serif; font-size: 14.5px; margin: -6px 0 18px; }}
.body .listen a {{ margin-right: 14px; }}
.body .sources li {{ font-family: "Libre Franklin", Arial, sans-serif; font-size: 14px; line-height: 1.5; margin: 0 0 6px; overflow-wrap: anywhere; }}
@media (max-width: 600px) {{
  .body .toc ol {{ columns: 1; }}
  .facts {{ grid-template-columns: 1fr; gap: 2px; }}
  .facts dd {{ margin-bottom: 8px; }}
}}
"""


def anchor(text: str) -> str:
    """Stable fragment id from a heading: 'My First Million' -> 'my-first-million'."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower().replace("&", " and "))
    return slug.strip("-")


def human_date(iso: str) -> str:
    year, month, day = (int(part) for part in iso.split("-"))
    return f"{MONTHS[month - 1]} {day}, {year}"


def article_path(slug: str) -> str:
    return f"/articles/{slug}"


def json_ld_script(payload) -> str:
    # "</" inside a string would close the script element early.
    text = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">{text}</script>'


# Schema.org caps nothing, but Google truncates Article.headline past this.
HEADLINE_MAX = 110


def all_shows(data: dict) -> list[dict]:
    """Page order: our show first (the disclosed pick), then the others A to Z."""
    return [data["our_show"], *data["shows"]]


def h1_text(data: dict) -> str:
    """The visible H1 as plain text. Article.headline, the breadcrumb, the
    ItemList name, og:title, related links, and llms.txt all use this same
    string (via data["headline"], which tests hold equal to it)."""
    return f"{data['h1']} {data['h1_em']}"


# Links that announce a show rather than host it; never a show's canonical url.
NON_CANONICAL_HOSTS = ("podnews.net/press-release",)


def podcast_series(show: dict) -> dict:
    """The PodcastSeries a list entry means, so search and AI engines can tell
    "Founders" or "Second Life" the podcast from anything else of that name."""
    series = show["series"]
    site = series["site"]
    if not site or any(host in site for host in NON_CANONICAL_HOSTS):
        site = series["apple"] or f"{BASE_URL}/"
    if show["name"] == SITE:
        site = f"{BASE_URL}/"
    same_as = [u for u in [series["apple"], *series.get("same_as", [])] if u and u != site]
    entity = {"@type": "PodcastSeries", "name": series["name"], "url": site}
    is_own_show = show["name"] == SITE
    if is_own_show:
        # Only our own show gets the site's @id; other shows never do.
        entity = {"@type": "PodcastSeries", "@id": SERIES_ID, "name": series["name"], "url": site}
    if same_as:
        entity["sameAs"] = same_as
    if series.get("author"):
        entity["author"] = {"@type": "Person", "name": series["author"]}
        if is_own_show:
            entity["author"] = {"@type": "Person", "@id": HOST_ID, "name": series["author"]}
    return entity


def build_structured_data(data: dict) -> tuple[list, dict]:
    """(Article + BreadcrumbList + ItemList, FAQPage)."""
    url = to_url(article_path(data["slug"]))
    headline = h1_text(data)[:HEADLINE_MAX]
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": data["og_description"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": data["published"],
        "dateModified": data["modified"],
        "author": AUTHOR,
        "publisher": {"@type": "Person", "@id": HOST_ID, "name": "Jack Pitts", "url": "https://thejackpitts.com/"},
        "image": SHOW_CARD_URL,
        "isPartOf": {"@type": "WebSite", "@id": WEBSITE_ID, "name": SITE, "url": f"{BASE_URL}/"},
    }
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE, "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Articles", "item": f"{BASE_URL}/articles"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": url},
        ],
    }
    shows = all_shows(data)
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": headline,
        # Only the first entry is a ranking (our own, disclosed pick); the rest
        # are alphabetical, so the list as a whole is not ordered by merit.
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "numberOfItems": len(shows),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": show["name"], "url": f"{url}#{anchor(show['name'])}",
             "item": podcast_series(show)}
            for i, show in enumerate(shows, start=1)
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in data["faqs"]
        ],
    }
    return [article, breadcrumbs, item_list], faq


def build_head(data: dict) -> str:
    url = to_url(article_path(data["slug"]))
    og_title = escape(data["headline"])
    og_desc = escape(data["og_description"])
    card_alt = escape(SHOW_CARD_ALT)
    graph, faq = build_structured_data(data)
    style = ARTICLE_CSS + LISTICLE_CSS + TOPNAV_CSS + FOOTER_CSS + CHROME_CSS
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#f3e8cf" />
<title>{escape(data['title_tag'])}</title>
<meta name="description" content="{escape(data['meta_description'])}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="{SITE}" />
<meta property="og:title" content="{og_title}" />
<meta property="og:description" content="{og_desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SHOW_CARD_URL}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{card_alt}" />
<meta property="article:published_time" content="{data['published']}" />
<meta property="article:modified_time" content="{data['modified']}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{og_title}" />
<meta name="twitter:description" content="{og_desc}" />
<meta name="twitter:image" content="{SHOW_CARD_URL}" />
<meta name="twitter:image:alt" content="{card_alt}" />
<link rel="icon" type="image/svg+xml" href='{FAVICON}' />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="{escape(FONTS_HREF)}" rel="stylesheet" />
{json_ld_script(graph)}
{json_ld_script(faq)}
<style>{style}</style>
</head>"""


def build_picks(data: dict) -> str:
    items = []
    for show in all_shows(data):
        # Badge before the name, so the sentence "<Name> is best for ..." reads
        # unbroken when the text is extracted.
        badge = f'<span class="badge">{escape(show["badge"])}</span> ' if show.get("badge") else ""
        sep = "" if show["pick_line"].startswith(",") else " "
        items.append(
            f'        <li>{badge}<a href="#{anchor(show["name"])}">{escape(show["name"])}</a>{sep}'
            f'{show["pick_line"]}</li>'
        )
    return (
        '    <div class="picks">\n'
        '      <span class="picks-label">TL;DR</span>\n'
        "      <ul>\n" + "\n".join(items) + "\n      </ul>\n"
        f'      <p>{data["tldr_close"]}</p>\n'
        "    </div>"
    )


def build_toc(entries: list[tuple[str, str]]) -> str:
    """entries: [(fragment id, label)]."""
    items = "\n".join(f'        <li><a href="#{fid}">{escape(label)}</a></li>' for fid, label in entries)
    return (
        '    <nav class="toc" aria-labelledby="toc-label">\n'
        '      <span class="toc-label" id="toc-label">On this page</span>\n'
        f"      <ol>\n{items}\n      </ol>\n"
        "    </nav>"
    )


def build_table(data: dict) -> str:
    columns = data["table_columns"]
    head = "".join(f'<th scope="col">{escape(c)}</th>' for c in ("Show", *columns))
    rows = []
    for i, show in enumerate(all_shows(data)):
        if len(show["table"]) != len(columns):
            raise ValueError(f"{show['name']}: {len(show['table'])} table cells, expected {len(columns)}")
        cls = ' class="row-best"' if i == 0 else ""
        name = f'<a href="#{anchor(show["name"])}">{escape(show["name"])}</a>'
        cells = "".join(f"<td>{cell}</td>" for cell in show["table"])
        rows.append(f'          <tr{cls}><th scope="row">{name}</th>{cells}</tr>')
    return (
        f'    <div class="table-wrap" role="region" tabindex="0" aria-label="{escape(data["table_heading"])}">\n'
        "      <table>\n"
        f'        <caption class="visually-hidden">{escape(data["table_heading"])}</caption>\n'
        f"        <thead><tr>{head}</tr></thead>\n"
        "        <tbody>\n" + "\n".join(rows) + "\n        </tbody>\n"
        "      </table>\n"
        "    </div>"
    )


def build_profile(show: dict, rank: int) -> str:
    # Only our disclosed pick carries a number; the others are alphabetical,
    # so numbering them would imply a ranking the page does not make.
    rank_label = "No. 1 &middot; Our pick, and our own show" if rank == 1 else "Also recommended (A to Z)"
    fid = anchor(show["name"])
    facts = "\n".join(f"        <dt>{escape(label)}</dt><dd>{value}</dd>" for label, value in show["facts"])
    sections = "\n".join(f"      <h3>{escape(heading)}</h3>\n      {body}" for heading, body in show["sections"])
    listen = ""
    if show.get("listen"):
        links = " ".join(
            f'<a href="{escape(href)}"{"" if href.startswith("/") else EXTERNAL}>{escape(label)}</a>'
            for label, href in show["listen"]
        )
        listen = f'\n      <p class="listen">{links}</p>'
    return f"""    <section class="profile" aria-labelledby="{fid}">
      <p class="rank">{rank_label}</p>
      <h2 id="{fid}">{escape(show['name'])}</h2>
      <dl class="facts">
{facts}
      </dl>{listen}
{sections}
    </section>"""


def build_faq(faqs: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'    <div class="faq-item">\n      <h3>{escape(q)}</h3>\n      <p>{escape(a)}</p>\n    </div>'
        for q, a in faqs
    )
    return (
        '  <section class="faq" aria-labelledby="faq">\n'
        '    <div class="faq-eyebrow">Common questions</div>\n'
        '    <h2 id="faq">FAQ</h2>\n'
        f"{items}\n"
        "  </section>"
    )


def build_sources(sources: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'        <li><a href="{escape(url)}" target="_blank" rel="noopener">{escape(label)}</a></li>'
        for label, url in sources
    )
    return (
        '    <section class="sources" aria-labelledby="sources">\n'
        '      <h2 id="sources">Sources</h2>\n'
        f"      <ul>\n{items}\n      </ul>\n"
        "    </section>"
    )


def build_link_list(label: str, intro: str, links: list[tuple[str, str]], aria: str, section_id: str = "") -> str:
    id_attr = f' id="{section_id}"' if section_id else ""
    intro_html = f"\n    <p>{intro}</p>" if intro else ""
    anchors = "\n".join(f'    <a href="{escape(href)}">{escape(text)}</a>' for href, text in links)
    return (
        f'  <section class="more-articles"{id_attr} aria-label="{escape(aria)}">\n'
        f'    <div class="faq-eyebrow">{escape(label)}</div>{intro_html}\n'
        f"{anchors}\n"
        "  </section>"
    )


def _prose(sections: list[tuple[str, str]]) -> str:
    return "\n".join(f'    <h2 id="{anchor(h)}">{escape(h)}</h2>\n    {body}' for h, body in sections)


def toc_entries(data: dict) -> list[tuple[str, str]]:
    labels = (
        [data["table_heading"]]
        + [h for h, _ in data["sections_before"]]
        + [s["name"] for s in all_shows(data)]
        + [h for h, _ in data["sections_after"]]
    )
    entries = [(anchor(label), label) for label in labels] + [("faq", "FAQ"), ("sources", "Sources")]
    ids = [fid for fid, _ in entries]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{data['slug']}: duplicate section anchors {ids}")
    return entries


def build_body(data: dict, related: list[tuple[str, str]]) -> str:
    profiles = "\n".join(build_profile(show, rank) for rank, show in enumerate(all_shows(data), start=1))
    published = human_date(data["published"])
    updated = ""
    if data["modified"] != data["published"]:
        updated = (f'\n    <span>Updated <time datetime="{data["modified"]}">'
                   f'{human_date(data["modified"])}</time></span>')
    episodes = build_link_list(
        "Hear it in practice",
        data["episodes_intro"],
        [(f"/episodes/{slug}", text) for slug, text in data["episodes"]] + [("/episodes", "Browse every episode")],
        "Related episodes",
        "hear-it-in-practice",
    )
    keep_reading = build_link_list("Keep reading", "", related, "More articles")
    return f"""<body>
{UNLISTED_MARKER}

{topnav_html()}

<main class="wrap">
  <div class="masthead">
    <span class="kicker">{escape(data['kicker'])}</span>
    <span>By Jack Pitts</span>
    <span><time datetime="{data['published']}">{published}</time></span>{updated}
    <span>Show details checked {escape(data['checked'])}</span>
    <span>{data['read_minutes']} min read</span>
  </div>

  <h1 class="hero-title">{escape(data['h1'])} <em>{escape(data['h1_em'])}</em></h1>

  <p class="answer">{data['answer']}</p>

  <div class="body">
{build_picks(data)}
{build_toc(toc_entries(data))}
    <h2 id="{anchor(data['table_heading'])}">{escape(data['table_heading'])}</h2>
    {data['table_intro']}
{build_table(data)}
{_prose(data['sections_before'])}
{profiles}
{_prose(data['sections_after'])}
  </div>

  <aside class="book-strip" aria-labelledby="listen-cta">
    <div>
      <p class="strip-title" id="listen-cta">Listen to <em>{SITE}</em>.</p>
      <p>Owners of real companies telling the whole story of how they built them, about an hour an episode.</p>
    </div>
    <div class="strip-actions">
      <a href="{SHOW_APPLE}" target="_blank" rel="noopener">Apple Podcasts</a>
      <a href="{SHOW_SPOTIFY}" target="_blank" rel="noopener">Spotify</a>
      <a href="{SHOW_YOUTUBE}" target="_blank" rel="noopener">YouTube</a>
    </div>
  </aside>

{build_faq(data['faqs'])}

  <div class="body">
{build_sources(data['sources'])}
  </div>

  <p class="disclaimer">This article is for general informational purposes only. {SITE} publishes this comparison and is one of the shows listed, which is disclosed above. Descriptions of other shows rely on their public materials and podcast listings as of {data['checked']} and may change. No show paid to be included, none of the other shows was contacted, and none reviewed this article.</p>

{episodes}

{keep_reading}
</main>

{footer_html()}

</body>
</html>
"""


def render(data: dict, related: list[tuple[str, str]]) -> str:
    """The finished page for one listicle. `related` is [(href, title)]."""
    return build_head(data) + "\n" + build_body(data, related)
