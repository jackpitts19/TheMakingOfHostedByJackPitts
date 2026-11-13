"""Best small business podcasts in 2026: our disclosed pick, then six more A to Z.

This list is about starting, running, and growing a company. Buying and
selling have their own list (buying_selling.py), so only Built to Sell Radio
appears on both, and it links readers there.

Every show's feed, site, and listing was re-checked on November 12, 2026.
Shared entries from shows.py are refreshed here where this list needs newer
facts (episode counts, episode length); the same fixes are requested for
shows.py so other lists inherit them.
"""

from listicles import shows
from listicles.common import (DISCLOSURE, PODCAST_CONSUMER_SOURCE, PODCAST_CONSUMER_URL, SHOW_SOURCES,
                              other_show, our_show)
from listicles.shows import cite

BUYING_SELLING_LIST = "/articles/best-podcasts-about-buying-and-selling-a-business-2026"
ENTREPRENEURSHIP_LIST = "/articles/best-entrepreneurship-podcasts-2026"
HIBT_ALTERNATIVES_LIST = "/articles/podcasts-like-how-i-built-this-2026"
EOFIRE_FEED_URL = "https://rss.libsyn.com/shows/37432/destinations/100507.xml"

# Market data for the explainer. Checked November 2026.
SBA_FAQ_URL = ("https://advocacy.sba.gov/wp-content/uploads/2026/02/"
               "FINAL_FAQsAboutSmallBusiness_2026_012826.pdf")
BFS_URL = "https://www.census.gov/econ/bfs/current/index.html"
BFS_CSV_URL = "https://www.census.gov/econ/bfs/csv/bfs_monthly.csv"

# Show pages cited only by this list. Checked November 2026.
ENTRELEADERSHIP_URL = "https://www.ramseysolutions.com/shows/the-entreleadership-podcast"
ENTRELEADERSHIP_APPLE_URL = "https://podcasts.apple.com/us/podcast/entreleadership/id435836905"
ENTRELEADERSHIP_FEED_URL = "https://feeds.megaphone.fm/RM6855404952"
SBM_URL = "https://servicebusinessmastery.com/"
SBM_HOSTS_URL = "https://servicebusinessmastery.com/about-the-hosts/"
SBM_PARKER_URL = "https://servicebusinessmastery.com/how-to-grow-home-service-business-paul-kelly-parker-sons/"
SBM_APPLE_URL = ("https://podcasts.apple.com/us/podcast/"
                 "service-business-mastery-for-skilled-trades-hvac-plumbing/id1530427467")
SBM_FEED_URL = "https://rss.libsyn.com/shows/106436/destinations/574473.xml"
HOB_FEED_URL = "https://rss.libsyn.com/shows/77073/destinations/346019.xml"
HOB_APPLE_URL = ("https://podcasts.apple.com/us/podcast/"
                 "the-how-of-business-how-to-start-run-grow-and/id1105145426")
MBA_ABOUT_URL = "https://100mba.net/about/"
MBA_FEED_URL = "https://feeds.simplecast.com/equXS9ic"
BTS_ABOUT_URL = "https://builttosell.com/about/"
BTS_FEED_URL = "https://rss.libsyn.com/shows/66633/destinations/269159.xml"
SIDE_HUSTLE_FEED_URL = "https://rss.introcast.io/655135292/feeds.megaphone.fm/YAP9195874886"

