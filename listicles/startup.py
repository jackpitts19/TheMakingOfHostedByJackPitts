"""Best Startup Podcasts in 2026: our disclosed pick, then seven more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SOURCES, other_show, our_show
from listicles.shows import cite

# Pages cited on this list that are not already in listicles/shows.py.
TWENTY_VC_URL = "https://www.thetwentyminutevc.com/"
TWENTY_VC_FEED_URL = "https://rss.libsyn.com/shows/61840/destinations/240976.xml"
TWENTY_VC_APPLE_URL = ("https://podcasts.apple.com/us/podcast/the-twenty-minute-vc-20vc-venture-capital-startup/"
                       "id958230465")
YC_FEED_URL = "https://anchor.fm/s/8c1524bc/podcast/rss"
YC_APPLE_URL = "https://podcasts.apple.com/us/podcast/y-combinator-startup-podcast/id1236907421"
LENNY_URL = "https://www.lennysnewsletter.com/podcast"
LENNY_FEED_URL = "https://api.substack.com/feed/podcast/10845.rss"
TWIST_ABOUT_URL = "https://www.thisweekinstartups.com/about"
TWIST_FEED_URL = "https://feeds.megaphone.fm/LTANT7633840743"
ILTB_FEED_URL = "https://feeds.megaphone.fm/CLS2859450455"
COLOSSUS_URL = "https://colossus.com/"
MOS_FEED_URL = "https://rss.art19.com/masters-of-scale"
CRUNCHBASE_Q3_URL = ("https://news.crunchbase.com/venture/"
                     "q3-2026-global-startup-funding-ai-billion-dollar-rounds-exits-data/")
CRUNCHBASE_US_AI_URL = "https://news.crunchbase.com/venture/us-ai-startup-funding-boom-data/"

TWENTY_VC = dict(
    name="The Twenty Minute VC (20VC)",
    site=TWENTY_VC_URL,
    apple=TWENTY_VC_APPLE_URL,
    facts=[
        ("Host", "Harry Stebbings"),
        ("Format", "Founder and investor interviews, often about an hour, several a week"),
        ("Owner", "Independent (the 20VC brand)"),
        ("Focus", "Venture capital, fundraising, and how investors think"),
    ],
    overview="Harry Stebbings interviews venture capitalists and founders about raising, investing, and "
             "markets. The " + cite("show's feed description", TWENTY_VC_FEED_URL)
             + " says past investor guests include Sequoia's Doug Leone and Benchmark's Bill Gurley, and past "
             "founder guests include Spotify's Daniel Ek and LinkedIn's Reid Hoffman. The same feed lists more than 1,500 episodes and added new ones about three times a week "
             "through October and early November 2026.",
    strengths="In our view it is a clear window into how investors actually decide. If you are about to raise, "
              "hearing partners explain what they look for, and what makes them pass, is direct preparation "
              "for the meeting.",
    consider="Despite the name, episodes often run about an hour. The lens is the investor's, so it says less "
             "about running a company day to day, and it matters most if you plan to raise venture money at all.",
    included="It is a long-running, frequently published interview show about venture funding, one of the "
             "biggest decisions many startup founders face.",
)

YC_STARTUP = dict(
    name="Y Combinator Startup Podcast",
    site=YC_APPLE_URL,
    facts=[
        ("Hosts", "Y Combinator partners, including the Lightcone hosts Garry Tan, Harj Taggar, Jared Friedman, "
                  "and Diana Hu"),
        ("Format", "Partner roundtables, founder interviews, and talks"),
        ("Publisher", "Y Combinator"),
        ("Focus", "Early-stage company building, especially AI startups"),
    ],
    overview="This is Y Combinator's own feed, which " + cite("describes itself", YC_FEED_URL)
             + " as the place where \"YC partners and founders share real stories, lessons, and tactics from the "
             "frontlines.\" Episodes of The Lightcone, the partners' roundtable, now publish here, and the feed "
             "carries dozens of episodes dated 2026, including a conversation with Supabase CEO Paul "
             "Copplestone in October. In its September 2026 episode on the state of startups, "
             + cite("YC said", YC_FEED_URL) + " nearly one in five YC companies has a solo founder.",
    strengths="The advice comes from the partners who run an accelerator, and in our view the roundtables are "
              "a good way to hear how YC thinks about what is working for early-stage companies right now.",
    consider="It reflects Y Combinator's model of company building: fast, venture-funded, and heavily focused "
             "on software and AI in 2026. Founders building a bootstrapped or local business will need to "
             "translate.",
    included="It is the accelerator's official show, and it is where Lightcone episodes kept running through "
             "2026 after the standalone Lightcone feed stopped updating.",
)

LENNYS_PODCAST = dict(
    name="Lenny's Podcast",
    site=LENNY_URL,
    apple="https://podcasts.apple.com/us/podcast/lennys-podcast-product-career-growth/id1627920305",
    facts=[
        ("Host", "Lenny Rachitsky"),
        ("Format", "Weekly long-form interview"),
        ("Publisher", "Lenny's Newsletter (independent)"),
        ("Focus", "Product, growth, and finding product-market fit"),
    ],
    overview="Lenny Rachitsky interviews product leaders and growth experts. The "
             + cite("show's feed", LENNY_FEED_URL) + " promises \"concrete, actionable, and tactical advice to help "
             "you build, launch, and grow your own product,\" and recent founder-relevant episodes include an "
             "86-minute guide to finding product-market fit with Rob Snyder. The "
             + cite("newsletter's podcast page", LENNY_URL) + " reports over 1,200,000 subscribers to the "
             "publication, a count that covers the newsletter, not podcast downloads.",
    strengths="In our view it is one of the more tactical shows on this list, and a strong pick for founders "
              "who are the product lead at their own company and want specific playbooks for onboarding, "
              "pricing, and growth.",
    consider="Many guests are product leaders and growth experts rather than founders, so some episodes are "
             "more about product careers than starting a company.",
    included="Finding product-market fit is the central problem of an early-stage startup, and in our view "
             "this show gives it more direct attention than founder story shows do.",
)

THIS_WEEK_IN_STARTUPS = dict(
    name="This Week in Startups",
    site=TWIST_ABOUT_URL,
    apple="https://podcasts.apple.com/us/podcast/this-week-in-startups/id315114957",
    facts=[
        ("Hosts", "Jason Calacanis, with co-host Alex Wilhelm"),
        ("Format", "Several episodes a week: founder interviews, news roundups, and VC panels"),
        ("Network", "LAUNCH"),
        ("Focus", "Startups, angel investing, and tech news"),
    ],
    overview="The show's " + cite("About page", TWIST_ABOUT_URL) + " says it has documented startups since "
             "2009. It describes host Jason Calacanis as an early investor in more than 400 companies and co-host Alex Wilhelm as a journalist who anchors market roundups and "
             "VC deep dives. Numbered episodes in the " + cite("show's feed", TWIST_FEED_URL)
             + " have passed 2,360, and the most recent include an interview with the CEO of Satlyt and a segment on founders sending VCs files written for AI.",
    strengths="Volume and timeliness. In our view it is a good way to stay current on what early-stage founders "
              "and angel investors are talking about this week.",
    consider="With several episodes a week, it rewards picking and choosing. The tone is conversational and "
             "opinionated, and the news episodes date quickly.",
    included="It has covered early-stage startups since 2009 and still publishes several times a week, which "
             "makes it a natural companion to slower, evergreen shows.",
)

INVEST_LIKE_THE_BEST = dict(
    name="Invest Like the Best with Patrick O'Shaughnessy",
    site=COLOSSUS_URL,
    apple="https://podcasts.apple.com/us/podcast/invest-like-the-best-with-patrick-oshaughnessy/id1154105909",
    facts=[
        ("Host", "Patrick O'Shaughnessy"),
        ("Format", "Long-form interview, about one a week"),
        ("Network", "Colossus"),
        ("Focus", "Investors and founders on venture, markets, and company building"),
    ],
    overview="Patrick O'Shaughnessy interviews investors, founders, and business leaders. The "
             + cite("show's feed", ILTB_FEED_URL) + " says it is meant for professional investors, CEOs, "
             "entrepreneurs, and business strategists, and the show reached its 500th episode on November 11, "
             "2026 with Ro co-founder Zach Reitano. Other fall 2026 guests in the feed include Michael Moritz, Nubank's David Vélez, "
             "and Martin Casado. The show is published by " + cite("Colossus", COLOSSUS_URL) + ".",
    strengths="Long, thoughtful conversations that connect company building to how capital and markets work. "
              "In our view it suits founders who want to understand the investor side of the table in depth.",
    consider="Many episodes are about public markets and investing rather than starting a company, so the "
             "startup-specific episodes take some choosing.",
    included="It features venture investors and founders at length, and in our view it gives startup founders "
             "a strategic counterweight to tactical shows.",
)

LISTICLE = dict(
    slug="best-startup-podcasts-2026",
    title_tag="Best Startup Podcasts in 2026: 8 Shows Compared",
    meta_description="Eight startup podcasts worth your time in 2026, from 20VC and Y Combinator to Lenny's "
                     "Podcast, compared on format, guests, and who each suits best.",
    headline="The Best Startup Podcasts in 2026: Our Pick and 7 More, Compared",
    og_description="Eight startup podcasts compared on format, guests, and which founders each one suits.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when you need help with this quarter's problem, such as a raise or "
               "product-market fit. To hear founders on the years after, <a href=\"/episodes\">start with any "
               "episode</a>.",
    kicker="Podcast picks",
    read_minutes=11,
    h1="The Best Startup Podcasts in 2026:",
    h1_em="Our Pick and 7 More, Compared",
    answer="<strong>The best startup podcasts in 2026 are The Making Of Hosted By Jack Pitts (our own show, "
           "ranked first with disclosure) for how a startup becomes a lasting company, The Twenty Minute VC for "
           "venture fundraising, the Y Combinator Startup Podcast for early-stage advice, and Lenny's Podcast for "
           "product-market fit.</strong> In our view, The Making Of Hosted By Jack Pitts is the best choice if "
           "you want founders explaining the whole arc, from first funding to running a company for decades.",
    table_heading="Startup Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other seven appear alphabetically.</p>",
    table_columns=["Best for", "Format", "Who you hear from"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for hearing how founders turn a startup into a company that lasts.",
        table=["Founders who want the whole arc, from first round to a business that lasts",
               "Long-form interview, about an hour",
               "Startup founders and the owners of established companies"],
        overview_note="Founders in the thick of it might start with <a href=\"/episodes/jesse-choe\">Jesse "
                      "Choe</a>, who raised $1 million at 19 and went through Y Combinator.",
        why_first="<p><strong>Both ends of the startup story.</strong> The show talks with founders in the "
                  "middle of it, such as <a href=\"/episodes/jesse-choe\">a Y Combinator founder who raised $1 "
                  "million at 19</a> and <a href=\"/episodes/concentrate-ai\">an AI infrastructure startup that "
                  "raised $5.1 million</a>, and with owners who built companies that have lasted decades. "
                  "Hearing both shows you where the startup years actually lead.</p>\n"
                  "      <p><strong>Not every startup is a software company.</strong> In our view, most startup "
                  "shows assume venture capital and a tech product. Here you also hear from the owners of "
                  "franchises, distributors, manufacturers, and service companies.</p>\n"
                  "      <p><strong>A view from the far end of the startup story.</strong> Because Jack Pitts "
                  "advises owners when they sell, the questions keep returning to what makes a company last and "
                  "hold its value after the first rounds: margins, customers, hiring, and debt.</p>",
        choose_another="<p>It is a young show, launched in November 2025, so the catalog is small next to shows "
                       "with hundreds of episodes, and it does not cover startup news. If you are raising venture "
                       "money this quarter, pick The Twenty Minute VC or This Week in Startups. If you are hunting "
                       "for product-market fit, pick Lenny's Podcast or the Y Combinator Startup Podcast.</p>",
    ),
    shows=[
        other_show(**shows.ACQUIRED, pick_line="is best for strategy lessons drawn from famous companies' full histories.",
                   table=["Founders who learn strategy from business history", "Long-form narrative, two hosts",
                          "The founding story, as researched by the hosts"],
                   strengths="For startup founders, the payoff is seeing how capital, timing, and competition "
                             "shaped the winners, decisions you will face at a much smaller scale.",
                   consider="The companies are mostly giants and the stories come from the hosts, not the "
                            "founders, so it is better for strategy than for this week's tactics.",
                   included="It gives founders the long view, how early bets played out over decades, which "
                            "tactical startup shows rarely cover."),
        other_show(**INVEST_LIKE_THE_BEST, pick_line="is best for long conversations on capital, markets, and company building.",
                   table=["Founders who want to understand investors in depth", "Long-form interview",
                          "Investors, founders, and business leaders"]),
        other_show(**LENNYS_PODCAST, pick_line="is best for tactical advice on product, growth, and product-market fit.",
                   table=["Founders searching for product-market fit", "Weekly long-form interview",
                          "Product leaders and growth experts"]),
        other_show(**{**shows.MASTERS_OF_SCALE,
                      "overview": "Each main episode is a short conversation with a well-known founder or CEO about growth. "
                                  "The " + cite("show's feed", MOS_FEED_URL) + " describes a set of hosts and "
                                  "still bills Reid Hoffman as founding host. Jeff Berman is credited as host "
                                  "on many recent episodes, including a conversation with Walmart CEO John "
                                  "Furner recorded live at the Masters of Scale Summit in October 2026. The "
                                  + cite("show's site", shows.MOS_URL) + " also runs spin-off feeds produced by "
                                  "WaitWhat."},
                   pick_line="is best for growth lessons once you have something to scale.",
                   table=["Founders scaling past the early stage", "CEO interview, about 30 minutes, some recorded live",
                          "CEOs and venture-backed founders"],
                   strengths="Each interview walks through how a leader handled growth, which suits founders who have "
                             "found traction and need a framework for what comes next.",
                   consider="It is most useful after product-market fit. Guests skew toward venture-backed and "
                            "very large companies, so seed-stage founders may want a more tactical show first.",
                   included="It covers the stage after product-market fit, and its live Summit recordings add "
                            "timely conversations with sitting CEOs."),
        other_show(**THIS_WEEK_IN_STARTUPS, pick_line="is best for keeping up with early-stage startup and angel news.",
                   table=["Founders and angels who want weekly news", "Interviews, news roundups, and VC panels",
                          "Founders, investors, and the hosts"]),
        other_show(**TWENTY_VC, pick_line="is best for learning how venture capitalists think before you raise.",
                   table=["Founders preparing to raise venture money", "Interview, several a week",
                          "Venture capitalists and founders"]),
        other_show(**YC_STARTUP, pick_line="is best for early-stage advice straight from an accelerator's partners.",
                   table=["First-time founders at the earliest stage", "Partner roundtables, interviews, and talks",
                          "Y Combinator partners and founders"]),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        MARKET_CONTEXT,
        ("What the 2026 Startup Market Means for Your Listening",
         "<p>The startup money of 2026 is large and concentrated. Crunchbase's "
         + cite("third-quarter funding report", CRUNCHBASE_Q3_URL)
         + " found that global venture funding reached $159 billion across close to 6,000 startups in Q3 2026, "
         "down about 25% from Q2 but up about 53% from a year earlier, with a record 27 companies raising rounds "
         "of $1 billion or more. Crunchbase also " + cite("reported in June", CRUNCHBASE_US_AI_URL)
         + " that so far in 2026, nearly 88% of AI-related startup funding, or $319 billion, went to U.S.-headquartered "
         "companies.</p>\n"
         "    <p>Company building is changing too. In a September 2026 episode, "
         + cite("Y Combinator's partners said", YC_FEED_URL)
         + " that nearly one in five YC companies now has a solo founder and that startups are reaching "
         "meaningful revenue faster than ever.</p>\n"
         "    <p>That is why one show is rarely enough. Funding-focused shows explain how capital moves, product "
         "shows explain how to find customers, and founder interviews explain what the years after the first "
         "round actually look like. Most founders, in our view, need one of each.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Startup Podcast",
         "<ul>\n"
         "      <li><strong>You want to build a company that lasts:</strong> The Making Of Hosted By Jack Pitts, "
         "then Acquired for how famous companies did it.</li>\n"
         "      <li><strong>You are about to raise venture money:</strong> The Twenty Minute VC and Invest Like the "
         "Best with Patrick O'Shaughnessy.</li>\n"
         "      <li><strong>You are a first-time founder at the idea or seed stage:</strong> the Y Combinator "
         "Startup Podcast.</li>\n"
         "      <li><strong>You are still searching for product-market fit:</strong> Lenny's Podcast.</li>\n"
         "      <li><strong>You want weekly startup news:</strong> This Week in Startups.</li>\n"
         "      <li><strong>You are scaling past the early stage:</strong> Masters of Scale.</li>\n"
         "    </ul>\n"
         "    <p>Pair a tactical show with a founder story show. Advice tells you what to do this week, and long "
         "founder conversations tell you what the next ten years can look like.</p>"),
    ],
    faqs=[
        ("What is the best startup podcast in 2026?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick for founders who "
         "want to hear how a startup becomes a lasting company. Among the others, in our view, The Twenty Minute VC stands out for "
         "fundraising, the Y Combinator Startup Podcast for early-stage advice, and Lenny's Podcast for finding "
         "product-market fit."),
        ("What podcast should I listen to before raising venture capital?",
         "The Twenty Minute VC interviews venture capitalists and founders about how investors decide, and Invest "
         "Like the Best with Patrick O'Shaughnessy goes deep on investors and markets. This Week in Startups "
         "covers early-stage funding news several times a week."),
        ("Is the Lightcone podcast still active?",
         "Yes, but in a different feed. Based on the two feeds as of November 2026, the standalone Lightcone "
         "feed stopped updating in December 2025, and Lightcone episodes now publish in Y Combinator's own "
         "Startup Podcast feed, which released dozens of episodes in 2026."),
        ("Who hosts Masters of Scale now?",
         "The Masters of Scale feed describes a set of hosts, with Reid Hoffman billed as founding host. Jeff "
         "Berman is credited as host on many recent episodes, including a conversation with Walmart CEO John Furner "
         "recorded live at the October 2026 Masters of Scale Summit."),
        ("Are there startup podcasts for founders who are not building tech companies?",
         "Yes. The Making Of Hosted By Jack Pitts interviews founders of franchises, distributors, manufacturers, "
         "and service companies as well as venture-backed startups. Acquired also covers companies well outside "
         "software, such as Home Depot."),
        ("How did you choose the shows on this list?",
         "We matched shows to the questions founders face in order: what to build, how to find product-market "
         "fit, how to raise, and how to scale. Every show published in 2026, and the figures we cite come from "
         "each show's feed or site. Our own show is first, with disclosure."),
    ],
    sources=[*SOURCES, *shows.sources_for(shows.ACQUIRED_URL, shows.MOS_URL),
             ("Colossus: Official Site and Podcast Series", COLOSSUS_URL),
             ("Colossus: Invest Like the Best Podcast Feed", ILTB_FEED_URL),
             ("Crunchbase News: Q3 2026 Global Startup Funding", CRUNCHBASE_Q3_URL),
             ("Crunchbase News: U.S. AI Startup Funding Boom (June 2026)", CRUNCHBASE_US_AI_URL),
             ("Lenny's Newsletter: Lenny's Podcast", LENNY_URL),
             ("Lenny's Newsletter: Lenny's Podcast Feed", LENNY_FEED_URL),
             ("Masters of Scale: Official Podcast Feed", MOS_FEED_URL),
             ("This Week in Startups: About", TWIST_ABOUT_URL),
             ("This Week in Startups: Podcast Feed", TWIST_FEED_URL),
             ("20VC: Official Site", TWENTY_VC_URL),
             ("20VC: Podcast Feed", TWENTY_VC_FEED_URL),
             ("Apple Podcasts: The Twenty Minute VC (20VC)", TWENTY_VC_APPLE_URL),
             ("Y Combinator: Y Combinator Startup Podcast Feed", YC_FEED_URL),
             ("Apple Podcasts: Y Combinator Startup Podcast", YC_APPLE_URL)],
    episodes_intro="Hear what a founder conversation about building a lasting company sounds like, then compare "
                   "it with any show above.",
    episodes=[
        ("jesse-choe", "Jesse Choe on raising $1 million at 19 and going through Y Combinator"),
        ("concentrate-ai", "Ari Jacoby and Zach Moskow on raising $5.1 million for Concentrate AI"),
        ("nishank-gite", "Nishank Gite on co-founding Nirvana Robotics"),
    ],
)
