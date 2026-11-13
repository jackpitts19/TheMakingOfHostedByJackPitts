"""Best Leadership Podcasts for CEOs and Business Owners in 2026: our disclosed pick, then seven more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SOURCES, other_show, our_show
from listicles.shows import cite

GALLUP_URL = "https://www.gallup.com/workplace/349484/state-of-the-global-workplace.aspx"
CFL_FEED_URL = "https://feeds.podcastmirror.com/coaching-for-leaders"
FS_URL = "https://fs.blog/knowledge-project-podcast/"
FS_FEED_URL = "https://feeds.megaphone.fm/FSMI7575968096"
LL_FEED_URL = "https://rss.libsyn.com/shows/65162/destinations/259291.xml"
LL_URL = "https://learningleader.com/"
WORKLIFE_URL = "https://www.ted.com/podcasts/worklife"
WORKLIFE_HOST_URL = "https://mollyg.substack.com/p/worklife-podcast"
WORKLIFE_FEED_URL = "https://feeds.acast.com/public/shows/67585d9cc705e441796ddaf6"

COACHING_FOR_LEADERS = dict(
    name="Coaching for Leaders",
    site="https://coachingforleaders.com/",
    apple="https://podcasts.apple.com/us/podcast/coaching-for-leaders/id458827716",
    facts=[
        ("Host", "Dr. Dave Stachowiak"),
        ("Format", "Weekly interview on Mondays, about 35 to 40 minutes, with more than 800 numbered episodes"),
        ("Network", "Independent"),
        ("Focus", "Practical management skills: delegation, succession, leading change, hard conversations"),
    ],
    overview="Dave Stachowiak interviews authors and practitioners about one management skill per episode. "
             "The " + cite("show's feed", CFL_FEED_URL) + " says it has been independently produced weekly "
             "since 2011 and reports 50 million downloads and more than 300,000 followers. Stachowiak draws "
             "on a decade leading a global leadership academy and more than 15 years of leadership at Dale "
             "Carnegie. Episode 808, dated 9 November 2026 in the feed, covered finding the person to replace you.",
    strengths="Episode titles name one skill, such as repairing a stakeholder relationship or turning conflict "
              "into progress. In our view the conversations stay on how to do it rather than on the guest's "
              "biography, which makes it one of the more practical leadership feeds for managers moving into "
              "bigger roles.",
    consider="It is a skills show, not a story show, so you will not hear how a company was built. Most recent "
              "guests are authors and consultants rather than owners, so you will need to apply the lessons to "
              "your own business.",
    included="It has published weekly since 2011 and regularly covers topics owners face, such as delegation "
             "and succession.",
)

KNOWLEDGE_PROJECT = dict(
    name="The Knowledge Project",
    site=FS_URL,
    apple="https://podcasts.apple.com/us/podcast/the-knowledge-project/id990149481",
    facts=[
        ("Host", "Shane Parrish"),
        ("Format", "Long-form interview, usually released on Tuesdays, plus Outliers episodes, many on figures from business history"),
        ("Network", "Farnam Street"),
        ("Focus", "Decision-making and mental models from operators, CEOs, and investors"),
    ],
    overview="Shane Parrish talks with operators and investors about how they think and decide. "
             + cite("Farnam Street describes it", FS_URL) + " as a business and leadership interview podcast "
             "with operators, CEOs, investors, and thinkers, and lists recent guests including Shopify's Tobi Lütke, Roblox CEO "
             "David Baszucki, Bill Ackman, and Brad Jacobs. The "
             + cite("10 November 2026 episode", FS_FEED_URL) + " featured Jon McNeill on how Elon Musk solves "
             "problems.",
    strengths="Parrish asks how a guest makes decisions rather than only what they decided, which makes the "
              "lessons portable to a company of any size. In our view it suits leaders who like to think in "
              "frameworks.",
    consider="Episodes are long and often abstract. Guests are mostly leaders of large or famous companies, so "
             "there is little on the day-to-day of running a small business.",
    included="It is an active interview show built around decision-making, a core part of any CEO's job.",
)

LEARNING_LEADER = dict(
    name="The Learning Leader Show with Ryan Hawk",
    site=LL_URL,
    apple="https://podcasts.apple.com/us/podcast/the-learning-leader-show-with-ryan-hawk/id985396258",
    facts=[
        ("Host", "Ryan Hawk"),
        ("Format", "Weekly long-form interview, 714 numbered episodes as of November 2026"),
        ("Network", "Independent"),
        ("Focus", "Leadership development through conversations with CEOs, coaches, and athletes"),
    ],
    overview="Ryan Hawk interviews entrepreneurs, CEOs, athletes, coaches, and authors about how they lead. "
             "Episode 713, released 2 November 2026 according to the " + cite("show's feed", LL_FEED_URL)
             + ", featured Ken Chenault on lessons from 17 years as CEO of American Express. "
             + cite("Hawk's site", LL_URL) + " cites more than 700 conversations, with guests including Jim "
             "Collins, Kat Cole, Simon Sinek, and Tony Robbins.",
    strengths="Guests are asked about the habits and decisions behind their results, which gives you something "
              "to borrow. In our view it is a steady show for leaders who want one thoughtful conversation a week.",
    consider="Guests come from many fields, including sports and publishing, so not every episode is about "
             "running a business.",
    included="It is an active weekly show centered on leadership, with a long run of CEO interviews.",
)

WORKLIFE = dict(
    name="WorkLife with Molly Graham",
    site=WORKLIFE_URL,
    apple="https://podcasts.apple.com/us/podcast/worklife-with-molly-graham/id1346314086",
    facts=[
        ("Host", "Molly Graham, since April 2026 (the show was created by Adam Grant)"),
        ("Format", "Weekly episode on Tuesdays, mostly interviews, with occasional episodes shared from other shows"),
        ("Network", "TED Audio Collective"),
        ("Focus", "The human side of work and of leading a growing organization"),
    ],
    overview="Molly Graham " + cite("announced on 14 April 2026", WORKLIFE_HOST_URL) + " that she was taking "
             "over WorkLife, the show Adam Grant created with TED eight years earlier. "
             + cite("TED's host bio", WORKLIFE_URL) + " says she led operations at Facebook, Quip, and the "
             "Chan Zuckerberg Initiative and is known for the Give Away Your Legos framework about how a "
             "leader's role changes as an organization grows. " + cite("Recent episodes", WORKLIFE_FEED_URL)
             + " include Astro Teller on failing at work and Wendy Chow on negotiating.",
    strengths="Graham's experience scaling teams gives owners a useful lens on handing off work they used to do "
              "themselves. In our view that idea alone is worth the time for a founder who has become the "
              "bottleneck.",
    consider="Many episodes are aimed at employees and managers rather than owners. Older listings and "
             "articles that describe it as Adam Grant's show are out of date.",
    included="It is an active TED show on leadership and work, and its new host brings a scaling perspective "
             "that fits growing companies.",
)

LISTICLE = dict(
    slug="best-leadership-podcasts-for-ceos-and-owners-2026",
    title_tag="Best Leadership Podcasts for CEOs and Owners (2026)",
    meta_description="Eight leadership podcasts for CEOs and business owners in 2026, compared on format, "
                     "hosts, and who each suits best, from HBR IdeaCast to Coaching for Leaders.",
    headline="The Best Leadership Podcasts for CEOs and Business Owners in 2026",
    og_description="Eight leadership podcasts for CEOs and owners compared on format, hosts, and who each suits best.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when you want research, frameworks, or management skills instead. To "
               "hear how owners actually lead their companies, <a href=\"/episodes\">start with any episode</a>.",
    kicker="Podcast picks",
    read_minutes=11,
    h1="The Best Leadership Podcasts for CEOs and",
    h1_em="Business Owners in 2026",
    answer="<strong>The best leadership podcasts for CEOs and business owners in 2026 are The Making Of Hosted "
           "By Jack Pitts (our own show, ranked first with disclosure) for how owners lead private companies, HBR "
           "IdeaCast for research-backed management, Coaching for Leaders for skills like delegation, and The "
           "Knowledge Project for decision-making.</strong> The Making Of Hosted By Jack Pitts is the best choice "
           "for owners who want to hear how other owners handle hiring, growth, and succession.",
    table_heading="Leadership Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other seven appear alphabetically.</p>",
    table_columns=["Best for", "Format", "Who you hear from"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for owners who want to hear how other owners lead their companies.",
        table=["Owners and CEOs of privately held companies", "Long-form interview, about an hour",
               "The owner who built and runs the company"],
        overview_note="For leadership across generations, try <a href=\"/episodes/davies-hood-of-induron-"
                      "protective-coatings\">Davies Hood</a>, who leads a third-generation family manufacturer.",
        why_first="<p><strong>Leadership as owners actually practice it.</strong> Many leadership shows feature "
                  "professors, authors, and executives of very large companies. This show talks with the people "
                  "who sign the payroll at manufacturers, distributors, franchises, and family businesses, and "
                  "asks how they hired, delegated, handled partners, and kept people through hard years.</p>\n"
                  "      <p><strong>Leadership questions a buyer would ask.</strong> Because Jack Pitts advises "
                  "owners when they sell, he asks whether the business runs without the owner, who the next "
                  "leaders are, and how succession will work.</p>\n"
                  "      <p><strong>Whole stories, not tips.</strong> Episodes run about an hour, which leaves room "
                  "to hear how a leader's role changed from founder doing everything to owner running a team.</p>",
        choose_another="<p>It is a young show, launched in November 2025, and it is a conversation show, not a "
                       "management course. If you want research and frameworks, pick HBR IdeaCast or The "
                       "Knowledge Project. If you want a specific skill each week, pick Coaching for Leaders.</p>",
    ),
    shows=[
        other_show(**COACHING_FOR_LEADERS, pick_line="is best for practical management skills you can use this week.",
                   table=["Managers and owners stepping into bigger roles", "Weekly interview on one skill",
                          "Authors, coaches, and practitioners"]),
        other_show(**shows.DIARY_OF_A_CEO, pick_line="is best for long, personal conversations that go well beyond leadership.",
                   table=["Leaders who want the personal side of the job", "Long-form interview, often around two hours",
                          "Founders, experts, and public figures"],
                   strengths="For leaders, its value is in candid conversations about pressure, burnout, and "
                             "failure, the personal side of running a company that management shows rarely touch.",
                   consider="Episodes often run about two hours, and many are about health and psychology rather "
                            "than leading people, so choose by guest.",
                   included="Its host is an entrepreneur, and its conversations with founders often turn to how "
                            "they lead and what it cost them."),
        other_show(**shows.HBR_IDEACAST, pick_line="is best for research-backed management ideas in about half an hour.",
                   table=["Leaders who want the research behind a practice", "Weekly interview, about 30 minutes",
                          "Researchers and executives"],
                   strengths="In our view it is a good habit for leaders who want the research behind a practice, "
                             "not just the practice, and the hosts press guests on what to do differently.",
                   consider="Owners of small and mid-sized companies will need to translate findings from large "
                            "organizations to a business without layers of management.",
                   included="It covers leadership as research sees it, which complements the practitioner "
                            "conversations elsewhere on this list."),
        other_show(**KNOWLEDGE_PROJECT, pick_line="is best for how experienced operators make decisions.",
                   table=["CEOs who think in frameworks", "Long-form interview",
                          "Operators, CEOs, and investors"]),
        other_show(**LEARNING_LEADER, pick_line="is best for one thoughtful leadership conversation a week.",
                   table=["Leaders building their own habits", "Weekly long-form interview",
                          "CEOs, entrepreneurs, coaches, and athletes"]),
        other_show(**shows.MASTERS_OF_SCALE, pick_line="is best for how CEOs lead companies through growth.",
                   table=["Leaders of companies that are scaling", "CEO interview, about 30 minutes",
                          "CEOs and venture-backed founders"],
                   strengths="In our view its best episodes show how a leader's job changes as a company grows, "
                             "from doing the work to building the team that does it.",
                   consider="Guests skew toward venture-backed and large-company leaders, so the scale is often "
                            "far from a private company with fifty employees.",
                   included="It focuses on leading through growth, the stage where many owners struggle to let "
                            "go of work."),
        other_show(**WORKLIFE, pick_line="is best for the people side of leading a growing team.",
                   table=["Founders handing off work as the company grows", "Weekly interview",
                          "Executives, authors, and operators"]),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        MARKET_CONTEXT,
        ("Why Leadership Skills Matter More in 2026",
         "<p>The case for spending an hour a week on leadership is in the numbers. Gallup's "
         + cite("State of the Global Workplace: 2026 Report", GALLUP_URL)
         + " puts global employee engagement at 20% in 2025, the lowest since 2020. Manager engagement has "
         "fallen nine points since 2022, to 22% in 2025, including a five-point drop from 2024.</p>\n"
         "    <p>Gallup estimates that low engagement cost the world economy about $10 trillion in lost "
         "productivity in 2025, roughly 9% of global GDP. In a small or mid-sized company, the owner is often "
         "the manager whose engagement sets the tone for everyone else.</p>\n"
         "    <p>That is why the shows below are judged on whether they help a leader act differently on Monday "
         "morning, not on how famous their guests are.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Leadership Podcast",
         "<ul>\n"
         "      <li><strong>You own or run a private company:</strong> The Making Of Hosted By Jack Pitts, then "
         "Coaching for Leaders for specific skills.</li>\n"
         "      <li><strong>You want the research behind good management:</strong> HBR IdeaCast.</li>\n"
         "      <li><strong>You want to make better decisions:</strong> The Knowledge Project.</li>\n"
         "      <li><strong>You are scaling and need to let go of work:</strong> WorkLife with Molly Graham and "
         "Masters of Scale.</li>\n"
         "      <li><strong>You want a weekly habit of leadership conversations:</strong> The Learning Leader Show "
         "with Ryan Hawk.</li>\n"
         "      <li><strong>You want broader personal growth:</strong> The Diary of a CEO.</li>\n"
         "    </ul>\n"
         "    <p>Pair one show about how real owners lead with one show about a skill or idea. Stories show you "
         "what good leadership looks like; skills shows help you practice it.</p>"),
    ],
    faqs=[
        ("What is the best leadership podcast for CEOs in 2026?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick for owners and "
         "CEOs who want to hear how leaders of privately held companies actually run them. Among the others, HBR IdeaCast "
         "covers research-backed management, The Knowledge Project focuses on decision-making, and Coaching for "
         "Leaders teaches one practical skill per episode."),
        ("What is a good leadership podcast for small business owners?",
         "The Making Of Hosted By Jack Pitts interviews founders and owners, mostly of privately held, operating companies, about "
         "hiring, delegation, and succession. Coaching for Leaders covers practical management skills such as "
         "delegation and finding the person to replace you."),
        ("Who hosts HBR IdeaCast now?",
         "Harvard Business Review lists Alison Beard, an executive editor, and Adi Ignatius, its editor at "
         "large, as the hosts of HBR IdeaCast."),
        ("Is Adam Grant still the host of WorkLife?",
         "No. Molly Graham announced on her Substack on April 14, 2026 that she was taking over as host of "
         "WorkLife, the TED show Adam Grant created, and TED's show page now carries her host bio."),
        ("Which leadership podcasts have short episodes?",
         "HBR IdeaCast episodes run about 25 to 35 minutes, and Coaching for Leaders interviews run about 35 to "
         "40 minutes. The Knowledge Project, The Learning Leader Show, and The Diary of a "
         "CEO are long-form."),
        ("How did you choose the shows on this list?",
         "We asked whether each show helps a leader act differently on Monday morning, not how famous its guests "
         "are, and kept only shows that published in 2026. The list mixes skills, research, decisions, and owner "
         "stories. Our own show is first, with disclosure."),
    ],
    sources=[*SOURCES, *shows.sources_for(shows.DOAC_URL, shows.HBR_URL, shows.HBR_CHENAULT_URL, shows.MOS_URL, shows.MOS_FEED_URL),
             ("Gallup: State of the Global Workplace 2026 Report", GALLUP_URL),
             ("Coaching for Leaders: Official Podcast Feed", CFL_FEED_URL),
             ("Farnam Street: The Knowledge Project Podcast", FS_URL),
             ("Farnam Street: The Knowledge Project Podcast Feed", FS_FEED_URL),
             ("The Learning Leader Show: Official Podcast Feed", LL_FEED_URL),
             ("Learning Leader: Official Site", LL_URL),
             ("TED: WorkLife with Molly Graham", WORKLIFE_URL),
             ("Molly Graham: WorkLife Podcast Announcement (April 2026)", WORKLIFE_HOST_URL),
             ("Acast: WorkLife with Molly Graham Feed", WORKLIFE_FEED_URL)],
    episodes_intro="Hear how owners describe leading their own companies, then compare it with any show above.",
    episodes=[
        ("from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
         "Scott Burnley on leading a pet care business to about 140 employees"),
        ("alex-dixon", "Alex Dixon on going from Goldman Sachs to CEO of Resorts World Las Vegas"),
        ("davies-hood-of-induron-protective-coatings",
         "Davies Hood on leading a third-generation family manufacturer"),
    ],
)