ENTRELEADERSHIP = dict(
    name="EntreLeadership",
    site=ENTRELEADERSHIP_URL,
    apple=ENTRELEADERSHIP_APPLE_URL,
    facts=[
        ("Hosts", "Dave Ramsey and John Felkins, EntreLeadership's head coach"),
        ("Format", "Short episodes, most about 10 to 25 minutes, Monday, Wednesday, and Friday"),
        ("Catalog", "About 750 episodes"),
        ("Network", "Ramsey Network"),
        ("Focus", "Leading, running, and growing a small business"),
    ],
    overview="Ramsey's " + cite("official show page", ENTRELEADERSHIP_URL)
             + " calls EntreLeadership \"the playbook behind Dave Ramsey's $300 million company\" and says "
             "co-host John Felkins has led EntreLeadership's coaching team since 2012. The "
             + cite("show's feed", ENTRELEADERSHIP_FEED_URL)
             + " promises \"a behind-the-scenes look at what it takes to scale and run a multimillion-dollar "
             "business\" and lists about 750 episodes. In fall 2026 it posted every Monday, Wednesday, and "
             "Friday, with episodes such as \"Buying a Business vs. Starting One: Which Is Better?\" (October 2), "
             "\"How Seasonal Businesses Actually Make Money\" (October 30), and \"How I Built a 7-Figure Business "
             "From My Garage\" (November 6).",
    strengths="Each episode takes one operating problem and answers it fast. Fall 2026 brought "
              + cite("episodes", ENTRELEADERSHIP_FEED_URL)
              + " on replacing a key employee who died unexpectedly, unpacking Dave Ramsey's hiring formula, "
              "and moving faster without hiring more people, and 101 of the show's 121 episodes in 2026 ran "
              "under half an hour. In our view it is one of the most practical habits here for an owner who "
              "manages a team.",
    consider="By its own description it is one company's playbook, so weigh the advice against your own "
             "business. Some episodes also address faith, such as \"I'm a Christian, Should I Work on "
             "Sundays?\" (November 2, 2026).",
    included="It is an active show about leading and running a small company day to day, three times a week, "
             "which in our view is the part of ownership most business podcasts give the least time.",
)

SERVICE_BUSINESS_MASTERY = dict(
    name="Service Business Mastery",
    site=SBM_URL,
    apple=SBM_APPLE_URL,
    facts=[
        ("Hosts", "Tersh Blissett and Joshua Crouch"),
        ("Format", "Weekly interview on Wednesdays, most about 42 to 52 minutes"),
        ("Catalog", "More than 500 episodes, back to 2017"),
        ("Network", "Skilled Trades Syndicate"),
        ("Focus", "Running home service and skilled trades companies: HVAC, plumbing, electrical"),
    ],
    overview="Tersh Blissett and " + cite("Joshua Crouch", SBM_HOSTS_URL)
             + " talk with operators and vendors about running a trades business. The "
             + cite("show's feed", SBM_FEED_URL)
             + " says it covers leadership, marketing, finance, pricing, and HR, along with automation and AI, "
             "lists more than 500 episodes since September 2017, and posted every Wednesday through fall 2026. "
             "A " + cite("September 2026 episode", SBM_PARKER_URL)
             + " with Paul Kelly covered how Parker &amp; Sons grew from $7 million to roughly $260 million.",
    strengths="The hosts come from the trades. The show's "
              + cite("episode pages", SBM_PARKER_URL)
              + " say Crouch spent more than eight years in HVAC as an operations manager, branch manager, "
              "territory sales manager, and director of marketing, that he founded Relentless Digital, and that "
              "Blissett has built several home service businesses in his small-town market. Topics are just as "
              "specific, such as a "
              + cite("September 9, 2026 episode", SBM_FEED_URL)
              + " on growing by buying competitors instead of buying ads.",
    consider="Many guests sell to contractors. Recent "
             + cite("episodes", SBM_FEED_URL)
             + " featured people from ClientTether, Driive, CallRail, JobNimbus, Blitzz, and PhoneTap, so some "
             "conversations lean toward a vendor's product. Owners outside the trades will find less here.",
    included="It is an active weekly show for trades owners, a kind of small business where, in our view, "
             "pricing, hiring technicians, and answering the phone decide the margin.",
)

