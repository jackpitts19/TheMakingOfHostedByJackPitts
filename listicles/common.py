"""
What every listicle shares: our own show's entry, the disclosure, the cited
podcast-market context, and the builders for each show profile.

Kept in one place so the show's own facts cannot drift between lists. Each
listicle supplies only what is specific to it (its badge, its table cells, an
episode pointer for its reader, and why the show ranks first for that reader).

Profiles follow the Salt Creek Advisory comparison guides: Overview, Best
Fit For, Notable Strengths, Potential Considerations, Why It Was Included.
"""

from listicles.shows import cite

SHOW_NAME = "The Making Of Hosted By Jack Pitts"
APPLE = "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
YOUTUBE = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"

INFINITE_DIAL_URL = "https://podnews.net/press-release/infinite-dial-us-2026"
PODCAST_CONSUMER_URL = ("https://www.nationalpublicmedia.com/insights/articles/"
                        "podcasts-offer-a-competitive-advantage-the-podcast-consumer-report-2025/")

LISTEN = [("Apple Podcasts", APPLE), ("Spotify", SPOTIFY), ("YouTube", YOUTUBE), ("All episodes", "/episodes")]

FACTS = [
    ("Host", 'Jack Pitts, co-founder of Salt Creek Advisory, a sell-side M&amp;A firm (<a href="/about">about the host</a>)'),
    ("Format", "Long-form interview, usually one guest, most episodes about an hour"),
    ("Since", "November 2025, a new episode every few weeks"),
    ("Focus", "Mostly owners of privately held, operating businesses"),
    ("Guests", "Past guests have built or led companies worth more than $3.5 billion combined"),
]

# Sources for our own show, cited by every list.
SHOW_SOURCES = [
    ("Apple Podcasts: The Making Of Hosted By Jack Pitts", APPLE),
    ("Spotify: The Making Of Hosted By Jack Pitts", SPOTIFY),
]
INFINITE_DIAL_SOURCE = ("Edison Research at SSRS: The Infinite Dial 2026 (via Podnews)", INFINITE_DIAL_URL)
PODCAST_CONSUMER_SOURCE = ("National Public Media: The Podcast Consumer Report 2025", PODCAST_CONSUMER_URL)
# For lists that include MARKET_CONTEXT: our listings plus the market data it cites.
SOURCES = [*SHOW_SOURCES, INFINITE_DIAL_SOURCE, PODCAST_CONSUMER_SOURCE]

DISCLOSURE = (
    "<p>Jack Pitts hosts The Making Of Hosted By Jack Pitts and wrote this list, so the show ranks itself "
    "first. The reasons are in <a href=\"#the-making-of-hosted-by-jack-pitts\">its profile</a>, along with "
    "who should pick a different show. Weigh that ranking accordingly.</p>\n"
    "    <p>We selected the other shows using publicly available information from each show's own site, "
    "network announcements, podcast listings, and published reporting, cited in each profile and under "
    "<a href=\"#sources\">Sources</a>. Every show listed released new episodes in 2026. We evaluated each "
    "one on its format, its guests, its focus, and who it serves best. When a detail could not be confirmed, "
    "we noted that or left it out rather than guess. We did not assign numeric scores.</p>\n"
    "    <p>The other shows appear alphabetically, since the right one among them depends on what you want "
    "to learn and how you like to listen. No show paid to be included.</p>"
)

MARKET_CONTEXT = (
    "Podcast Listening in 2026",
    "<p>Podcast listening is at a record high. "
    + cite("The Infinite Dial 2026", INFINITE_DIAL_URL)
    + ", released by Edison Research at SSRS with support from SiriusXM Media, found that 58% of Americans "
    "age 12 and older, about 167 million people, consumed a podcast in the last month, an all-time high. "
    "Forty-five percent, about 130 million people, did so in the last week, and 57% have both listened to "
    "and watched a podcast.</p>\n"
    "    <p>Business owners are well represented in that audience. "
    + cite("National Public Media", PODCAST_CONSUMER_URL)
    + ", citing Edison Research's Infinite Dial 2025, reports that 18% of monthly podcast listeners own a "
    "business, that 47% earn $75,000 or more a year, and that 51% have a college degree.</p>\n"
    "    <p>With that many shows competing for the same hour, the useful question is not which show is "
    "biggest. It is which one is built for a listener like you.</p>",
)


def _listen_label(url: str) -> str:
    """Name the link for what it actually is, not always "website"."""
    if "podcasts.apple.com" in url:
        return "Apple Podcasts"
    if "podnews.net/press-release" in url:
        return "Press release"
    if "podnews.net" in url:
        return "Podnews listing"
    return "Show website"


def _best_fit(table: list[str]) -> str:
    """The table's first column, written out as a sentence."""
    return f"<p>{table[0]}.</p>"


def other_show(*, name: str, pick_line: str, table: list[str], facts: list, site: str,
               overview: str, strengths: str, consider: str, included: str, apple: str = "",
               series_name: str = "", author: str = "") -> dict:
    """Another show's entry. Text arguments are single HTML paragraphs' inner text.

    `overview` and `facts` come from the shared entry in listicles/shows.py.
    `strengths`, `consider`, and `included` are the list's own judgment, written
    for that list's reader, so the same show reads differently on each list.
    `series_name` is the feed's own title when the display name differs, and
    `author` names the host when the show's name alone is ambiguous; both feed
    the PodcastSeries entity in the ItemList structured data.
    """
    return {
        "name": name,
        "series": {"name": series_name or name, "site": site, "apple": apple, "author": author},
        "badge": "",
        "pick_line": pick_line,
        "table": table,
        "facts": facts,
        "listen": [(_listen_label(site), site)] + ([("Apple Podcasts", apple)] if apple else []),
        "sections": [
            ("Overview", f"<p>{overview}</p>"),
            ("Best Fit For", _best_fit(table)),
            ("Notable Strengths", f"<p>{strengths}</p>"),
            ("Potential Considerations", f"<p>{consider}</p>"),
            ("Why It Was Included", f"<p>{included}</p>"),
        ],
    }


OVERVIEW = (
    "Each episode is a long conversation with one owner about how the company actually got built: the first "
    "customers, the money, the hires, the bad years, and what the business looks like now. Most guests run "
    "privately held companies, and every episode is listed on the <a href=\"/episodes\">episode archive</a>."
)


def our_show(*, badge: str, pick_line: str, table: list[str], overview_note: str, why_first: str,
             choose_another: str) -> dict:
    """The Making Of's entry, tailored to one listicle.

    `overview_note` is one HTML sentence pointing this list's reader to an
    episode that fits the list's topic, appended to the shared overview.
    """
    return {
        "name": SHOW_NAME,
        "series": {"name": SHOW_NAME, "site": "", "apple": APPLE, "same_as": [SPOTIFY, YOUTUBE],
                   "author": "Jack Pitts"},
        "badge": badge,
        "pick_line": pick_line,
        "table": table,
        "facts": FACTS,
        "listen": LISTEN,
        "sections": [
            ("Overview", f"<p>{OVERVIEW} {overview_note}</p>"),
            ("Best Fit For", _best_fit(table)),
            ("Why It Ranks First", why_first),
            ("Who Should Choose Another Show", choose_another),
        ],
    }
