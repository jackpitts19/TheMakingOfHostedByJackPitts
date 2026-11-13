"""
Verified facts and write-ups for the other shows the listicles compare.

One entry per show, shared by every list it appears on, so a correction is
made once. An entry holds only facts: name, links, the facts box, and a cited
overview. Each list supplies its own judgment of the show for its reader
(strengths, considerations, why it was included), plus its pick line and
table cells, through listicles.common.other_show(**SHOW, ...). That keeps the
lists from repeating each other word for word.

Like the Salt Creek Advisory comparisons, factual claims are cited inline:
the overview links the claim to the page it came from, and the same pages
appear under each list's Sources. Facts were checked in November 2026; only
claims that could be confirmed are stated. Re-check before changing `modified`.
"""


def cite(text: str, url: str) -> str:
    """An inline citation link, styled the same as the Salt Creek guides."""
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


ACQUIRED_URL = "https://www.acquired.fm/"
BUSINESS_WARS_URL = "https://podcasts.apple.com/us/podcast/business-wars/id1335814741"
DOAC_URL = "https://podcasts.apple.com/us/podcast/the-diary-of-a-ceo-with-steven-bartlett/id1291423644"
FOUNDERS_URL = "https://www.founderspodcast.com/"
FOUNDERS_FEED_URL = "https://feeds.megaphone.fm/DSLLC6297708582"
SENRA_SITE_URL = "https://www.davidsenra.com/"
SENRA_TBPN_URL = "https://tbpn.substack.com/p/david-senra-on-why-hes-launching"
FORTUNE_SENRA_URL = ("https://fortune.com/2026/07/05/how-david-senra-built-founders-podcast-powerful-ceos-"
                     "spotify-bezos-coinbase-ramp-tbpn/")
HIBT_PRESS_URL = "https://podnews.net/press-release/how-i-built-this-vox"
HIBT_APPLE_URL = "https://podcasts.apple.com/us/podcast/how-i-built-this-with-guy-raz/id1150510297"
HIBT_FEED_URL = "https://feeds.megaphone.fm/VMP2035168248"
HIBT_WONDERY_URL = ("https://www.npr.org/about-npr/1079830094/"
                    "wondery-and-npr-announce-a-licensing-agreement-for-how-i-built-this-with-guy-raz")
HIBT_WRAP_URL = ("https://www.thewrap.com/industry-news/tech/how-i-built-this-leaves-npr-for-vox-media-"
                 "guy-raz-takes-ownership/")
MOS_URL = "https://mastersofscale.com/"
MOS_FEED_URL = "https://rss.art19.com/masters-of-scale"
MIXERGY_URL = "https://mixergy.com/"
MFM_URL = "https://www.mfmpod.com/"
FERRISS_URL = "https://tim.blog/podcast/"
MBA_URL = "https://100mba.net/"
MBA_FEED_URL = "https://feeds.simplecast.com/equXS9ic"
ACQ_MINDS_URL = "https://podcasts.apple.com/us/podcast/acquiring-minds/id1569715379"
ACQ_ANON_URL = "https://podnews.net/podcast/ia89b"
BTS_URL = "https://builttosell.libsyn.com/"
SIDE_HUSTLE_URL = "https://podcasts.apple.com/us/podcast/the-side-hustle-show/id655135292"
HBR_URL = "https://hbr.org/podcasts/ideacast"
HBR_CHENAULT_URL = "https://hbr.org/podcast/2026/10/staying-principled-in-a-time-of-uncertainty"
JOURNAL_APPLE_URL = "https://podcasts.apple.com/us/podcast/the-journal/id1469394914"
JOURNAL_FEED_URL = "https://video-api.shdsvc.dowjones.io/api/podcasts/the%20journal/feed"
JOURNAL_LINEBAUGH_URL = "https://www.audioscrape.com/podcast/the-journal/episode/arrivederci-donatella-versace"
JOURNAL_2019_URL = "https://talkingbiznews.com/they-talk-biz-news/wsj-names-linebaugh-knutson-co-hosts-of-new-podcast/"
PLANET_MONEY_FEED_URL = "https://feeds.npr.org/510289/podcast.xml"
PLANET_MONEY_APPLE_URL = "https://podcasts.apple.com/us/podcast/planet-money/id290783428"
INDICATOR_FEED_URL = "https://feeds.npr.org/510325/podcast.xml"

