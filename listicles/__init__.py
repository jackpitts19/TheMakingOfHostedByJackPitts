"""
Content for the podcast listicles in articles/.

Each module in this package exposes one `LISTICLE` dict, which
listicle_render.py turns into articles/<slug>.html. ALL lists every
listicle; generate_listicles.py renders each one and links them together.

Field reference (strings marked HTML are inserted as-is, so escape `&`):
  slug, title_tag, meta_description, headline, og_description
  published, modified        ISO dates, YYYY-MM-DD
  checked                    when the show facts were last verified ("November 2026")
  kicker, read_minutes, h1, h1_em   headline must equal f"{h1} {h1_em}" (tests check it)
  answer                     HTML, the boxed direct answer under the H1
  table_heading, table_intro (HTML), table_columns
  our_show, shows            dicts built by common.our_show() / common.other_show():
                             name, badge, pick_line (HTML),
                             table (HTML cells), facts [(label, HTML)],
                             listen [(label, url)], sections [(heading, HTML)]
  sections_before, sections_after   [(heading, HTML)]
  faqs                       [(question, plain-text answer)], mirrored into FAQPage JSON-LD
  sources                    [(label, url)]
  episodes_intro, episodes   [(episode slug, link text)]
"""

from listicles import (
    business,
    buying_selling,
    entrepreneurship,
    how_i_built_this,
    leadership,
    small_business,
    startup,
    storytelling,
)

ALL = (
    entrepreneurship.LISTICLE,
    how_i_built_this.LISTICLE,
    small_business.LISTICLE,
    storytelling.LISTICLE,
    business.LISTICLE,
    startup.LISTICLE,
    buying_selling.LISTICLE,
    leadership.LISTICLE,
)