HOW_OF_BUSINESS = dict(
    name="The How of Business",
    site=HOB_APPLE_URL,
    facts=[
        ("Host", "Henry Lopez"),
        ("Format", "Weekly on Mondays, topic episodes and owner interviews, often about 20 to 45 minutes"),
        ("Since", "April 2016"),
        ("Catalog", "More than 620 numbered episodes, plus replays"),
        ("Focus", "How to start, run, grow, and exit a small business"),
    ],
    overview="Henry Lopez alternates between a business topic and an interview with a small business owner "
             "or service provider. The " + cite("show's feed", HOB_FEED_URL)
             + " describes a weekly show for \"aspiring Entrepreneurs and existing Small Business Owners\" on "
             "how to start (including buying a first business), run, and grow a small business. Its first "
             "episodes posted in April 2016, and episode 627, \"Year-End Bookkeeping Best Practices,\" posted "
             "on November 9, 2026.",
    strengths="The mix suits owners who are still learning the basics. Recent "
              + cite("episodes", HOB_FEED_URL)
              + " ran from \"The Time Value of Money\" (October 26, 2026) to \"From Home Kitchen to Seven "
              "Figures with Addison LaBonte\" (October 5, 2026), and \"5 Reasons NOT to Start a Small "
              "Business\" (September 21, 2026) is the kind of honest check, in our view, that a would-be "
              "owner should hear first.",
    consider="It is a one-host show, some weeks are replays of older interviews (marked with an R "
             "in the feed), and some guests are service providers rather than owners.",
    included="Its " + cite("full title", HOB_APPLE_URL)
             + " is the question this list answers, how to start, run, grow, and exit a small business, and it "
             "has published weekly for more than ten years.",
)

# Shared entries, refreshed with this list's November 2026 check.
HUNDRED_MBA = {
    **shows.HUNDRED_MBA,
    "facts": [
        ("Host", "Omar Zenhom, co-founder of WebinarNinja (acquired by ProProfs in 2024)"),
        ("Format", "One lesson per episode, about 22 minutes (2026 median), most 18 to 28, Monday, Wednesday, "
                   "and Friday"),
        ("Catalog", "About 2,890 episodes since August 2014"),
        ("Focus", "Practical lessons for small business owners, with a lean toward online businesses"),
    ],
    "overview": "Business lessons and listener questions on marketing, pricing, hiring, and money. The "
                + cite("show's about page", MBA_ABOUT_URL)
                + " calls it Apple's \"Best of 2014\" podcast and says WebinarNinja, the company host Omar "
                "Zenhom co-founded with Nicole Baldinu, was acquired by ProProfs in 2024. Its "
                + cite("feed", MBA_FEED_URL)
                + " holds about 2,890 episodes, starting with \"What is a Business Anyway?\" on August 11, "
                "2014, and in 2026 posted three a week with a median length of about 22 minutes.",
}

BUILT_TO_SELL = {
    **shows.BUILT_TO_SELL,
    "facts": [
        ("Host", "John Warrillow, author of Built to Sell (Random House, 2011)"),
        ("Format", "Weekly interviews with owners who sold their companies, posted Fridays"),
        ("Catalog", "More than 570 episodes since July 2015"),
        ("Focus", "Building a company buyers want, and the sale itself"),
    ],
}

SIDE_HUSTLE = {
    **shows.SIDE_HUSTLE,
    "facts": [
        ("Host", "Nick Loper"),
        ("Format", "Tactical interviews with people building businesses on the side"),
        ("Catalog", "More than 760 episodes since May 2013"),
        ("Network", "YAP Media"),
        ("Focus", "Starting a small business while keeping a job"),
    ],
    "overview": "Nick Loper interviews people who built side businesses, from online stores to local services, "
                "and asks exactly how they got their first customers. The "
                + cite("show's feed", SIDE_HUSTLE_FEED_URL)
                + " runs from episode 1 on May 16, 2013 to episode 769 on November 5, 2026, now on YAP Media, "
                "and its " + cite("podcast listing", shows.SIDE_HUSTLE_URL)
                + " shows new episodes on November 2 and 5, 2026.",
}