# (label, url) for each list's Sources section, in "Publisher: Page" form.
SOURCE_LABELS = {
    ACQUIRED_URL: "Acquired: Official Site and Episode List",
    BUSINESS_WARS_URL: "Apple Podcasts: Business Wars",
    DOAC_URL: "Apple Podcasts: The Diary of a CEO with Steven Bartlett",
    FOUNDERS_URL: "Founders Podcast: Official Site",
    FOUNDERS_FEED_URL: "Megaphone: Founders (podcast feed)",
    SENRA_SITE_URL: "David Senra: Official Site",
    SENRA_TBPN_URL: "TBPN: David Senra on Why He Is Launching an Interview Show",
    FORTUNE_SENRA_URL: "Fortune: How David Senra Built the Founders Podcast (July 2026)",
    HIBT_PRESS_URL: "Podnews: How I Built This Partners with Vox Media (September 2026)",
    HIBT_WRAP_URL: "TheWrap: How I Built This Leaves NPR for Vox Media (September 2026)",
    HIBT_APPLE_URL: "Apple Podcasts: How I Built This with Guy Raz",
    HIBT_FEED_URL: "Vox Media Podcast Network: How I Built This (podcast feed)",
    HIBT_WONDERY_URL: "NPR: Wondery and NPR Announce a Licensing Agreement for How I Built This (2022)",
    MOS_URL: "Masters of Scale: Official Site",
    MOS_FEED_URL: "ART19: Masters of Scale (podcast feed)",
    MIXERGY_URL: "Mixergy: Official Site",
    MFM_URL: "My First Million: Official Site",
    FERRISS_URL: "Tim Ferriss: The Tim Ferriss Show",
    MBA_URL: "The $100 MBA Show: Official Site",
    MBA_FEED_URL: "Simplecast: The $100 MBA Show (podcast feed)",
    ACQ_MINDS_URL: "Apple Podcasts: Acquiring Minds",
    ACQ_ANON_URL: "Podnews: Acquisitions Anonymous",
    BTS_URL: "Built to Sell Radio: Episode Archive",
    SIDE_HUSTLE_URL: "Apple Podcasts: The Side Hustle Show",
    HBR_URL: "Harvard Business Review: HBR IdeaCast",
    HBR_CHENAULT_URL: "Harvard Business Review: Staying Principled in a Time of Uncertainty (October 2026)",
    JOURNAL_FEED_URL: "The Wall Street Journal: The Journal. (podcast feed)",
    JOURNAL_2019_URL: "Talking Biz News: WSJ Names Linebaugh, Knutson Co-Hosts of New Podcast (2019)",
    JOURNAL_LINEBAUGH_URL: "Audioscrape: The Journal., Arrivederci Donatella Versace (transcript, March 2025)",
    PLANET_MONEY_FEED_URL: "NPR: Planet Money (podcast feed)",
    PLANET_MONEY_APPLE_URL: "Apple Podcasts: Planet Money",
    INDICATOR_FEED_URL: "NPR: The Indicator from Planet Money (podcast feed)",
}


def sources_for(*urls: str) -> list[tuple[str, str]]:
    return [(SOURCE_LABELS[url], url) for url in urls]


ACQUIRED = dict(
    name="Acquired",
    site=ACQUIRED_URL,
    apple="https://podcasts.apple.com/us/podcast/acquired/id1050462261",
    facts=[
        ("Hosts", "Ben Gilbert and David Rosenthal"),
        ("Format", "Long-form company histories, often several hours"),
        ("Owner", "Independent (ACQ, LLC)"),
        ("Focus", "How great companies were built, told end to end"),
    ],
    overview="Two hosts research one company in depth and tell its full story, from founding through the "
             "decisions that made it. Recent subjects on the "
             + cite("show's episode list", ACQUIRED_URL) + " include Home Depot and Seinfeld.",
)

BUSINESS_WARS = dict(
    name="Business Wars",
    site=BUSINESS_WARS_URL,
    facts=[
        ("Host", "David Brown"),
        ("Format", "Dramatized narrative series, about 40 minutes an episode"),
        ("Network", "Created by Wondery; now listed as an Audible Original"),
        ("Focus", "Rivalries between companies and the people who ran them"),
    ],
    overview="Each multi-part season dramatizes a fight between competitors, such as rival brands or whole "
             "industries, with scripted narration and sound design. Its "
             + cite("current podcast listing", BUSINESS_WARS_URL)
             + " carries it as an Audible Original and shows new episodes in November 2026.",
)

