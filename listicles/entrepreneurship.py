"""Best Entrepreneurship Podcasts in 2026: our disclosed pick, then seven more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, SHOW_SOURCES, other_show, our_show
from listicles.shows import cite

# Pages cited only by this list. Facts were checked November 12, 2026.
OUR_FEED_URL = "https://api.riverside.fm/hosting/wMWn2YqB.rss"
BFS_CSV_URL = "https://www.census.gov/econ/bfs/csv/bfs_monthly.csv"
BFS_RELEASE_URL = "https://www.census.gov/econ/bfs/current/index.html"
KAUFFMAN_URL = "https://indicators.kauffman.org/report/early-stage-entrepreneurship-national-2025"
SBA_FAQ_URL = "https://advocacy.sba.gov/2026/02/03/frequently-asked-questions-about-small-business-2026/"
BUSINESS_LISTENER_URL = ("https://soundsprofitable.com/wp-content/uploads/2025/01/"
                         "The-Business-Podcast-Consumer-Downloadable-Report.pdf")
PEW_URL = "https://www.pewresearch.org/journalism/fact-sheet/podcasts-and-news-fact-sheet/"
ACQUIRED_FEED_URL = "https://feeds.transistor.fm/acquired"
DOAC_FEED_URL = "https://rss2.flightcast.com/xmsftuzjjykcmqwolaqn6mdn"
MOS_FEED_URL = "https://rss.art19.com/masters-of-scale"
MFM_FEED_URL = "https://feeds.megaphone.fm/HS2300184645"
FERRISS_FEED_URL = "https://rss.art19.com/tim-ferriss-show"
FOUNDERS_FEED_URL = "https://feeds.megaphone.fm/DSLLC6297708582"
MBA_FEED_URL = "https://feeds.simplecast.com/equXS9ic"
EDISON_TOP50_URL = "https://podnews.net/press-release/edison-top-50-podcasts-us-q226"
EOFIRE_FEED_URL = "https://rss.libsyn.com/shows/37432/destinations/100507.xml"
GARYVEE_FEED_URL = "https://anchor.fm/s/f39a864/podcast/rss"
GARYVEE_APPLE_URL = "https://podcasts.apple.com/us/podcast/the-garyvee-audio-experience/id928159684"

# Sibling lists this one points readers to.
SMALL_BUSINESS_LIST = "/articles/best-small-business-podcasts-2026"
HIBT_ALTERNATIVES_LIST = "/articles/podcasts-like-how-i-built-this-2026"

# Shared entries, with this list's corrections and checked figures in the facts box.
ACQUIRED = {
    **shows.ACQUIRED,
    "facts": [
        ("Hosts", "Ben Gilbert and David Rosenthal"),
        ("Format", "Long-form company histories; the median 2026 episode runs about four hours"),
        ("Pace", "About one episode a month (10 so far in 2026)"),
        ("Since", "October 2015"),
        ("Owner", "Independent (ACQ, LLC)"),
    ],
}

DIARY_OF_A_CEO = {
    **shows.DIARY_OF_A_CEO,
    "facts": [
        ("Host", "Steven Bartlett, entrepreneur and investor"),
        ("Format", "Long-form interview, usually 90 minutes to two hours, several a week"),
        ("Since", "September 2017; 915 episodes on Apple Podcasts"),
        ("Focus", "Business, health, psychology, and personal development"),
    ],
}

FOUNDERS = {
    **shows.FOUNDERS,
    "facts": [
        ("Host", "David Senra"),
        ("Format", "Solo episodes, each built on one founder's biography or memoir"),
        ("Catalog", "439 numbered episodes, the latest on November 4, 2026 (464 feed items with bonus episodes)"),
        ("Since", "September 2016, independent with no corporate parent"),
    ],
}

HOW_I_BUILT_THIS = {
    **shows.HOW_I_BUILT_THIS,
    "facts": [
        ("Host", "Guy Raz"),
        ("Format", "Interviews with founders about their company's origin story"),
        ("Catalog", "More than 700 episodes since 2016"),
        ("Owner", "Moving from NPR to Guy Raz, announced September 2026, with Vox Media as partner"),
    ],
}

MASTERS_OF_SCALE = {
    **shows.MASTERS_OF_SCALE,
    "facts": [
        ("Hosts", "Mostly Jeff Berman, with founding host Reid Hoffman, co-founder of LinkedIn, on some episodes"),
        ("Format", "Interviews with CEOs and founders, about 25 to 35 minutes, two or three a week"),
        ("Network", "WaitWhat"),
        ("Since", "2017"),
    ],
    "overview": "Short interviews with CEOs and founders about growing a company, many of the latest recorded "
                "live at the Masters of Scale Summit. The " + cite("show's feed", MOS_FEED_URL)
                + " names Reid Hoffman as founding host among a set of hosts. Recent episodes are led mostly by "
                "Jeff Berman, with Hoffman on some; Berman's conversation with Walmart CEO John Furner, released November "
                "12, 2026, was recorded live at the Summit in San Francisco in October. The " + cite("show's site", shows.MOS_URL)
                + " lists Rapid Response and Pioneers of AI as separate feeds.",
}

MY_FIRST_MILLION = {
    **shows.MY_FIRST_MILLION,
    "facts": [
        ("Hosts", "Shaan Puri and Sam Parr"),
        ("Format", "Co-host conversation about business ideas, plus guest interviews, about two a week"),
        ("Catalog", "920 episodes in its feed, numbered through 881 as of November 11, 2026"),
        ("Network", "HubSpot Media"),
    ],
}

TIM_FERRISS = {
    **shows.TIM_FERRISS,
    "facts": [
        ("Host", "Tim Ferriss"),
        ("Format", "Long-form interviews and solo Q&amp;A episodes, the median 2026 episode about 90 minutes"),
        ("Catalog", "889 numbered episodes as of November 11, 2026"),
        ("Since", "April 2014"),
    ],
}

LISTICLE = dict(
    slug="best-entrepreneurship-podcasts-2026",
    title_tag="Best Entrepreneurship Podcasts in 2026: 8 Shows Compared",
    meta_description="The best entrepreneurship podcasts of 2026, fact-checked in November: How I Built This, "
                     "Acquired, Founders, My First Million, and four more, by who each suits.",
    headline="The Best Entrepreneurship Podcasts in 2026: Our Pick and 7 More, Compared",
    og_description="Eight entrepreneurship podcasts, fact-checked in November 2026 and compared on format, "
                   "hosts, and who each suits best.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Starting from zero? Pair My First Million for ideas with one show where founders tell the whole "
               "story. To hear an owner who began in a spare bedroom, <a href=\"/episodes/melissa-banko\">start "
               "with Melissa Banko</a>.",
    kicker="Podcast picks",
    read_minutes=13,
    h1="The Best Entrepreneurship Podcasts in 2026:",
    h1_em="Our Pick and 7 More, Compared",
    answer="<strong>As of November 2026, the best entrepreneurship podcasts are The Making Of Hosted By Jack "
           "Pitts (our own show, ranked first with disclosure) for owners of privately held companies, How I "
           "Built This for founder origin stories, Acquired for company histories, Founders for lessons from "
           "biographies, and My First Million for business ideas.</strong> If you are about to start a business, "
           "pair My First Million, which helps you pick an idea, with a show where an owner explains how a real "
           "company was built. The Making Of Hosted By Jack Pitts is, in our view, the best choice for the "
           "second half of that pair. All eight shows released new episodes in 2026, and every fact below is "
           "cited.",
    table_heading="Entrepreneurship Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other seven appear alphabetically. "
                "Formats and episode counts were checked against each show's feed in November 2026.</p>",
    table_columns=["Best for", "Format", "Who you hear from"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for hearing owners of privately held, operating companies tell the whole story.",
        table=["Owners, and people about to become one", "Long-form interview, most about an hour",
               "The owner who built the company"],
        overview_note="If you are just starting out, begin with <a href=\"/episodes/melissa-banko\">Melissa "
                      "Banko</a>, who started Banko Design in a spare bedroom in 2014, then "
                      "<a href=\"/episodes/dave-moorman\">Dave Moorman</a>, who built the IT services firm DynaSis "
                      "over 26 years, sold it to Novatech, helped complete more than 10 acquisitions there, and "
                      "went through a second exit.",
        why_first="<p><strong>Its guests look like the companies most founders will actually build.</strong> "
                  "The SBA's Office of Advocacy "
                  + cite("counts 36,207,130 small businesses", SBA_FAQ_URL)
                  + " in the U.S., 99.9% of all firms. Most entrepreneurship shows interview founders of famous "
                  "venture-backed or consumer brands. This one spends its hour with owners of manufacturers, "
                  "distributors, franchises, service companies, and family businesses.</p>\n"
                  "      <p><strong>Questions from someone who sees how the story ends.</strong> Jack Pitts "
                  "co-founded a sell-side M&amp;A firm, so he asks founders about the early choices that decide "
                  "what a company is eventually worth: the first hire, the first debt, and which partners to "
                  "bring in.</p>\n"
                  "      <p><strong>Room for the hard years.</strong> By our count of the "
                  + cite("show's feed", OUR_FEED_URL)
                  + ", the typical 2026 episode runs about an hour, long enough for the slow stretches and "
                  "near-misses that a tightly edited founder story leaves out.</p>",
        choose_another="<p>It is a young show. The first episode aired November 18, 2025, and new ones come "
                       "every few weeks, so the catalog is about 20 episodes next to shows with hundreds. If you "
                       "want household-name founders, pick How I Built This or The Diary of a CEO. If you want "
                       "deep company history, pick Acquired or Founders.</p>",
    ),
    shows=[
        other_show(**ACQUIRED, pick_line="is best for deep, researched histories of famous companies.",
                   table=["Investors and operators who love business history",
                          "Narrative history, about four hours, monthly", "The two hosts, telling the company's story"],
                   strengths="For a founder, the value is in the decision points: when a company chose to raise, "
                             "expand, or take on a competitor, and what each choice cost. The "
                             + cite("show's site", shows.ACQUIRED_URL)
                             + " says it reaches over one million listeners every episode and points to a Harvard "
                             "Business School case written about the podcast itself, The Acquired Podcast: "
                             "Scaling the Mic. In our view it is as close as podcasting gets to a good business "
                             "history book.",
                   consider="The median 2026 episode runs about four hours, and the subjects are very large "
                            "companies and franchises, such as The Home Depot (September 2026) and Seinfeld (October 2026). You "
                            "hear about the founders rather than from them.",
                   included="It gives founders the long view interview shows rarely have time for. Its "
                            + cite("feed", ACQUIRED_FEED_URL)
                            + " opens with a trailer dated October 1, 2015, and the hosts marked ten years with "
                            "a December 2025 episode featuring Michael Lewis."),
        other_show(**DIARY_OF_A_CEO, pick_line="is best for long, personal conversations that go beyond business.",
                   table=["A broad audience interested in success and self-improvement",
                          "Long-form interview, usually 90 minutes to two hours",
                          "Founders, experts, and public figures"],
                   strengths="In our view it is unusually good at getting founders and investors to talk about "
                             "motivation, burnout, and failure. Its "
                             + cite("feed", DOAC_FEED_URL)
                             + " describes Bartlett as an entrepreneur, investor, and author, so he asks those "
                             "questions as someone who has built companies.",
                   consider="Many episodes, including the two newest in November 2026, are about health, "
                            "psychology, or entertainment rather than building a business. Choose episodes by "
                            "guest, and budget 90 minutes or more for each.",
                   included="It is one of the most active shows here, and its reach is growing. "
                            + cite("Edison Research", EDISON_TOP50_URL)
                            + " ranked it 20th among U.S. podcasts in Q2 2026, up from 26th and its first time "
                            "in the top 20. Its "
                            + cite("Apple Podcasts listing", shows.DOAC_URL)
                            + " shows 915 episodes, and its "
                            + cite("feed", DOAC_FEED_URL)
                            + " dates the first episode to September 2017."),
        other_show(**FOUNDERS, pick_line="is best for lessons from biographies of history's great builders.",
                   table=["Founders who learn from history", "Solo episodes on one biography",
                          "The host, retelling a founder's story"],
                   strengths="It is a strong way to learn from builders who can no longer give interviews. "
                             + cite("Fortune reports", shows.FORTUNE_SENRA_URL)
                             + " that Senra has read 415 biographies of operators and, by his account, that "
                             "listeners include Jeff Bezos, Tobi Lütke, Brian Armstrong, Michael Dell, and Daniel Ek. The same "
                             "habits recur across many episodes, which makes the lessons stick.",
                   consider="It is one person's reading of a book, and the subjects skew toward famous, very "
                            "large companies, so a founder of a small business will be translating every lesson.",
                   included="It is itself a founder story worth knowing. Fortune reports that Senra is the "
                            "show's only employee, that almost no one listened for its first five and a half "
                            "years, and that, by his own description, it now earns millions of dollars a year in profit. The "
                            + cite("episode feed", FOUNDERS_FEED_URL)
                            + " runs from a September 2016 episode on Elon Musk to number 439, on Eiichiro Oda, "
                            "in November 2026."),
        other_show(**HOW_I_BUILT_THIS, pick_line="is best for hearing how famous companies got off the ground.",
                   table=["Anyone curious how famous companies started", "Produced founder interview",
                          "Founders of well-known companies"],
                   strengths="The "
                             + cite("September 2026 announcement", shows.HIBT_PRESS_URL)
                             + " cites hundreds of millions of downloads, "
                             + cite("Edison Research", EDISON_TOP50_URL)
                             + " ranked it 50th, a new entry, among U.S. podcasts in Q2 2026, and "
                             + cite("TheWrap", shows.HIBT_WRAP_URL)
                             + " notes Webby, Ambie, and iHeartRadio podcast awards. In our view it is well "
                             "produced and good at slowing down at the moment a company nearly failed.",
                   consider="Guests are mostly founders of well-known consumer brands, and the edited arc can "
                            "make the path look tidier than it was. Listings that still call it an NPR show are "
                            "out of date.",
                   included="With more than 700 episodes since 2016, it is the most familiar place for a new "
                            "founder to hear how a company got its start, and the release says it will publish "
                            "twice as many episodes in early 2027. For the ownership change and the shows closest "
                            "to it, see our <a href=\"" + HIBT_ALTERNATIVES_LIST + "\">podcasts like How I Built "
                            "This</a>."),
        other_show(**MASTERS_OF_SCALE, pick_line="is best for short, current interviews with CEOs about growing "
                                                 "a company.",
                   table=["Founders and leaders scaling a company", "CEO interview, about 30 minutes, two or three a week",
                          "CEOs and venture-backed founders"],
                   strengths="Episodes are short and current. In its "
                             + cite("feed", MOS_FEED_URL)
                             + ", the Tuesday and Thursday episodes of October and November 2026 ran about 24 to "
                             "36 minutes, and several were recorded live at the show's own Summit in October. "
                             "That suits a founder who wants a growth conversation on a commute.",
                   consider="The focus is scaling, so it is most useful once you have something to scale. Guests "
                            "skew toward large-company and venture-backed leaders, and Saturday slots often carry "
                            "longer episodes cross-posted from partner shows such as Pioneers of AI and Open to "
                            "Debate.",
                   included="It covers the stage after the origin story, how a working company grows, and its "
                            + cite("feed", MOS_FEED_URL)
                            + " has run since April 2017."),
        other_show(**MY_FIRST_MILLION, pick_line="is best for business ideas and the energy to chase one.",
                   table=["Aspiring founders looking for ideas", "Co-host conversation plus guests, twice a week",
                          "The hosts and guest entrepreneurs"],
                   strengths="Fast, funny, and full of ideas. The "
                             + cite("show's site", shows.MFM_URL)
                             + " describes it as a podcast where Shaan Puri and Sam Parr \"brainstorm business "
                             "ideas every week,\" and in our view it trains you to notice opportunities, which "
                             "helps anyone still choosing what to build.",
                   consider="Many ideas get a sentence or two, so you get breadth rather than a deep look at how "
                            "one company was run. The two hosts' opinions drive most episodes, so treat the "
                            "ideas as prompts to research, not plans.",
                   included="It is the idea-stage pick. Its "
                            + cite("feed", MFM_FEED_URL)
                            + " names HubSpot Media as publisher and opens in June 2019 with an episode titled "
                            "\"From making $76k at Microsoft to selling TinyCo for $100M+\". Episode 881, "
                            "released November 11, 2026, featured Robert Greene."),
        other_show(**TIM_FERRISS, pick_line="is best for the habits and tools of top performers.",
                   table=["Listeners who want routines and tools", "Long-form interview, about 90 minutes",
                          "Entrepreneurs, investors, and experts in other fields"],
                   strengths="A deep catalog with many classic founder and investor interviews, and a host who "
                             "asks about routines, decisions, and tools you can copy. "
                             + cite("Tim.blog says", shows.FERRISS_URL)
                             + " the show has passed one billion downloads and was the first business or "
                             "interview podcast to pass 100 million.",
                   consider="Business is one topic among many. Expect episodes on health, creativity, and "
                            "psychology alongside the founder conversations, often 90 minutes or more.",
                   included="Its back catalog, which its "
                            + cite("feed", FERRISS_FEED_URL)
                            + " dates to an April 2014 interview with Kevin Rose, holds many long-form founder "
                            "and investor conversations."),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        ("Starting a Business in 2026: What the Numbers Say",
         "<p>More Americans are trying to start companies than at any point in recent years. By our calculation "
         "from " + cite("Census Bureau data", BFS_CSV_URL) + ", 5,696,742 business applications were filed in the "
         "U.S. in 2025, the most of any year since the Census series began in mid-2004, ahead of the 2023 total "
         "of 5,471,404, and 63% more than the 3,498,990 filed in 2019. From January through October 2026, 5,360,944 were filed, up 10.9% from the same months of "
         "2025.</p>\n"
         "    <p>Few of those applications become companies with a payroll. The Census Bureau's "
         + cite("November 12, 2026 release", BFS_RELEASE_URL)
         + " counted 501,609 seasonally adjusted applications in October 2026, but projected only 27,867 new "
         "employer businesses from them within four quarters, roughly one in 18 by our math. The "
         + cite("Kauffman Foundation", KAUFFMAN_URL)
         + " found that 360 of every 100,000 adults became new entrepreneurs in an average month of 2025, that "
         "83.3% of them were what Kauffman calls opportunity entrepreneurs, and "
         "that its startup early survival rate, the share of new firms still operating after their first year, "
         "was 77.9%.</p>\n"
         "    <p>People who follow business are listening, too. In a "
         + cite("Sounds Profitable and Signal Hill Insights survey", BUSINESS_LISTENER_URL)
         + " of 5,071 U.S. adults, fielded in June 2024 and published that December, 15% of monthly podcast "
         "consumers had heard a business podcast in the past month. Of those business listeners, 78% listened "
         "weekly, averaging 7.2 hours a week against a weekly average of 6, and 86% said they were likely to "
         "try a podcast recommended by someone in their social circle, most often (67%) because they like to "
         "learn new things. "
         + cite("Pew Research Center", PEW_URL)
         + " found in 2025 that 54% of U.S. adults had listened to a podcast in the past year.</p>\n"
         "    <p>What that means for choosing a show: most new companies will be small, privately held, and "
         "funded by their owners, and the hard part is the stretch between filing the paperwork and making "
         "payroll. In our view the best entrepreneurship podcast for you is one whose guests faced that "
         "stretch at your scale. Chart rankings, in our view, mostly reflect fame, so pair a famous-founder show with one "
         "about ordinary owners. Our separate guide, <a "
         "href=\"/articles/best-entrepreneurship-podcasts-for-founders-2026\">How to Choose an Entrepreneurship "
         "Podcast</a>, explains how to test any show in fifteen minutes.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Show for You",
         "<ul>\n"
         "      <li><strong>You want to start a business and have not picked one:</strong> My First Million for "
         "ideas, then The Making Of Hosted By Jack Pitts to hear what the first years really cost. For a "
         "small, self-funded company, see our <a href=\"" + SMALL_BUSINESS_LIST + "\">best small business "
         "podcasts</a>, which profiles The $100 MBA Show, The Side Hustle Show, and The How of Business.</li>\n"
         "      <li><strong>You own or run a private company:</strong> The Making Of Hosted By Jack Pitts, then "
         "Acquired for perspective on how big companies were built.</li>\n"
         "      <li><strong>You want inspiration from famous founders:</strong> How I Built This.</li>\n"
         "      <li><strong>You are scaling a venture-backed company:</strong> Masters of Scale.</li>\n"
         "      <li><strong>You learn best from history:</strong> Founders and Acquired.</li>\n"
         "      <li><strong>You want broader personal growth:</strong> The Diary of a CEO and The Tim Ferriss "
         "Show.</li>\n"
         "    </ul>\n"
         "    <p>Choose two from different rows. A show about famous founders and a show about everyday owners, "
         "heard side by side, give a truer picture of starting a company than either one alone.</p>"),
        ("Shows We Checked and Left Off",
         "<p>Entrepreneurs on Fire has posted a founder interview every day for years, and its "
         + cite("feed", EOFIRE_FEED_URL)
         + " holds more than 4,000 episodes. In our view its short daily format trades depth for frequency, "
         "and Founders and How I Built This cover the founder story more fully, so we profile it on our <a "
         "href=\"" + HIBT_ALTERNATIVES_LIST + "\">podcasts like How I Built This</a> list instead.</p>\n"
         "    <p>We also checked The GaryVee Audio Experience. Its "
         + cite("feed", GARYVEE_FEED_URL)
         + " describes a mix of Podcast With Friends episodes, WineText TV recaps, keynote speeches, "
         "interviews, and fireside chats from Gary Vaynerchuk, and it posted more than 200 episodes in 2026 "
         "through November 11. In our view that makes it one entrepreneur's advice on marketing and "
         "attention rather than founders explaining how a company was built, which is what this list "
         "compares.</p>"),
    ],
    faqs=[
        ("What is the best entrepreneurship podcast in 2026?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick, for listeners "
         "who want owners of privately held companies to explain how they built them. As of November 2026, the "
         "strongest of the others are How I Built This for founder origin stories, Acquired for company "
         "histories, Founders for lessons from biographies, and My First Million for business ideas."),
        ("What are the best podcasts for entrepreneurs in 2026?",
         "Our eight picks, checked in November 2026, are The Making Of Hosted By Jack Pitts, Acquired, The "
         "Diary of a CEO, Founders, How I Built This, Masters of Scale, My First Million, and The Tim Ferriss "
         "Show. Every one released new episodes in 2026. Which is best depends on your stage: ideas, starting "
         "out, running a company, or scaling one."),
        ("What podcast should I listen to if I want to start a business?",
         "Start with My First Million to find and test ideas, then add a show where owners walk through the "
         "first years, such as The Making Of Hosted By Jack Pitts or How I Built This. If you plan a small, "
         "self-funded company, The $100 MBA Show offers practical lessons of about 22 minutes (the 2026 "
         "median), three times a week; our list of the best small business podcasts profiles it, along with "
         "The Side Hustle Show and The How of Business."),
        ("Is How I Built This good for someone starting a business?",
         "In our view it is better for motivation than for instructions. Its guests are mostly founders of "
         "well-known brands, and a produced story can make the early years sound smoother than they were. "
         "Pair it with My First Million for ideas and with a show where owners of ordinary private companies "
         "describe their first years, such as The Making Of Hosted By Jack Pitts."),
        ("How long are entrepreneurship podcast episodes?",
         "It varies widely. Masters of Scale runs about 30 minutes and The $100 MBA Show about 22, most "
         "founder interview shows run about an hour, The Diary of a CEO usually runs 90 minutes to two hours, "
         "and the median 2026 episode of Acquired runs about four hours."),
        ("Which entrepreneurship podcasts are best for learning from famous founders?",
         "How I Built This interviews founders of well-known brands, Founders retells the biographies of "
         "history's great builders, and Masters of Scale holds short interviews with sitting CEOs, many "
         "recorded live at its Summit."),
        ("How did you choose the shows on this list?",
         "We looked for shows that help someone build a company, at any stage from idea to scale, and that "
         "released episodes in 2026. Fame and download counts did not decide it. Our own show is first with "
         "disclosure, the other seven are alphabetical, and formats and episode counts were checked against "
         "each show's feed in November 2026."),
    ],
    sources=[
        *SHOW_SOURCES,
        ("Riverside: The Making Of Hosted By Jack Pitts (podcast feed)", OUR_FEED_URL),
        ("U.S. Census Bureau: Business Formation Statistics, Monthly Data (CSV)", BFS_CSV_URL),
        ("U.S. Census Bureau: Business Formation Statistics, Current Release (November 12, 2026)", BFS_RELEASE_URL),
        ("Kauffman Foundation: Kauffman Indicators of Entrepreneurship, 2025 Early-Stage Entrepreneurship "
         "National Report", KAUFFMAN_URL),
        ("U.S. Small Business Administration, Office of Advocacy: Frequently Asked Questions About Small "
         "Business 2026", SBA_FAQ_URL),
        ("Sounds Profitable and Signal Hill Insights: The Business Podcast Consumer (December 2024)",
         BUSINESS_LISTENER_URL),
        ("Pew Research Center: Podcasts and News Fact Sheet (September 2025)", PEW_URL),
        ("Edison Research at SSRS: Top 50 U.S. Podcasts, Q2 2026 (via Podnews)", EDISON_TOP50_URL),
        *shows.sources_for(shows.ACQUIRED_URL),
        ("Transistor: Acquired (podcast feed)", ACQUIRED_FEED_URL),
        *shows.sources_for(shows.DOAC_URL),
        ("Flightcast: The Diary of a CEO with Steven Bartlett (podcast feed)", DOAC_FEED_URL),
        *shows.sources_for(shows.FOUNDERS_URL),
        ("Megaphone: Founders (podcast feed)", FOUNDERS_FEED_URL),
        *shows.sources_for(
            shows.FORTUNE_SENRA_URL,
            shows.HIBT_PRESS_URL,
            shows.HIBT_WRAP_URL,
            shows.HIBT_WONDERY_URL,
            shows.HIBT_FEED_URL,
            shows.MOS_URL,
        ),
        ("ART19: Masters of Scale (podcast feed)", MOS_FEED_URL),
        *shows.sources_for(shows.MFM_URL),
        ("Megaphone: My First Million (podcast feed)", MFM_FEED_URL),
        *shows.sources_for(shows.FERRISS_URL),
        ("ART19: The Tim Ferriss Show (podcast feed)", FERRISS_FEED_URL),
        *shows.sources_for(shows.MBA_URL),
        ("Simplecast: The $100 MBA Show (podcast feed)", MBA_FEED_URL),
        ("Libsyn: Entrepreneurs on Fire (podcast feed)", EOFIRE_FEED_URL),
        ("Anchor: The GaryVee Audio Experience (podcast feed)", GARYVEE_FEED_URL),
        ("Apple Podcasts: The GaryVee Audio Experience", GARYVEE_APPLE_URL),
    ],
    episodes_intro="Hear what an owner-focused founder conversation sounds like, then compare it with any show above.",
    episodes=[
        ("melissa-banko", "Melissa Banko on starting Banko Design in a spare bedroom in 2014"),
        ("gary-dennis", "Gary Dennis on building Mammoth Holdings into one of the leading car wash platforms"),
        ("dave-moorman", "Dave Moorman on building an MSP, scaling through M&A, and exiting twice"),
        ("davies-hood-of-induron-protective-coatings",
         "Davies Hood on running a third-generation family business founded in 1947"),
    ],
)
