"""Best storytelling podcasts about business in 2026: our disclosed pick, then seven more A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, MARKET_CONTEXT, SOURCES, other_show, our_show
from listicles.shows import cite

# Sources new to this list (shows.py covers the rest).
BREAKDOWNS_SITE = "https://colossus.com/series/business-breakdowns/"
BREAKDOWNS_FEED = "https://feeds.megaphone.fm/breakdowns"
BREAKDOWNS_AFFIRM = "https://colossus.com/episode/affirm-the-internets-american-express/"
FREAKONOMICS_SITE = "https://freakonomics.com/series/freakonomics-radio/"
FREAKONOMICS_ABOUT = "https://freakonomics.com/about/"
FREAKONOMICS_FEED = "https://feeds.simplecast.com/Y8lFbOT4"
INFINITE_DIAL_NPM = ("https://www.nationalpublicmedia.com/insights/articles/audio-continues-to-break-"
                     "listening-records-2026-infinite-dial-report/")
INFINITE_DIAL_URL = "https://podnews.net/press-release/infinite-dial-us-2026"
ENGADGET_WONDERY = ("https://www.engadget.com/big-tech/amazon-splits-up-the-wondery-podcast-network-and-lays-"
                    "off-about-110-employees-185358357.html")

NEW_SOURCES = [
    ("Colossus: Business Breakdowns Series Page", BREAKDOWNS_SITE),
    ("Megaphone: Business Breakdowns Podcast Feed", BREAKDOWNS_FEED),
    ("Colossus: Affirm, The Internet's American Express (EP.249)", BREAKDOWNS_AFFIRM),
    ("Freakonomics: About", FREAKONOMICS_ABOUT),
    ("Simplecast: Freakonomics Radio Podcast Feed", FREAKONOMICS_FEED),
    ("National Public Media: Audio Continues to Break Listening Records, 2026 Infinite Dial", INFINITE_DIAL_NPM),
    ("Engadget: Amazon Splits Up the Wondery Podcast Network (August 2025)", ENGADGET_WONDERY),
]

BUSINESS_BREAKDOWNS = dict(
    name="Business Breakdowns",
    site=BREAKDOWNS_SITE,
    apple="https://podcasts.apple.com/us/podcast/business-breakdowns/id1559120677",
    facts=[
        ("Hosts", "Matt Reustle and Zack Fuss, per the series page; some 2026 episodes have other hosts"),
        ("Format", "Interview with an investor or operator about one company, often about an hour"),
        ("Network", "Colossus"),
        ("Focus", "How one business works: origins, model, financials, and edge"),
    ],
    overview="Each episode takes one company apart with a guest who knows it well. The "
             + cite("show's feed", BREAKDOWNS_FEED)
             + " says every episode \"dissects a single business,\" from its origins and model to its "
               "financials and competitive edge. The " + cite("Colossus series page", BREAKDOWNS_SITE)
             + " describes Matt Reustle as the CEO of Colossus and Zack Fuss as the Chief Investment Officer "
               "of a single family office. " + cite("EP.249 on Affirm", BREAKDOWNS_AFFIRM)
             + ", released in October 2026, was hosted by Avidan Rudansky.",
    strengths="In our view it is one of the clearest ways to understand why a company makes money, "
              "with a guest who has studied the numbers rather than a narrator summarizing them.",
    consider="It is more analysis than story. The founding tale usually gets a few minutes before the "
             "conversation turns to economics and competition, and new episodes came less often in 2026.",
    included="It complements the narrative shows here: once a story hooks you on a company, this is where "
             "you learn how the business underneath actually works.",
)

FREAKONOMICS_RADIO = dict(
    name="Freakonomics Radio",
    site=FREAKONOMICS_SITE,
    apple="https://podcasts.apple.com/us/podcast/freakonomics-radio/id354668519",
    facts=[
        ("Host", "Stephen J. Dubner"),
        ("Format", "Weekly reported documentary and interview episodes, often in multi-part series"),
        ("Since", "2010"),
        ("Network", "Freakonomics Radio Network, produced with Stitcher (SiriusXM)"),
    ],
    overview="Stephen J. Dubner reports stories about economics and what the show's feed calls the hidden side "
             "of everything. " + cite("Freakonomics.com", FREAKONOMICS_ABOUT)
             + " says the podcast began in 2010 and that the network's shows are produced in partnership with "
               "Stitcher, the podcast production arm of SiriusXM. Its "
             + cite("feed", FREAKONOMICS_FEED)
             + " shows episode 694 released in November 2026, right after a two-part series on A.I. and human "
               "creativity.",
    strengths="The reporting is careful and the storytelling is patient. In our view it is a good habit "
              "for anyone who wants to think more clearly about prices, markets, and decisions.",
    consider="Many episodes are not about business at all. Recent topics include politics and creativity, "
             "so expect company stories only some weeks.",
    included="It is an established economics storytelling show, and its business episodes pair well with "
             "the company-focused picks on this list.",
)

LISTICLE = dict(
    slug="best-storytelling-podcasts-about-business-2026",
    title_tag="Best Storytelling Podcasts About Business (2026)",
    meta_description="Eight narrative business podcasts for 2026, from company histories to dramatized "
                     "rivalries and reported news, compared on format, length, and who each suits.",
    headline="The Best Storytelling Podcasts About Business in 2026, From Company Histories to Rivalries",
    og_description="Eight narrative business podcasts compared on format, length, and who each one suits.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when you want a different kind of story. To hear an owner tell their own, "
               "<a href=\"/episodes\">start with any episode</a>.",
    kicker="Podcast picks",
    read_minutes=11,
    h1="The Best Storytelling Podcasts About Business in 2026,",
    h1_em="From Company Histories to Rivalries",
    answer="<strong>The best storytelling podcasts about business in 2026 are The Making Of Hosted By Jack Pitts "
           "(our own show, ranked first with disclosure) for owners telling their own stories, Acquired for "
           "the full history of a famous company, Business Wars for dramatized rivalries, and Planet Money for "
           "short reported stories about the economy.</strong> The Making Of Hosted By Jack Pitts is the best "
           "choice if you want the story of a real, privately held company from the person who built it.",
    table_heading="Business Storytelling Podcasts at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other seven appear alphabetically. "
                "The last column says who tells the story.</p>",
    table_columns=["Best for", "Format", "Who tells the story"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is best for founder stories told firsthand by owners of privately held companies.",
        table=["Listeners who want the whole story of a real company, from the person who built it",
               "Long-form interview, about an hour",
               "The owner, in their own words"],
        overview_note="For a story told start to finish, try <a href=\"/episodes/melissa-banko\">Melissa "
                      "Banko</a> on growing a design firm from a spare bedroom.",
        why_first="<p><strong>The story comes from the person who lived it.</strong> Many business storytelling "
                  "shows have a narrator or reporter retell what happened. Here the owner tells it: the first "
                  "customers, the money, the hires, and the bad years.</p>\n"
                  "      <p><strong>Stories you have not heard before.</strong> Famous companies get told and "
                  "retold. This show's guests run design firms, bourbon brands, pet care companies, "
                  "and family manufacturers, so the stories are new and closer to the businesses most people "
                  "work in.</p>\n"
                  "      <p><strong>Stories with a second act.</strong> Most business stories stop at the "
                  "breakthrough. Because Jack Pitts advises owners on selling their companies, he keeps going: "
                  "what the business became, who runs it now, and where it goes next.</p>",
        choose_another="<p>It is an interview show, not a scripted production, and it launched in November 2025, "
                       "so the catalog is small. If you want sound design and dramatized scenes, pick Business "
                       "Wars. If you want a famous company's full history, pick Acquired. If you want short "
                       "reported stories, pick Planet Money or WSJ's The Journal.</p>",
    ),
    shows=[
        other_show(**shows.ACQUIRED, pick_line="is best for the complete, researched story of one famous company.",
                   table=["Business history fans with time to spare", "Long-form narrative, two hosts",
                          "The hosts, from their research"],
                   strengths="The craft is the draw: two hosts build a company's history like a long nonfiction "
                             "book, with clear acts, turning points, and deep research.",
                   consider="Episodes often run several hours, which is a commitment even for history fans, and "
                            "the subjects are almost always large, famous companies.",
                   included="It is the long-form narrative history on this list, told from research rather than "
                            "from memory."),
        other_show(**BUSINESS_BREAKDOWNS, pick_line="is best for understanding how one business actually makes money.",
                   table=["Investors and operators who want the numbers behind the story",
                          "Interview about one company, about an hour",
                          "An investor or operator who studied the company"]),
        other_show(**shows.BUSINESS_WARS, pick_line="is best for dramatized stories of corporate rivalries.",
                   table=["Listeners who want story first, like a drama series", "Scripted, dramatized narrative arcs",
                          "A narrator, with scripted scenes and sound design"],
                   strengths="It is built like a drama series, with multi-part arcs, scripted scenes, and sound "
                             "design, which makes it easy listening even for people who do not usually choose "
                             "business shows.",
                   consider="Dramatized dialogue is a reconstruction rather than a record, so treat the scenes as "
                            "storytelling, not transcripts.",
                   included="It is the most heavily produced format on the list, and an example of the premium "
                            "narrative shows now moving to Audible."),
        other_show(**FREAKONOMICS_RADIO, pick_line="is best for economics stories that sometimes center on business.",
                   table=["Curious listeners who like economics and big ideas",
                          "Weekly reported episodes, often multi-part",
                          "The host, with experts and reporting"]),
        other_show(**shows.HOW_I_BUILT_THIS, pick_line="is best for interviews edited into a story with a beginning, "
                                                       "a crisis, and a turn.",
                   table=["Anyone curious how famous brands started", "Produced founder interview",
                          "The founder, shaped into a narrative arc"],
                   strengths="The editing is the craft: a long interview is shaped into a story with a beginning, a "
                             "crisis, and a turning point, and it closes by asking how much was skill and how much "
                             "was luck.",
                   consider="Because the story is edited into an arc, it can look tidier than it was, and the "
                            "guests are mostly founders of famous consumer brands.",
                   included="It sits between a firsthand interview and a narrated history: the founder's own "
                            "words, arranged by a producer into a story."),
        other_show(**shows.THE_JOURNAL, pick_line=", from The Wall Street Journal, is best for the story behind a "
                                                  "business headline, every weekday.",
                   table=["Busy listeners who follow business news", "Daily narrative, about 18 to 30 minutes",
                          "A host and the reporter who covered it"],
                   strengths="In our view it is one of the best examples of narrative news: a reporter walks you "
                             "through what happened, with tape, in under half an hour.",
                   consider="It follows the news, so the subjects are mostly large public companies, markets, and "
                            "policy, and the story comes from reporters rather than the people involved.",
                   included="It brings narrative storytelling to the day's business headlines, every weekday."),
        other_show(**shows.PLANET_MONEY, pick_line="is best for short stories that explain the economy through businesses.",
                   table=["Commuters who want a lesson in each story", "Reported narrative, about 20 to 35 minutes",
                          "NPR reporters"],
                   strengths="It is good at finding a small, specific story, a single shop or product, and using "
                             "it to explain something bigger about the economy.",
                   consider="The business is often the example rather than the subject, and the feed mixes new "
                            "episodes with reruns of older ones.",
                   included="It is NPR's long-running reported storytelling show about money and the economy."),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        MARKET_CONTEXT,
        ("Why Business Storytelling Podcasts Matter in 2026",
         "<p>In our view, stories are how most people remember business lessons. A margin percentage fades, but the owner "
         "who started out selling ice or the four veterans who started a bourbon brand stays with you. And "
         "the podcast audience those stories reach keeps growing. "
         + cite("National Public Media's summary of the 2026 Infinite Dial", INFINITE_DIAL_NPM)
         + " calls 58% monthly and 45% weekly podcast listening among Americans record levels. "
         + cite("Edison Research found", INFINITE_DIAL_URL)
         + " that listeners 55 and older are driving the growth: monthly online audio listening in that group "
           "rose from 52% in 2024 to 70% in 2026.</p>\n"
         "    <p>The business of narrative shows is changing too. In August 2025, "
         + cite("Engadget reported", ENGADGET_WONDERY)
         + " that Amazon was splitting up Wondery and that its more narrative-focused podcasts, including "
           "Business Wars, would merge with Amazon's Audible team. In our view that is a sign that heavily "
           "produced storytelling is moving toward "
           "premium, subscription-backed homes.</p>\n"
         "    <p>Business storytelling comes in three main forms. Narrated shows retell a company's story from "
         "research. Reported shows follow a journalist through one story. Interview shows let the founder tell "
         "it firsthand. We think the best listening mix includes at least two of the three.</p>"),
    ],
    sections_after=[
        ("How to Choose the Right Storytelling Show",
         "<ul>\n"
         "      <li><strong>You want the story from the person who lived it:</strong> The Making Of Hosted By "
         "Jack Pitts for owners of private companies, How I Built This for well-known brands.</li>\n"
         "      <li><strong>You want a famous company's full history:</strong> Acquired.</li>\n"
         "      <li><strong>You want drama and sound design:</strong> Business Wars.</li>\n"
         "      <li><strong>You have half an hour and want a reported story:</strong> WSJ's The Journal for "
         "business news, Planet Money for the economics behind it.</li>\n"
         "      <li><strong>You want the numbers behind the story:</strong> Business Breakdowns.</li>\n"
         "      <li><strong>You like big ideas about incentives and markets:</strong> Freakonomics Radio.</li>\n"
         "    </ul>\n"
         "    <p>Pair a firsthand founder show with one narrated or reported show. Hearing a story from the "
         "person who lived it and from someone looking in from outside gives a truer picture than either "
         "alone.</p>"),
    ],
    faqs=[
        ("What is the best storytelling podcast about business?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick for listeners "
         "who want owners of privately held companies telling their own stories. Among the others, Acquired "
         "tells the full history of famous companies, Business Wars dramatizes corporate rivalries, and Planet "
         "Money explains the economy through short reported stories."),
        ("What are the best business history podcasts?",
         "Acquired tells the full, researched history of one famous company per episode, and Business Wars "
         "dramatizes long rivalries between companies. Business Breakdowns takes one company apart with an "
         "investor or operator who has studied it."),
        ("Is Business Wars still made by Wondery?",
         "Business Wars was created by Wondery. Engadget reported in August 2025 that Amazon was splitting up "
         "Wondery and moving its narrative shows, including Business Wars, to Audible, and the show's Apple "
         "Podcasts listing now carries it as an Audible Original. David Brown hosts it."),
        ("What is a good short business story podcast?",
         "WSJ's The Journal tells the story behind one business news item in about 18 to 30 minutes each "
         "weekday, and Planet Money runs about 20 to 35 minutes and explains the economy through stories about "
         "businesses."),
        ("Are there narrative business podcasts like a documentary?",
         "Yes. Business Wars is a scripted, dramatized series told in multi-episode arcs, Acquired tells long "
         "researched company histories, and Freakonomics Radio produces reported documentary episodes, often in "
         "multi-part series."),
        ("How did you choose the shows on this list?",
         "We wanted one strong example of each way to tell a business story: firsthand interview, edited "
         "interview, narrated history, dramatized series, and reported news, each released in 2026. Our own show "
         "is first, with disclosure, and every fact about the others links to the show's feed, site, or a "
         "news report."),
    ],
    sources=[*SOURCES, *shows.sources_for(
        shows.ACQUIRED_URL,
        shows.BUSINESS_WARS_URL,
        shows.HIBT_PRESS_URL,
        shows.HIBT_WRAP_URL,
        shows.HIBT_WONDERY_URL,
        shows.HIBT_FEED_URL,
        shows.JOURNAL_FEED_URL,
        shows.JOURNAL_2019_URL,
        shows.JOURNAL_LINEBAUGH_URL,
        shows.PLANET_MONEY_FEED_URL,
        shows.PLANET_MONEY_APPLE_URL,
        shows.INDICATOR_FEED_URL,
    ), *NEW_SOURCES],  # The Infinite Dial release on Podnews is already in SOURCES.
    episodes_intro="Hear an owner tell the story of building a company firsthand, then compare it with any show above.",
    episodes=[
        ("melissa-banko", "Melissa Banko on growing Banko Design from a spare bedroom into a multi-brand firm"),
        ("how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott",
         "How four veterans built Four Branches Bourbon"),
        ("from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
         "Scott Burnley on going from selling ice to a 140-person pet care business"),
    ],
)