DIARY_OF_A_CEO = dict(
    name="The Diary of a CEO",
    series_name="The Diary of a CEO with Steven Bartlett",
    site=DOAC_URL,
    facts=[
        ("Host", "Steven Bartlett"),
        ("Format", "Long-form interview, usually 90 minutes to two hours"),
        ("Focus", "Business, health, psychology, and personal development"),
    ],
    overview="Steven Bartlett interviews a wide range of guests, from founders and investors to doctors and "
             "psychologists, in long, personal conversations. The "
             + cite("show's podcast listing", DOAC_URL) + " shows new episodes in November 2026.",
)

DAVID_SENRA = dict(
    name="David Senra (interview show)",
    series_name="David Senra",
    site=SENRA_SITE_URL,
    apple="https://podcasts.apple.com/us/podcast/david-senra/id1836497887",
    facts=[
        ("Host", "David Senra"),
        ("Format", "Long-form interviews with living founders"),
        ("Since", "September 2025 (first guest: Daniel Ek of Spotify)"),
        ("Focus", "How great founders think and operate"),
    ],
    overview="The interview show from the host of Founders, launched in September 2025 as a separate feed "
             "titled simply David Senra. " + cite("TBPN reported", SENRA_TBPN_URL)
             + " that Senra started it to hold long conversations with living founders, and that the first "
             "episode featured Spotify's Daniel Ek.",
)

FOUNDERS = dict(
    name="Founders",
    site=FOUNDERS_URL,
    apple="https://podcasts.apple.com/us/podcast/founders/id1141877104",
    facts=[
        ("Host", "David Senra"),
        ("Format", "Solo episodes, each built on one founder's biography or memoir"),
        ("Since", "2016, independent with no corporate parent"),
        ("Focus", "Lessons from history's great entrepreneurs"),
    ],
    overview="David Senra reads a biography, autobiography, or memoir of an entrepreneur and walks through "
             "what he learned from it. The " + cite("show's feed", FOUNDERS_FEED_URL)
             + " runs to 439 numbered episodes, the latest released November 4, 2026, and " + cite("Fortune", FORTUNE_SENRA_URL)
             + " reports that Senra runs it independently, without investors or a corporate parent.",
)

HOW_I_BUILT_THIS = dict(
    name="How I Built This",
    series_name="How I Built This with Guy Raz",
    site=HIBT_PRESS_URL,
    apple=HIBT_APPLE_URL,
    facts=[
        ("Host", "Guy Raz"),
        ("Format", "Interviews with founders about their company's origin story"),
        ("Owner", "Moving from NPR to Guy Raz, announced September 2026, with Vox Media as partner"),
        ("Focus", "Founder origin stories, from consumer brands to tech"),
    ],
    overview="For about ten years, Guy Raz has asked founders to tell the story of their company from the "
             "beginning. NPR owned the show and had " + cite("licensed it to Amazon's Wondery", HIBT_WONDERY_URL)
             + " since 2022. In September 2026, " + cite("TheWrap reported", HIBT_WRAP_URL)
             + " that Raz is acquiring full ownership of the show from NPR, and the "
             + cite("announcement", HIBT_PRESS_URL)
             + " named Vox Media as partner for sales, marketing, distribution, and business operations, with "
             "video episodes on YouTube and twice as many episodes promised for early 2027. The "
             + cite("show's feed", HIBT_FEED_URL) + " now names its publisher as Guy Raz | Vox Media.",
)

MASTERS_OF_SCALE = dict(
    name="Masters of Scale",
    site=MOS_URL,
    apple="https://podcasts.apple.com/us/podcast/masters-of-scale/id1227971746",
    facts=[
        ("Hosts", "Mostly Jeff Berman, with founding host Reid Hoffman, co-founder of LinkedIn, on some episodes"),
        ("Format", "Interviews with CEOs and founders, most about 25 to 35 minutes, two or three a week"),
        ("Network", "WaitWhat"),
        ("Focus", "How companies and leaders grow"),
    ],
    overview="Short interviews with CEOs and founders about how they grew their companies, some recorded live "
             "at the Masters of Scale Summit. The " + cite("show's feed", MOS_FEED_URL)
             + " bills Reid Hoffman as founding host among a set of hosts, credits Jeff Berman as host on many "
             "recent interviews, and posts on Tuesdays and Thursdays, plus some Saturdays. The "
             + cite("show's site", MOS_URL) + " lists Rapid Response and Pioneers of AI as separate shows.",
)