LISTICLE = dict(
    slug="best-small-business-podcasts-2026",
    title_tag="Best Small Business Podcasts 2026: 7 Picks for Owners",
    meta_description="The best small business podcasts in 2026, compared on host, format, and business stage, "
                     "from EntreLeadership to The How of Business. Checked November 2026.",
    headline="The Best Small Business Podcasts in 2026, for Owners and Operators",
    og_description="Seven small business podcasts for starting, running, and growing a company, checked "
                   "November 2026.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when it fits your stage or your trade better. To hear an owner of an "
               "established company, <a href=\"/episodes\">start with any episode</a>.",
    kicker="Podcast picks",
    read_minutes=12,
    h1="The Best Small Business Podcasts in 2026,",
    h1_em="for Owners and Operators",
    answer="<strong>As of November 2026, the best small business podcasts are The Making Of Hosted By Jack "
           "Pitts (our own show, ranked first with disclosure) for hearing owners of established companies "
           "explain how they built them, EntreLeadership for running the business week to week, The How of "
           "Business for learning to start and grow one, and Service Business Mastery for trades and home "
           "service owners.</strong> The $100 MBA Show adds a lesson of about 22 minutes three times a week, "
           "The Side Hustle Show suits owners starting on the side, and Built to Sell Radio shows what makes "
           "a company worth buying. All seven published new episodes in fall 2026.",
    table_heading="Small Business Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other six appear alphabetically. "
                "The stage column shows where in an owner's life each show is most useful.</p>",
    table_columns=["Best for", "Format", "Business stage"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for learning from owners who built and run established private companies.",
        table=["Owners of established companies with employees", "Long-form interview, about an hour",
               "Growing and running"],
        overview_note="Owners might start with <a href=\"/episodes/dave-menz\">Dave Menz</a>, who left a "
                      "17-year corporate job and, with his wife Carla, bought a laundromat that was losing money.",
        why_first="<p><strong>Guests run the kind of company you run.</strong> "
                  "<a href=\"/episodes/gary-dennis\">Gary Dennis</a> built one of the leading car wash "
                  "platforms in the country. <a href=\"/episodes/davies-hood-of-induron-protective-coatings\">"
                  "Davies Hood</a> leads Induron Protective Coatings, a third-generation family business founded "
                  "in 1947. <a href=\"/episodes/kris-carlson\">Kris Carlson</a> leads The Fish Guys, a growing "
                  "food distribution company, and "
                  "<a href=\"/episodes/from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley\">"
                  "Scott Burnley</a> helped build a 140-person pet care business. These are private companies "
                  "with payroll, customers, and real operating problems.</p>\n"
                  "      <p><strong>It is built for the owners who made it past the early years.</strong> Most "
                  "small business shows teach you how to start. This one talks with people who kept going: "
                  "hiring, financing, family dynamics, and growth, so the show stays useful as your company "
                  "gets bigger.</p>\n"
                  "      <p><strong>Questions about what makes a company last.</strong> Jack Pitts co-founded "
                  "Salt Creek Advisory, a sell-side M&amp;A firm, which steers the conversation toward what "
                  "makes a business durable: steady customers, good managers, and an owner who is not the "
                  "bottleneck.</p>",
        choose_another="<p>If you have not started a business yet, The How of Business, The Side Hustle Show, or "
                       "The $100 MBA Show will give you more step-by-step tactics. If you run a trades company, "
                       "Service Business Mastery is more specific to you. The Making Of Hosted By Jack Pitts "
                       "launched in November 2025 and publishes a new episode every few weeks, so its catalog "
                       "is small next to shows with hundreds of episodes.</p>",
    ),
    shows=[
        other_show(**HUNDRED_MBA, pick_line="is best for a short lesson you can act on the same week.",
                   table=["Busy owners who want quick, practical lessons",
                          "Solo lesson, about 22 minutes, three a week", "Starting and running"],
                   strengths="One topic per episode, such as pricing or hiring, three times a week. With "
                             "about 2,890 episodes in its "
                             + cite("feed", MBA_FEED_URL)
                             + ", it has the deepest back catalog on this list, so in our view an owner with a "
                             "specific problem can usually find a lesson on it.",
                   consider="Episodes are lessons, not stories, and its "
                            + cite("site", shows.MBA_URL)
                            + " pitches it at growing a profitable online business, so owners of local or "
                            "trades companies will need to translate. Lessons have also grown longer: the "
                            + cite("feed", MBA_FEED_URL)
                            + " shows a median episode of about 13 to 16 minutes from 2023 through 2025 and "
                            "about 22 minutes in 2026.",
                   included="It is a short-format show for small business owners that has published for "
                            "more than a decade."),
        other_show(**BUILT_TO_SELL, pick_line="is best for owners who want to build a company a buyer would pay for.",
                   table=["Owners who want a more valuable company", "Weekly interview, Fridays",
                          "Running with an exit in mind"],
                   strengths="Even for an owner years from selling, hearing what buyers paid for, and why, is "
                             "a useful checklist for running the business today. Host John Warrillow's book "
                             "Built to Sell, according to his "
                             + cite("about page", BTS_ABOUT_URL)
                             + ", was a top-10 pick for business owners by both Fortune and Inc., and his "
                             + cite("feed", BTS_FEED_URL)
                             + " dates its first episode to July 13, 2015. Episode 571 (November 6, 2026) covered a "
                             "propane distributor that sold in 2022 for 9.5 times EBITDA, when private equity "
                             "buyers were pricing the industry at roughly 5 times.",
                   consider="Nearly every episode is about the exit, so it works best next to a show about "
                            "day-to-day operations.",
                   included="It is the one show here about the end of an owner's journey. For more on that side, "
                            "see our <a href=\"" + BUYING_SELLING_LIST + "\">list of podcasts about buying and "
                            "selling a business</a>."),
        other_show(**ENTRELEADERSHIP, pick_line="is best for short, practical advice on running the business week to week.",
                   table=["Owners who lead a small team", "Short episodes, three a week", "Running and growing"]),
        other_show(**HOW_OF_BUSINESS, pick_line="is best for a weekly, plain-English course in starting and "
                                                "growing a small business.",
                   table=["New and aspiring owners who want the fundamentals",
                          "Weekly topic episode or owner interview", "Starting and growing"]),
        other_show(**SERVICE_BUSINESS_MASTERY, pick_line="is best for owners of HVAC, plumbing, electrical, and other "
                                                         "trades companies.",
                   table=["Home service and trades owners", "Weekly interview, about 45 minutes",
                          "Running and growing"]),
        other_show(**SIDE_HUSTLE, pick_line="is best for starting a business while keeping your job.",
                   table=["Would-be owners with a day job", "Tactical interview", "Starting"],
                   strengths="Concrete, repeatable tactics, with numbers, such as episode 765, \"The $50k/mo "
                             "One-Person Agency\" ("
                             + cite("October 15, 2026", SIDE_HUSTLE_FEED_URL)
                             + "). In our view it is especially useful for someone who has not started yet.",
                   consider="It is aimed at the earliest stage of a business. Owners already running a company "
                            "with employees will outgrow it quickly.",
                   included="It has covered starting a business alongside a job since 2013, which in our view "
                            "is still the lowest-risk way to test whether an idea can become a company."),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        ("Small Business in 2026, by the Numbers",
         "<p>Small business is most of American business. The SBA Office of Advocacy's "
         + cite("2026 small business FAQ", SBA_FAQ_URL)
         + " counts 36,207,130 small businesses, meaning independent firms with fewer than 500 employees. They "
         "make up 99.9% of U.S. firms, employ 45.9% of private-sector workers (62.3 million people), and account "
         "for 43.5% of GDP. Only 21,041 businesses are large.</p>\n"
         "    <p>Most of those businesses are one person. The "
         + cite("same report", SBA_FAQ_URL)
         + " finds that 82.3%, about 29.8 million, have no employees, while 6,395,635 have a payroll. A solo "
         "owner deciding what to sell and an owner managing twenty people face different problems, and they "
         "need different shows.</p>\n"
         "    <p>New owners keep arriving. Summing the Census Bureau's "
         + cite("monthly business application data", BFS_CSV_URL)
         + ", Americans filed 5,696,742 business applications in 2025 (not seasonally adjusted), the most of any "
         "year since the Census series began in mid-2004, ahead of the 2023 total of 5,471,404, and 63% more "
         "than in 2019. January through October 2026 is running about 11% ahead "
         "of the same months of 2025, and the "
         + cite("November 12, 2026 release", BFS_URL)
         + " put October at 501,609 applications, seasonally adjusted. Survival is the harder part: the SBA "
         + cite("reports", SBA_FAQ_URL)
         + " that from 1994 to 2022, on average, 67.7% of new employer establishments lasted two years, 49.2% "
         "lasted five, and 33.9% lasted ten.</p>\n"
         "    <p>That is how we built this list. A good small business podcast matches your stage: the first "
         "two years, when the question is whether the business works at all, or the years after, when the "
         "question is how to run it with other people. The stage column in the table and the guide at the end "
         "match each show to a stage. Owners are already listening: "
         + cite("National Public Media", PODCAST_CONSUMER_URL)
         + ", citing Edison Research, reports that 18% of monthly podcast listeners own a business. If you are "
         "buying or selling a company, see our <a href=\"" + BUYING_SELLING_LIST + "\">podcasts about buying "
         "and selling a business</a> instead.</p>"),
    ],
    sections_after=[
        ("Match the Show to Your Stage",
         "<ul>\n"
         "      <li><strong>Not started yet, or starting on the side:</strong> The Side Hustle Show and The How "
         "of Business.</li>\n"
         "      <li><strong>In the first few years, learning every job yourself:</strong> The $100 MBA Show and "
         "The How of Business.</li>\n"
         "      <li><strong>Running a team and growing:</strong> The Making Of Hosted By Jack Pitts and "
         "EntreLeadership.</li>\n"
         "      <li><strong>Running a trades or home service company:</strong> Service Business Mastery.</li>\n"
         "      <li><strong>Thinking about what the company will be worth:</strong> Built to Sell Radio.</li>\n"
         "    </ul>\n"
         "    <p>Most owners do well with two: one show for the problem in front of you this week, and one "
         "long-form show about an owner who is a few years further down the road.</p>"),
        ("Shows We Checked and Left Off",
         "<p>We checked How I Built This, which in our view is a great listen. We left it off because its "
         + cite("September 2026 announcement", shows.HIBT_PRESS_URL)
         + " frames it as ten years of interviews with \"the world's most successful entrepreneurs,\" mostly "
         "founders of famous brands rather than owners meeting a payroll. It appears on our <a href=\""
         + ENTREPRENEURSHIP_LIST + "\">entrepreneurship podcasts list</a> and is the benchmark for our <a "
         "href=\"" + HIBT_ALTERNATIVES_LIST + "\">podcasts like How I Built This</a>.</p>\n"
         "    <p>We also checked Entrepreneurs on Fire, which posts a founder interview every day. Its "
         + cite("feed", EOFIRE_FEED_URL)
         + " shows that three of its early November 2026 episodes were sponsored by Amazon and recorded at "
         "Amazon's seller conference, and in our view its short daily format suits a quick dose of motivation "
         "more than the operating questions this list is about. We cover it on our How I Built This "
         "alternatives list instead.</p>"),
    ],
    faqs=[
        ("What are the best podcasts for small business owners?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick for owners who "
         "want to hear how other owners built and run established private companies. As of November 2026, "
         "EntreLeadership is best for week-to-week operating advice, The How of Business for learning to start "
         "and grow, Service Business Mastery for trades owners, and The $100 MBA Show for short lessons."),
        ("What small business podcasts do you recommend in 2026?",
         "Match the show to your stage. To start, try The Side Hustle Show or The How of Business. In the first "
         "few years, add The $100 MBA Show. Once you run a team, listen to EntreLeadership and The Making Of "
         "Hosted By Jack Pitts. Trades owners should add Service Business Mastery, and owners thinking about "
         "value should add Built to Sell Radio. All seven released new episodes in fall 2026."),
        ("What podcast should I listen to as a new small business owner?",
         "The How of Business covers the fundamentals of starting, running, and growing a small business every "
         "Monday, and The $100 MBA Show teaches one topic, such as pricing or marketing, three times a week. "
         "EntreLeadership is a good next step once you hire."),
        ("What is a good podcast for running a small business day to day?",
         "EntreLeadership takes one operating problem per short episode every Monday, Wednesday, and Friday. "
         "Owners of HVAC, plumbing, and electrical companies will find Service Business Mastery, published every "
         "Wednesday, more specific to their trade."),
        ("Are there short small business podcasts?",
         "Yes. Most EntreLeadership episodes in 2026 ran 22 minutes or less, with a typical length of about 16 "
         "minutes. The $100 MBA Show runs about 22 minutes (the 2026 median), three times a week."),
        ("Is there a podcast about selling a small business?",
         "Built to Sell Radio interviews owners who sold their companies about price, terms, and what they would "
         "do differently. Our separate list of podcasts about buying and selling a business covers more shows "
         "on that topic."),
        ("How did you pick these small business podcasts?",
         "We looked for shows that speak to owners of real companies at each stage, from starting to running a "
         "team, and checked every feed in November 2026 to confirm each released episodes this fall. Buying and "
         "selling got its own list, so this one stays on running the business. Our own show is first, with "
         "disclosure."),
    ],
    sources=[
        *SHOW_SOURCES,
        PODCAST_CONSUMER_SOURCE,
        *shows.sources_for(shows.HIBT_PRESS_URL, shows.HIBT_FEED_URL),
        ("Libsyn: Entrepreneurs on Fire (podcast feed)", EOFIRE_FEED_URL),
        ("U.S. Small Business Administration, Office of Advocacy: Frequently Asked Questions About Small "
         "Business (2026)", SBA_FAQ_URL),
        ("U.S. Census Bureau: Business Formation Statistics, Current Release (November 12, 2026)", BFS_URL),
        ("U.S. Census Bureau: Business Formation Statistics Monthly Data (CSV)", BFS_CSV_URL),
        *shows.sources_for(shows.MBA_URL, shows.BTS_URL, shows.SIDE_HUSTLE_URL),
        ("The $100 MBA Show: About", MBA_ABOUT_URL),
        ("Simplecast: The $100 MBA Show Podcast Feed", MBA_FEED_URL),
        ("Built to Sell: About John Warrillow", BTS_ABOUT_URL),
        ("Libsyn: Built to Sell Radio Podcast Feed", BTS_FEED_URL),
        ("Ramsey Solutions: The EntreLeadership Podcast", ENTRELEADERSHIP_URL),
        ("Apple Podcasts: EntreLeadership", ENTRELEADERSHIP_APPLE_URL),
        ("Ramsey Network: EntreLeadership Podcast Feed", ENTRELEADERSHIP_FEED_URL),
        ("Libsyn: The How of Business Podcast Feed", HOB_FEED_URL),
        ("Apple Podcasts: The How of Business", HOB_APPLE_URL),
        ("Service Business Mastery: Official Site", SBM_URL),
        ("Service Business Mastery: About the Hosts", SBM_HOSTS_URL),
        ("Service Business Mastery: How Paul Kelly Grew Parker and Sons From $7M to $260M "
         "(September 2026)", SBM_PARKER_URL),
        ("Apple Podcasts: Service Business Mastery", SBM_APPLE_URL),
        ("Libsyn: Service Business Mastery Podcast Feed", SBM_FEED_URL),
        ("YAP Media: The Side Hustle Show Podcast Feed", SIDE_HUSTLE_FEED_URL),
    ],
    episodes_intro="Three owners of real, private companies on how they built them.",
    episodes=[
        ("from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
         "Scott Burnley on building a 140-person pet care business"),
        ("dave-menz", "Dave Menz, the Laundromat Millionaire, on leaving a corporate job to buy a struggling laundromat"),
        ("kris-carlson", "Kris Carlson on leading The Fish Guys, a growing food distributor"),
    ],
)
