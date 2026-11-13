"""Best Podcasts About Buying and Selling a Business in 2026: our disclosed pick, then six more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SOURCES, other_show, our_show
from listicles.shows import cite

# Pages cited only by this list. Facts were checked in November 2026.
BTS_RADIO_URL = "https://builttosell.com/podcast/"
ACQ_MINDS_SITE_URL = "https://acquiringminds.co/"
ACQ_ANON_SITE_URL = "https://www.acquanon.com/"
ACQ_ANON_APPLE_URL = shows.ACQUISITIONS_ANONYMOUS["apple"]
MA_SCIENCE_URL = "https://www.mascience.com/podcast"
MA_SCIENCE_APPLE_URL = "https://podcasts.apple.com/us/podcast/m-a-science/id1203521153"
EXIT_READINESS_URL = ("https://podcasts.apple.com/us/podcast/"
                      "exitreadiness-podcast-exit-planning-succession-selling/id1434897834")
SEARCH_FUNDED_URL = "https://podcasts.apple.com/us/podcast/search-funded-the-eta-podcast/id1655263215"
SEARCH_FUNDED_EPISODES_URL = "https://www.buzzsprout.com/2025469/episodes"
BIZBUYSELL_Q3_URL = "https://finviz.com/news/404656/bizbuysell-releases-q3-2026-insight-report"
MARKET_PULSE_URL = "https://www.webull.com/news/15462423712777216"
BTS_BURNOUT_URL = ("https://podcasts.apple.com/us/podcast/"
                   "ep-553-why-17-5-of-owners-are-burnt-out-and-want-to-sell/id1018988393?i=1000775280413")

# Shared entries, refreshed for this list's sell-side and buy-side angle.
BUILT_TO_SELL = {
    **shows.BUILT_TO_SELL,
    "site": BTS_RADIO_URL,
    "facts": [
        ("Host", "John Warrillow, author of Built to Sell"),
        ("Format", "Weekly long-form interviews with owners who sold, plus buyers and advisors"),
        ("Catalog", "More than 570 episodes"),
        ("Focus", "Raising company value and selling it: valuation, buyer types, earn-outs, life after the sale"),
    ],
    "overview": "John Warrillow interviews owners who sold their companies, along with the buyers and advisors "
                "on the other side, and runs recurring series such as Inside the Mind of an Acquirer, Mastering "
                "the Deal, and After the Deal. The " + cite("show's page", BTS_RADIO_URL)
                + " lists episode 571, published November 6, 2026, in which a distributor sold at 9.5 times "
                "EBITDA after private equity had offered 5 times. The " + cite("episode archive", shows.BTS_URL)
                + " passed 570 episodes in November 2026.",
    "strengths": "In our view, no show on this list stays closer to the owner's side of a sale. Episodes get "
                 "into multiples, earn-outs, rollover equity, and the different ways private equity, "
                 "strategic buyers, and searchers price a company, often with real numbers.",
    "consider": "Nearly every episode is about the exit. If you are years from selling, pair it with a show "
                "about running and growing the company in the meantime.",
    "included": "It is a long-running podcast devoted to owners selling their companies, which makes it the "
                "natural pick for the sell side.",
}

ACQUIRING_MINDS = {
    **shows.ACQUIRING_MINDS,
    "site": ACQ_MINDS_SITE_URL,
    "apple": shows.ACQ_MINDS_URL,
    "facts": [
        ("Host", "Will Smith (per its Apple Podcasts listing)"),
        ("Format", "Interviews with people who bought a small business, about twice a week"),
        ("Focus", "Buying, owning, and operating small businesses"),
    ],
    "overview": "Interviews with people who bought an existing small business, covering how they found it, "
                "financed it, and ran it after closing. The " + cite("official site", ACQ_MINDS_SITE_URL)
                + " calls it a media platform about buying, owning, and operating small businesses, cites a "
                "community of 4,778 acquisition entrepreneurs, and lists recent episodes such as "
                "“She Wanted to Run a Factory, So She Bought One” (November 9, 2026) and "
                "“Run It for 6 Months Before You Buy It” (October 29, 2026).",
    "strengths": "Detailed deal mechanics, such as SBA loans, seller notes, partnerships, and diligence "
                 "surprises, told by the buyers who did the deals.",
    "consider": "It is told from the buyer's side. Owners planning to sell will learn how buyers think, which "
                "is valuable, but it is not sell-side advice.",
    "included": "It is a focused interview show on buying an existing small business, and in our view a "
                "strong starting point for first-time buyers.",
}

ACQUISITIONS_ANONYMOUS = {
    **shows.ACQUISITIONS_ANONYMOUS,
    "site": ACQ_ANON_SITE_URL,
    "facts": [
        ("Hosts", "Michael Girdley, Mills Snell, Bill D'Alessandro, and Heather Endresen"),
        ("Format", "Panel breakdowns of real businesses for sale, about 30 to 45 minutes, twice a week"),
        ("Focus", "Buying, selling, and operating small businesses"),
    ],
    "overview": "Four hosts take a real business listing and debate whether they would buy it and at what "
                "price. The " + cite("show's site", ACQ_ANON_SITE_URL)
                + " introduces the panel: Girdley co-founded Dura Software, Snell is COO of Aqua Seal Roofing "
                "and previously ran a sell-side M&amp;A advisory firm, D'Alessandro founded Elements Brands, "
                "and Endresen has more than 30 years in banking and leads Viso Business Capital. Its "
                + cite("Apple Podcasts listing", ACQ_ANON_APPLE_URL)
                + " shows recent episodes on a mobile RV repair business said to make $105,000 a year and a $23 million "
                "Caribbean construction company.",
    "strengths": "You hear how experienced buyers, an operator, and a lender read the same listing: what "
                 "they trust, what worries them, and what drives price. Useful for owners who will one day "
                 "sell.",
    "consider": "The hosts are reacting to public listings, so the analysis is quick and informal rather than "
                "a full valuation.",
    "included": "It walks through real listings from the buyer's chair twice a week, which makes it useful "
                "on both sides of a deal.",
}

# Shows new to the listicles.
MA_SCIENCE = dict(
    name="M&A Science",
    site=MA_SCIENCE_URL,
    apple=MA_SCIENCE_APPLE_URL,
    facts=[
        ("Host", "Kison Patel, founder and CEO of DealRoom"),
        ("Format", "Weekly practitioner interviews, most about 50 to 70 minutes"),
        ("Catalog", "More than 400 episodes"),
        ("Focus", "How corporate deals get done, from strategy and diligence to integration"),
    ],
    overview="Kison Patel interviews corporate development leaders and deal practitioners about strategy, "
             "sourcing, diligence, valuation, integration, and divestitures. The "
             + cite("show's site", MA_SCIENCE_URL)
             + " lists more than 400 episodes, describes 10 years of practitioner interviews in a February 2026 "
             "episode, and shows a November 12, 2026 episode on how Winsupply runs M&amp;A with four people.",
    strengths="In our view it is a practical, detailed look at the buyer's process inside a company, "
              "including what happens to a business after it is acquired.",
    consider="The audience is corporate development teams, not owners selling a small company. Expect process "
             "and integration detail rather than founder stories.",
    included="It shows how strategic acquirers run deals, which is the buyer many owners eventually sell to.",
)

EXIT_READINESS = dict(
    name="ExitReadiness Podcast",
    site=EXIT_READINESS_URL,
    facts=[
        ("Hosts", "Pat Ennis and Walter Deyhle of ENNIS Legacy Partners"),
        ("Format", "Expert-guest episodes, about 25 to 45 minutes, roughly two a month"),
        ("Catalog", "About 200 episodes"),
        ("Focus", "Exit planning, succession, and selling a business"),
    ],
    overview="Pat Ennis and Walter Deyhle bring on advisors and specialists to walk owners through preparing "
             "for a transition. Its " + cite("Apple Podcasts listing", EXIT_READINESS_URL)
             + " titles it a show on exit planning, succession, and selling your business, with about 200 "
             "episodes and recent ones on a holding company strategy for transferring a business to children "
             "and what leadership teams are not told when their company is acquired.",
    strengths="It covers the years before a sale, such as succession to family, team readiness, and planning, "
              "which deal-focused shows tend to skip.",
    consider="Episodes are advisor-led rather than owner stories, and the hosts run an advisory practice, so "
             "treat it as one firm's point of view.",
    included="It is a dedicated exit-planning show for owners who are preparing to sell or hand off a company.",
)

SEARCH_FUNDED = dict(
    name="Search Funded: The ETA Podcast",
    site=SEARCH_FUNDED_URL,
    facts=[
        ("Host", "Nick Lall"),
        ("Format", "Interviews, about 30 to 45 minutes, with searchers, investors, and operators"),
        ("Focus", "Search funds, self-funded search, and independent sponsors"),
    ],
    overview="Nick Lall talks with people who set out to buy and run a company through entrepreneurship "
             "through acquisition. Its " + cite("Apple Podcasts listing", SEARCH_FUNDED_URL)
             + " shows recent episodes on buying a family business without inheriting it and on moving from "
             "self-funded searcher to institutional investor, and the "
             + cite("episode archive", SEARCH_FUNDED_EPISODES_URL) + " is hosted on Buzzsprout.",
    strengths="It stays on the search fund model specifically, so listeners weighing that path hear from "
              "searchers and the investors who back them.",
    consider="It is a smaller show, with about 40 episodes on Apple Podcasts, and it is aimed at would-be "
             "buyers rather than owners.",
    included="It is a dedicated search fund and ETA show, a buyer type more owners now meet when they sell.",
)

LISTICLE = dict(
    slug="best-podcasts-about-buying-and-selling-a-business-2026",
    title_tag="Best Podcasts About Buying and Selling a Business in 2026",
    meta_description="Seven podcasts on buying and selling a business in 2026, compared on hosts, format, "
                     "and who each suits, from Built to Sell Radio to Acquiring Minds.",
    headline="The Best Podcasts About Buying and Selling a Business in 2026",
    og_description="Seven podcasts on buying and selling a business, compared on hosts, format, and who each suits best.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when it fits your side of the deal better. To hear an owner who sold "
               "twice, <a href=\"/episodes/dave-moorman\">start with Dave Moorman</a>.",
    kicker="Podcast picks",
    read_minutes=12,
    h1="The Best Podcasts About Buying and Selling",
    h1_em="a Business in 2026",
    answer="<strong>The best podcasts about buying and selling a business in 2026 are The Making Of Hosted By "
           "Jack Pitts (our own show, ranked first with disclosure) for how owners built companies worth buying, "
           "Built to Sell Radio for the sale itself, Acquiring Minds for buying a small business, and M&amp;A "
           "Science for corporate deal process.</strong> The Making Of Hosted By Jack Pitts is hosted by the "
           "co-founder of a sell-side M&amp;A firm and, in our view, is the best choice if you want the whole story "
           "of how an owner built a company worth buying.",
    table_heading="Buying and Selling Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other six appear alphabetically.</p>",
    table_columns=["Best for", "Side of the deal", "Format"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for hearing owners explain how they built, grew, and sold real companies, from a "
                  "host who works on sell-side deals.",
        table=["Owners who may sell one day, and buyers who want to know what they are buying",
               "Seller and owner, with growth by acquisition", "Long-form interview, about an hour"],
        overview_note="Start with <a href=\"/episodes/dave-moorman\">Dave Moorman</a>, who grew a managed IT "
                      "company through acquisitions and exited twice.",
        why_first="<p><strong>The host works on sell-side deals for a living.</strong> Jack Pitts co-founded "
                  "Salt Creek Advisory, a sell-side M&amp;A firm, so the questions go where buyers will look: "
                  "margins, customer concentration, key people, debt, and who could run the company without "
                  "the founder.</p>\n"
                  "      <p><strong>You hear the build, not only the exit.</strong> What a buyer pays for is "
                  "decided over years. Episodes such as <a href=\"/episodes/dave-moorman\">Dave Moorman</a> on "
                  "building an MSP, growing through acquisitions, and exiting twice, and "
                  "<a href=\"/episodes/gary-dennis\">Gary Dennis</a> on building Mammoth Holdings into a "
                  "leading car wash platform, follow the whole path.</p>\n"
                  "      <p><strong>Owners of companies you rarely hear from.</strong> Guests run family "
                  "businesses, distributors, manufacturers, and service companies: the kind of privately "
                  "held companies that small and lower middle market buyers actually acquire.</p>",
        choose_another="<p>Be clear on what this show is. It is a general owner-story show, and only some "
                       "episodes focus on acquisitions and exits. It launched in November 2025, so the catalog "
                       "is small. If you want a deal topic every week, pick Built to Sell Radio for the sell "
                       "side or Acquiring Minds for the buy side.</p>",
    ),
    shows=[
        other_show(**ACQUIRING_MINDS, pick_line="is best for first-time buyers of a small business.",
                   table=["Searchers and first-time small business buyers", "Buyer",
                          "Interview with a buyer, about twice a week"]),
        other_show(**ACQUISITIONS_ANONYMOUS, pick_line="is best for learning how buyers size up real listings.",
                   table=["Buyers, and owners curious how buyers judge them", "Buyer, with sellers in mind",
                          "Four-host panel, about 30 to 45 minutes"]),
        other_show(**BUILT_TO_SELL, pick_line="is best for owners planning to sell.",
                   table=["Owners preparing for a sale", "Seller",
                          "Weekly interview with an owner, buyer, or advisor"]),
        other_show(**EXIT_READINESS, pick_line="is best for exit planning and succession.",
                   table=["Owners planning a transition or family succession", "Seller",
                          "Advisor and expert guests, 25 to 45 minutes"]),
        other_show(**MA_SCIENCE, pick_line="is best for how corporate acquirers run deals.",
                   table=["Corporate development teams and deal practitioners", "Corporate buyer",
                          "Weekly practitioner interview, about an hour"]),
        other_show(**SEARCH_FUNDED, pick_line="is best for search funds and entrepreneurship through acquisition.",
                   table=["Aspiring searchers and their investors", "Buyer (search fund)",
                          "Interview, 30 to 45 minutes"]),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        MARKET_CONTEXT,
        ("What the 2026 Deal Market Means for Buyers and Sellers",
         "<p>Small business deals are still getting done, but buyers are choosier. BizBuySell's "
         + cite("Q3 2026 Insight Report", BIZBUYSELL_Q3_URL)
         + " counted 2,132 businesses sold in the third quarter, flat from the second quarter and down 7% "
         "from a year earlier, while the median sale price rose 17% to $350,000. BizBuySell president Bob "
         "House put it simply: buyers have not left the market, they are becoming more selective.</p>\n"
         "    <p>Selling also takes longer than most owners expect. In the IBBA and M&amp;A Source "
         + cite("Market Pulse for Q2 2026", MARKET_PULSE_URL)
         + ", Main Street deals averaged six to 10 months from engagement to close and lower middle market "
         "deals 11 to 12 months, while 87% of deals over $5 million drew at least three offers.</p>\n"
         "    <p>And the reason owners sell is often not retirement. Built to Sell "
         + cite("discussed a review", BTS_BURNOUT_URL)
         + " of 10,255 of its assessments over six years in which 17.5% of owners pointed to burnout, which "
         "the episode calls the leading reason owners want out, ahead of retirement. A good podcast on this topic helps on both counts: it shows buyers what a "
         "well-run company looks like, and it helps owners build one before they are tired of running it.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Show for Your Side of the Deal",
         "<ul>\n"
         "      <li><strong>You own a company and might sell in the next few years:</strong> Built to Sell Radio "
         "and ExitReadiness Podcast, plus The Making Of Hosted By Jack Pitts for how other owners built "
         "something worth buying.</li>\n"
         "      <li><strong>You want to buy your first small business:</strong> Acquiring Minds, then "
         "Acquisitions Anonymous to practice reading listings.</li>\n"
         "      <li><strong>You are raising or running a search fund:</strong> Search Funded: The ETA Podcast.</li>\n"
         "      <li><strong>You work in corporate development:</strong> M&amp;A Science.</li>\n"
         "      <li><strong>You want to grow by acquisition while you own the company:</strong> The Making Of "
         "Hosted By Jack Pitts and Acquiring Minds.</li>\n"
         "    </ul>\n"
         "    <p>Listen to one show from each side. Sellers learn the most from hearing how buyers think, and "
         "buyers learn the most from hearing what owners went through to build the company.</p>"),
    ],
    faqs=[
        ("What is the best podcast about buying and selling a business?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick; it is hosted by "
         "the co-founder of a sell-side M&A firm. Among the others, Built to Sell Radio focuses on owners selling their "
         "companies, Acquiring Minds on people buying small businesses, and Acquisitions Anonymous on how "
         "buyers judge real listings."),
        ("What is a good podcast for business owners who want to sell their company?",
         "Built to Sell Radio interviews owners who sold, along with buyers and advisors. ExitReadiness "
         "Podcast covers exit planning and succession. The Making Of Hosted By Jack Pitts shows how owners "
         "built companies worth buying."),
        ("What is the best podcast for buying a small business?",
         "Acquiring Minds interviews people who bought small businesses about financing and running them. "
         "Acquisitions Anonymous breaks down real listings twice a week, and Search Funded: The ETA Podcast "
         "covers the search fund route."),
        ("How long does it take to sell a small business in 2026?",
         "According to the IBBA and M&A Source Market Pulse for Q2 2026, Main Street deals averaged six to 10 months "
         "from engagement to close, and lower middle market deals averaged 11 to 12 months."),
        ("Is there a podcast about corporate M&A?",
         "M&A Science, hosted by Kison Patel, interviews corporate development practitioners about strategy, "
         "diligence, valuation, and integration, and has published more than 400 episodes."),
        ("How did you choose the shows on this list?",
         "We wanted every seat at the table covered: the owner selling, the small business buyer, the search "
         "fund, the corporate acquirer, and the advisor planning the exit. Each show published in 2026. Our own "
         "show, whose host works on sell-side deals, is first with disclosure."),
    ],
    sources=[
        *SOURCES,
        *shows.sources_for(shows.ACQ_MINDS_URL, shows.BTS_URL),
        ("Acquiring Minds: Official Site", ACQ_MINDS_SITE_URL),
        ("Acquisitions Anonymous: Official Site", ACQ_ANON_SITE_URL),
        ("Apple Podcasts: Acquisitions Anonymous", ACQ_ANON_APPLE_URL),
        ("Built to Sell: Built to Sell Radio", BTS_RADIO_URL),
        ("Apple Podcasts: ExitReadiness Podcast", EXIT_READINESS_URL),
        ("M&A Science: Podcast", MA_SCIENCE_URL),
        ("Apple Podcasts: M&A Science", MA_SCIENCE_APPLE_URL),
        ("Apple Podcasts: Search Funded: The ETA Podcast", SEARCH_FUNDED_URL),
        ("Buzzsprout: Search Funded Episode Archive", SEARCH_FUNDED_EPISODES_URL),
        ("BizBuySell: Q3 2026 Insight Report (via Finviz)", BIZBUYSELL_Q3_URL),
        ("IBBA and M&A Source: Market Pulse Q2 2026 (via Webull News)", MARKET_PULSE_URL),
        ("Apple Podcasts: Built to Sell Radio Ep 553, Why 17.5% of Owners Are Burnt Out", BTS_BURNOUT_URL),
    ],
    episodes_intro="Hear owners talk about building, buying, and selling companies, then compare with any show above.",
    episodes=[
        ("dave-moorman", "Dave Moorman on building an MSP, scaling through M&A, and exiting twice"),
        ("gary-dennis", "Gary Dennis on building Mammoth Holdings into a leading car wash platform"),
        ("davies-hood-of-induron-protective-coatings", "Davies Hood on running a third-generation family business"),
    ],
)