MIXERGY = dict(
    name="Mixergy",
    site=MIXERGY_URL,
    facts=[
        ("Host", "Andrew Warner"),
        ("Format", "Interviews with founders about how they built their companies"),
        ("Catalog", "More than 2,300 episodes, archived on mixergy.com"),
        ("Focus", "Startups and internet businesses, many bootstrapped"),
    ],
    overview="Andrew Warner presses each guest on how the business actually started and grew. "
             + cite("Mixergy's site", MIXERGY_URL)
             + " says it has interviewed more than 1,500 entrepreneurs, with a new episode in October 2026.",
)

MY_FIRST_MILLION = dict(
    name="My First Million",
    site=MFM_URL,
    apple="https://podcasts.apple.com/us/podcast/my-first-million/id1469759170",
    facts=[
        ("Hosts", "Shaan Puri and Sam Parr"),
        ("Format", "Co-host conversation about business ideas, plus guest interviews"),
        ("Catalog", "More than 880 numbered episodes, new ones every week"),
        ("Focus", "Business ideas, trends, and how people made money"),
    ],
    overview="Two founders brainstorm business ideas, break down how other people made money, and bring on "
             "guests who have built and sold companies. The " + cite("show's site", MFM_URL)
             + " lists more than 880 numbered episodes, with new ones every week.",
)

TIM_FERRISS = dict(
    name="The Tim Ferriss Show",
    site=FERRISS_URL,
    apple="https://podcasts.apple.com/us/podcast/the-tim-ferriss-show/id863897795",
    facts=[
        ("Host", "Tim Ferriss"),
        ("Format", "Long-form interviews and solo Q&amp;A episodes"),
        ("Catalog", "Close to 900 episodes"),
        ("Focus", "The habits and tools of top performers in many fields"),
    ],
    overview="Tim Ferriss interviews entrepreneurs, investors, athletes, writers, and scientists about how they "
             "work. His " + cite("episode archive", FERRISS_URL) + " is close to 900 episodes deep.",
)

HUNDRED_MBA = dict(
    name="The $100 MBA Show",
    site=MBA_URL,
    apple="https://podcasts.apple.com/us/podcast/the-%24100-mba-show/id906218859",
    facts=[
        ("Host", "Omar Zenhom, co-founder of WebinarNinja (acquired by ProProfs in 2024)"),
        ("Format", "Short lessons, about 22 minutes (2026 median), most 18 to 28, three a week"),
        ("Since", "August 2014"),
        ("Focus", "Practical lessons for small business owners"),
    ],
    overview="Business lessons and listener questions on marketing, pricing, hiring, and money. The "
             + cite("show's site", MBA_URL) + " dates the podcast to 2014 (the $100 MBA business to 2013), and "
             "its " + cite("feed", MBA_FEED_URL) + " shows three new episodes a week in 2026, with a typical "
             "length of about 22 minutes.",
)

ACQUIRING_MINDS = dict(
    name="Acquiring Minds",
    site=ACQ_MINDS_URL,
    facts=[
        ("Host", "Will Smith"),
        ("Format", "Long-form interviews with people who bought a small business"),
        ("Focus", "Buying and running an existing business"),
    ],
    overview="Will Smith interviews buyers of small and mid-sized businesses about how they found the company, "
             "financed it, and ran it after closing. Its " + cite("podcast listing", ACQ_MINDS_URL)
             + " shows new episodes in November 2026.",
)

ACQUISITIONS_ANONYMOUS = dict(
    name="Acquisitions Anonymous",
    site=ACQ_ANON_URL,
    apple="https://podcasts.apple.com/us/podcast/acquisitions-anonymous-1-for-business-buying-selling/id1533153678",
    facts=[
        ("Hosts", "Michael Girdley, Mills Snell, Bill D'Alessandro, and Heather Endresen"),
        ("Format", "Panel reviews of real businesses for sale, about 30 to 45 minutes, twice a week"),
        ("Focus", "Buying, selling, and operating small businesses"),
    ],
    overview="The hosts pick a real business listing, from a car wash to a software company, and debate "
             "whether they would buy it and at what price. Its " + cite("Podnews listing", ACQ_ANON_URL)
             + " describes it as a show about business buying, selling, and operating, with new episodes in "
             "November 2026.",
)

