"""Best Business Podcasts in 2026: our disclosed pick, then seven more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SOURCES, other_show, our_show
from listicles.shows import cite

INFINITE_DIAL_URL = "https://podnews.net/press-release/infinite-dial-us-2026"

DECODER_FEED_URL = "https://feeds.megaphone.fm/recodedecode"
DECODER_APPLE_URL = "https://podcasts.apple.com/us/podcast/decoder-with-nilay-patel/id1011668648"
MARKETPLACE_URL = "https://www.marketplace.org/shows/marketplace"
MARKETPLACE_FEED_URL = "https://feeds.publicradio.org/public_feeds/marketplace"
ODD_LOTS_FEED_URL = ("https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/"
                     "8a94442e-5a74-4fa2-8b8d-ae27003a8d6b/982f5071-765c-403d-969d-ae27003a8d83/podcast.rss")
ODD_LOTS_APPLE_URL = "https://podcasts.apple.com/us/podcast/odd-lots/id1056200096"
ODD_LOTS_QA_URL = "https://omny.fm/shows/odd-lots/tracy-and-joe-answer-all-your-questions"
PROF_G_FEED_URL = "https://feeds.megaphone.fm/WWO6655869236"
PROF_G_APPLE_URL = "https://podcasts.apple.com/us/podcast/the-prof-g-pod-with-scott-galloway/id1498802610"
FORTUNE_VOX_URL = "https://fortune.com/2026/06/29/kara-swisher-pivot-podcast-democrats-2028-influence/"

DECODER = dict(
    name="Decoder with Nilay Patel",
    site="https://www.theverge.com/decoder-podcast-with-nilay-patel",
    apple=DECODER_APPLE_URL,
    facts=[
        ("Host", "Nilay Patel, editor-in-chief of The Verge"),
        ("Format", "Long-form interviews, most about 40 to 80 minutes, two to three a week"),
        ("Network", "The Verge, part of the Vox Media Podcast Network"),
        ("Focus", "How business and technology leaders make decisions"),
    ],
    overview="Nilay Patel, The Verge's editor-in-chief, talks with what the "
             + cite("show's feed", DECODER_FEED_URL)
             + " calls \"a diverse cast of innovators and policymakers at the frontiers of business and "
             "technology.\" Conversations center on strategy, how companies are structured, and how leaders "
             "make decisions. A "
             + cite("November 2026 episode", DECODER_APPLE_URL)
             + " featured Harvard Business School professor Willy Shih on the economics of global supply chains "
             "and the hidden supply chain costs of the AI boom.",
    strengths="Patel asks leaders how their organizations are actually set up and how decisions get made. In "
              "our view that makes it one of the more useful interview shows for anyone who manages people.",
    consider="It leans toward technology companies, policy, and AI. If your business has little to do with "
             "tech, many episodes will feel distant.",
    included="Decoder is an active, well-known interview show about how companies are run, and it adds a "
             "technology lens the other shows here do not.",
)

MARKETPLACE = dict(
    name="Marketplace",
    site=MARKETPLACE_URL,
    apple="https://podcasts.apple.com/us/podcast/marketplace/id201853034",
    facts=[
        ("Host", "Kai Ryssdal, host since 2005"),
        ("Format", "Daily weekday business news program, about 25 minutes"),
        ("Distributor", "American Public Media"),
        ("Focus", "Context on the day's economic and business news"),
    ],
    overview="Marketplace "
             + cite("calls itself", MARKETPLACE_URL)
             + " a \"leading business news radio program and podcast\" focused on \"providing context on the "
             "economic news of the day,\" with \"no econ degree or finance background required.\" Kai Ryssdal "
             "has hosted it since 2005, and American Public Media distributes it. A "
             + cite("November 2026 episode", MARKETPLACE_FEED_URL)
             + " reported that the U.S. added 165,000 jobs in October, more than expected.",
    strengths="It is built for a general audience, so it explains inflation, jobs reports, and interest rates "
              "without assuming you already follow markets.",
    consider="It is a public radio news program first, so episodes cover the whole economy rather than how "
             "individual companies are built or run.",
    included="Marketplace is an active daily business news show with a long-tenured host and a plain-English "
             "approach to the economy.",
)

ODD_LOTS = dict(
    name="Odd Lots",
    site="https://www.bloomberg.com/oddlots",
    apple=ODD_LOTS_APPLE_URL,
    facts=[
        ("Hosts", "Joe Weisenthal and Tracy Alloway"),
        ("Format", "Expert guest conversations, about 30 to 55 minutes, several a week"),
        ("Network", "Bloomberg"),
        ("Focus", "Finance, markets, economics, and the real economy"),
    ],
    overview="Bloomberg's Joe Weisenthal and Tracy Alloway, in the words of the "
             + cite("show's feed", ODD_LOTS_FEED_URL)
             + ", \"explore the most interesting topics in finance, markets and economics.\" Recent "
             + cite("2026 episodes", ODD_LOTS_APPLE_URL)
             + " covered the conditions that hit hedge funds this fall and how New York City collects its "
             "trash, with a deputy commissioner of the city's sanitation department. The hosts also answer "
             "listener questions in a "
             + cite("year-end Q&amp;A episode", ODD_LOTS_QA_URL)
             + ", most recently on January 1, 2026.",
    strengths="The hosts follow an expert down a specific question, whether it is a market event or how a "
              "physical industry works. In our view few shows make the plumbing of the economy this interesting.",
    consider="It assumes some comfort with finance and markets. Listeners new to the subject may find the "
             "pace and vocabulary steep at first.",
    included="Odd Lots is an active, frequently published Bloomberg show and a strong choice for listeners "
             "who want depth on markets and the real economy.",
)

PROF_G = dict(
    name="The Prof G Pod with Scott Galloway",
    site="https://www.profgmedia.com/",
    apple=PROF_G_APPLE_URL,
    facts=[
        ("Host", "Scott Galloway, with guests"),
        ("Format", "Interviews, listener Q&amp;A, and deep dives, most 30 to 65 minutes, new episodes daily"),
        ("Network", "Vox Media Podcast Network (Prof G Media)"),
        ("Focus", "Business, tech, markets, and careers through one host's opinions"),
    ],
    overview="Scott Galloway, an author, professor, and entrepreneur, covers business, tech, markets, and "
             "careers through interviews, listener questions, and deep-dive episodes. The "
             + cite("show's feed", PROF_G_FEED_URL)
             + " says new episodes come out every day of the week and that it is part of the Vox Media Podcast "
             "Network. "
             + cite("Fortune reported", FORTUNE_VOX_URL)
             + " in June 2026 that James Murdoch had acquired Vox Media and brought the podcast network, New York "
             "magazine, and the Vox editorial brand into a single company. A "
             + cite("November 2026 special", PROF_G_APPLE_URL)
             + " on entrepreneurship featured Founders host David Senra.",
    strengths="Galloway is direct and has a clear point of view on markets, big tech, and careers, and the "
              "listener Q&amp;A episodes give practical advice to people early in their working lives.",
    consider="It is built around one host's opinions, which you may or may not share. Treat the predictions "
             "and hot takes as a starting point for your own thinking.",
    included="Prof G is an active daily business show with a distinct voice on markets and careers.",
)

LISTICLE = dict(
    slug="best-business-podcasts-2026",
    title_tag="Best Business Podcasts in 2026: 8 Shows Compared",
    meta_description="Eight business podcasts compared for 2026 on format, hosts, and who each suits best, from "
                     "WSJ's The Journal and Odd Lots to Planet Money and Marketplace.",
    headline="The Best Business Podcasts in 2026: Our Pick and 7 More, Compared",
    og_description="Eight business podcasts compared on format, hosts, and who each one suits best.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pair it with a news show from the list if you also want the day's business headlines. To hear "
               "what our pick sounds like, <a href=\"/episodes\">start with any episode</a>.",
    kicker="Podcast picks",
    read_minutes=11,
    h1="The Best Business Podcasts in 2026:",
    h1_em="Our Pick and 7 More, Compared",
    answer="<strong>The best business podcasts in 2026 are The Making Of Hosted By Jack Pitts (our own show, "
           "ranked first with disclosure) for owner stories, WSJ's The Journal for daily business news, Odd Lots "
           "for markets, and HBR IdeaCast for management.</strong> The Making Of Hosted By Jack Pitts is the best "
           "choice if you want owners of privately held companies explaining how they built and run them. The "
           "full comparison and our method are below.",
    table_heading="Business Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other seven appear alphabetically.</p>",
    table_columns=["Best for", "Format", "Who you hear from"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for hearing how real, privately held companies are built and run, from the owners.",
        table=["Owners, operators, and anyone who wants to run a company", "Long-form interview, most about an hour",
               "The owner who built the company"],
        overview_note="For a view from the top of a large company, try <a href=\"/episodes/alex-dixon\">Alex "
                      "Dixon</a>, who went from Goldman Sachs to CEO of Resorts World Las Vegas.",
        why_first="<p><strong>It covers the part of business most shows skip.</strong> Most business podcasts "
                  "report on public companies, markets, and the economy. This show talks with the owners of "
                  "manufacturers, distributors, franchises, and family companies about the decisions behind "
                  "them: pricing, hiring, debt, partners, and when to sell.</p>\n"
                  "      <p><strong>Questions about how the business makes money.</strong> Because Jack Pitts "
                  "advises owners when they sell, he asks about the numbers a news show never reaches: margins, "
                  "customer concentration, and what a buyer would pay.</p>\n"
                  "      <p><strong>It complements a news show.</strong> A daily news podcast tells you what "
                  "happened to big companies. An hour with one owner shows you how a business works from "
                  "the inside.</p>",
        choose_another="<p>It is a young show, launched in November 2025, so the catalog is small next to "
                       "shows with more than a thousand episodes. If you want daily business headlines, pick "
                       "WSJ's The Journal or Marketplace. If you want markets and economics, pick Odd Lots or "
                       "Planet Money.</p>",
    ),
    shows=[
        other_show(**DECODER, pick_line="is best for how technology and business leaders make decisions.",
                   table=["Managers and tech-curious professionals", "Long-form interview, two to three a week",
                          "CEOs, policymakers, and experts"]),
        other_show(**shows.HBR_IDEACAST, pick_line="is best for one practical management idea a week.",
                   table=["Managers and leaders who want ideas to use at work", "Weekly interview, about 30 minutes",
                          "Researchers and executives"],
                   strengths="Episodes are short and grounded in research, so you get a well-argued management "
                             "idea in about half an hour, a useful counterweight to the news shows here.",
                   consider="Guests are mostly academics and big-company executives. Older episodes were "
                            "co-hosted by Curt Nickisch, so some listings may still name him.",
                   included="It is Harvard Business Review's weekly show and the management pick among the "
                            "business shows here."),
        other_show(**shows.THE_JOURNAL, pick_line=", from The Wall Street Journal, is best for one big business "
                                                  "story a day, explained clearly.",
                   table=["Anyone who wants a short daily business news habit",
                          "Narrative news, about 18 to 30 minutes", "WSJ reporters and the hosts"],
                   strengths="In our view it is a good daily habit: one business story, told by the reporter who "
                             "covered it, short enough for a commute.",
                   consider="Most episodes are about large public companies, markets, and policy rather than how a "
                            "company is built or run day to day.",
                   included="It is the daily news pick: an active weekday show from The Wall Street Journal, "
                            "co-produced with Spotify."),
        other_show(**MARKETPLACE, pick_line="is best for plain-English context on the day's economic news.",
                   table=["General listeners who want the economy explained", "Daily weekday news, about 25 minutes",
                          "The host, reporters, and guests"]),
        other_show(**ODD_LOTS, pick_line="is best for deep dives into markets and the real economy.",
                   table=["Investors and finance-curious listeners", "Expert conversation, several a week",
                          "Economists, investors, and industry experts"]),
        other_show(**shows.PLANET_MONEY, pick_line="is best for economics told as reported stories.",
                   table=["Listeners who want economics made approachable", "Reported narrative, about two a week",
                          "NPR hosts and the people in each story"],
                   strengths="It makes economics approachable by tying each idea to a real business or market, and "
                             "its companion, The Indicator, covers the economy in ten minutes or less.",
                   consider="If you want to know how companies are run, treat it as a supplement: the business "
                            "usually illustrates an economic idea rather than being the subject.",
                   included="It is the economics pick for listeners who want explanation more than market data."),
        other_show(**PROF_G, pick_line="is best for opinionated takes on markets, tech, and careers.",
                   table=["Professionals early or mid career", "Daily mix of interviews and Q&amp;A",
                          "The host and his guests"]),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        MARKET_CONTEXT,
        ("Business News, Big Ideas, or Owner Stories",
         "<p>\"Business podcast\" covers three different kinds of show. <strong>News shows</strong> such as "
         "WSJ's The Journal and Marketplace tell you what happened today. <strong>Idea shows</strong> such as HBR "
         "IdeaCast, Decoder, and Odd Lots go deep on management, strategy, or markets. <strong>Owner "
         "stories</strong> show you how a single company was built and is run. Most listeners do best with one "
         "of each.</p>\n"
         "    <p>The audience is there for all three. "
         + cite("The Infinite Dial 2026", INFINITE_DIAL_URL)
         + " found that 68% of Americans age 35 to 54 consumed a podcast in the last month, and called "
         "podcasting \"a powerful vehicle for reaching one of advertising's most valued demographics.\" Those "
         "are the years when many people manage teams, run companies, or start their own.</p>\n"
         "    <p>Video is changing how people find shows, but not replacing audio. As Megan Lazovick of Edison Research at SSRS "
         "put it in "
         + cite("the same study's release", INFINITE_DIAL_URL)
         + ", \"Video isn't replacing podcast audio. It's expanding the tent.\" Every show on this list works "
         "as audio on a commute.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Show for You",
         "<ul>\n"
         "      <li><strong>You own, run, or want to buy a private company:</strong> The Making Of Hosted By Jack "
         "Pitts.</li>\n"
         "      <li><strong>You want a short daily news habit:</strong> WSJ's The Journal or Marketplace.</li>\n"
         "      <li><strong>You follow markets and the economy:</strong> Odd Lots and Planet Money.</li>\n"
         "      <li><strong>You manage people:</strong> HBR IdeaCast and Decoder with Nilay Patel.</li>\n"
         "      <li><strong>You want opinions on careers, tech, and markets:</strong> The Prof G Pod with Scott "
         "Galloway.</li>\n"
         "    </ul>\n"
         "    <p>Pick one news show and one show about how companies work. The headlines make more sense once you "
         "have heard an owner explain the trade-offs behind them.</p>"),
    ],
    faqs=[
        ("What is the best business podcast in 2026?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick for listeners "
         "who want to hear owners of privately held companies explain how they built and run them. Among the "
         "others, WSJ's The Journal is a strong daily news pick, Odd Lots stands out for markets, and HBR "
         "IdeaCast for management ideas."),
        ("What is a good daily business news podcast?",
         "The Wall Street Journal's The Journal, made with Spotify, tells one business story in about 18 to 30 "
         "minutes, every weekday. Marketplace with Kai Ryssdal covers the day's economic news in "
         "about 25 minutes every weekday."),
        ("What business podcasts are good for learning about the economy?",
         "Planet Money from NPR explains the economy through reported stories, and its companion, The "
         "Indicator, runs Monday through Friday in ten minutes or less. Odd Lots from Bloomberg goes deeper "
         "into finance and markets with expert guests."),
        ("Who hosts The Journal podcast now?",
         "Ryan Knutson and Jessica Mendoza, according to the show's own feed. Founding co-host Kate Linebaugh "
         "said on a March 2025 episode, in a transcript published by Audioscrape, that she was leaving to become "
         "The Wall Street Journal's corporate news editor."),
        ("What is a good business podcast for managers?",
         "HBR IdeaCast from Harvard Business Review offers a weekly interview with a researcher or executive "
         "on management and leadership. Decoder with Nilay Patel asks business and technology leaders how "
         "they structure their companies and make decisions."),
        ("How did you choose the shows on this list?",
         "We picked shows across the three kinds of business podcast, news, ideas, and owner stories, and kept "
         "only those that published in 2026. Each had to be clearly useful to one kind of listener. Our own show "
         "is first, with disclosure; the rest are alphabetical."),
    ],
    sources=[
        *SOURCES,
        ("The Verge: Decoder with Nilay Patel (podcast feed)", DECODER_FEED_URL),
        ("Apple Podcasts: Decoder with Nilay Patel", DECODER_APPLE_URL),
        *shows.sources_for(
            shows.HBR_URL,
            shows.HBR_CHENAULT_URL,
            shows.JOURNAL_FEED_URL,
            shows.JOURNAL_2019_URL,
            shows.JOURNAL_LINEBAUGH_URL,
        ),
        ("Marketplace: About the Show", MARKETPLACE_URL),
        ("American Public Media: Marketplace (podcast feed)", MARKETPLACE_FEED_URL),
        ("Bloomberg: Odd Lots (podcast feed)", ODD_LOTS_FEED_URL),
        ("Apple Podcasts: Odd Lots", ODD_LOTS_APPLE_URL),
        ("Omny: Odd Lots, Tracy and Joe Answer All Your Questions (January 2026)", ODD_LOTS_QA_URL),
        *shows.sources_for(shows.PLANET_MONEY_FEED_URL, shows.PLANET_MONEY_APPLE_URL, shows.INDICATOR_FEED_URL),
        ("Vox Media: The Prof G Pod with Scott Galloway (podcast feed)", PROF_G_FEED_URL),
        ("Apple Podcasts: The Prof G Pod with Scott Galloway", PROF_G_APPLE_URL),
        ("Fortune: Kara Swisher, Pivot, and Vox Media (June 2026)", FORTUNE_VOX_URL),
    ],
    episodes_intro="Hear what an owner-focused business conversation sounds like, then compare it with any show above.",
    episodes=[
        ("alex-dixon", "Alex Dixon on going from Goldman Sachs to CEO of Resorts World Las Vegas"),
        ("dave-moorman", "Dave Moorman on building an MSP, scaling through M&A, and exiting twice"),
        ("from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
         "Scott Burnley on building a pet care business with about 140 employees"),
    ],
)