BUILT_TO_SELL = dict(
    name="Built to Sell Radio",
    site=BTS_URL,
    apple="https://podcasts.apple.com/us/podcast/built-to-sell-radio/id1018988393",
    facts=[
        ("Host", "John Warrillow, author of Built to Sell"),
        ("Format", "Weekly interviews with owners who sold their companies"),
        ("Catalog", "More than 570 episodes"),
        ("Focus", "Building a company buyers want, and the sale itself"),
    ],
    overview="John Warrillow interviews owners who have sold a business about the price, the terms, and what "
             "they would do differently. The " + cite("episode archive", BTS_URL)
             + " passed 570 episodes in November 2026.",
)

SIDE_HUSTLE = dict(
    name="The Side Hustle Show",
    site=SIDE_HUSTLE_URL,
    facts=[
        ("Host", "Nick Loper"),
        ("Format", "Tactical interviews with people building businesses on the side"),
        ("Catalog", "More than 760 episodes since May 2013"),
        ("Focus", "Starting a small business while keeping a job"),
    ],
    overview="Nick Loper interviews people who built side businesses, from online stores to local services, "
             "and asks exactly how they got their first customers. Its "
             + cite("podcast listing", SIDE_HUSTLE_URL) + " shows a new episode in November 2026.",
)

HBR_IDEACAST = dict(
    name="HBR IdeaCast",
    site=HBR_URL,
    apple="https://podcasts.apple.com/us/podcast/hbr-ideacast/id152022135",
    facts=[
        ("Hosts", "Alison Beard and Adi Ignatius"),
        ("Format", "Weekly interview on Tuesdays, about 25 to 35 minutes"),
        ("Publisher", "Harvard Business Review"),
        ("Focus", "Management and leadership ideas from researchers and executives"),
    ],
    overview="Each week one researcher or executive explains a management idea and what leaders should do "
             "about it. " + cite("HBR lists", HBR_URL) + " Alison Beard, an executive editor and a former "
             "Financial Times reporter and editor, and Adi Ignatius, who served as its editor in chief for 16 "
             "years, as the hosts. A " + cite("late October 2026 episode", HBR_CHENAULT_URL)
             + " featured Kenneth Chenault, the former American Express CEO.",
)

THE_JOURNAL = dict(
    name="The Journal.",
    site="https://www.wsj.com/podcasts/the-journal",
    apple=JOURNAL_APPLE_URL,
    facts=[
        ("Hosts", "Ryan Knutson and Jessica Mendoza"),
        ("Format", "Narrative news episodes, about 18 to 30 minutes, every weekday"),
        ("Network", "The Wall Street Journal and Spotify Studios"),
        ("Focus", "One story about money, business, or power per episode"),
    ],
    overview="A host walks through one story with the Wall Street Journal reporter who covered it. The "
             + cite("show's feed", JOURNAL_FEED_URL)
             + " describes it as \"the most important stories about money, business and power,\" hosted by Ryan "
             "Knutson and Jessica Mendoza and co-produced by Spotify and The Wall Street Journal. Founding "
             "co-host Kate Linebaugh, " + cite("named co-host in 2019", JOURNAL_2019_URL)
             + ", said on a " + cite("March 2025 episode", JOURNAL_LINEBAUGH_URL)
             + " that she was leaving the show to become the paper's corporate news editor.",
)

PLANET_MONEY = dict(
    name="Planet Money",
    site="https://www.npr.org/podcasts/510289/planet-money",
    apple=PLANET_MONEY_APPLE_URL,
    facts=[
        ("Hosts", "A rotating team of NPR hosts and reporters"),
        ("Format", "Reported narrative episodes, about 20 to 35 minutes, about two a week"),
        ("Network", "NPR"),
        ("Focus", "Economics told through stories about businesses, industries, and money"),
    ],
    overview="The " + cite("show's feed", PLANET_MONEY_FEED_URL)
             + " pitches it this way: \"Give us any topic and we can tie it back to the economy.\" Episodes are "
             "reported stories from a rotating team of hosts. The "
             + cite("November 11, 2026 episode", PLANET_MONEY_APPLE_URL)
             + ", hosted by Amanda Aronczyk and Jeff Guo, traced how bodegas led to a wave of Yemeni "
             "coffeehouses. NPR also publishes a short companion, "
             + cite("The Indicator from Planet Money", INDICATOR_FEED_URL)
             + ", which runs Monday through Friday in ten minutes or less.",
)
