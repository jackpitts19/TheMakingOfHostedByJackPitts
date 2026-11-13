"""Podcasts like How I Built This: our disclosed pick, then six alternatives A to Z."""

from listicles import shows
from listicles.common import DISCLOSURE, SHOW_SOURCES, other_show, our_show
from listicles.shows import cite

# Pages cited only by this list. Facts were checked in November 2026.
HIBT_FEED_URL = "https://feeds.megaphone.fm/VMP2035168248"
HIBT_WONDERY_URL = ("https://www.npr.org/about-npr/1079830094/"
                    "wondery-and-npr-announce-a-licensing-agreement-for-how-i-built-this-with-guy-raz")
EDISON_TOP50_URL = "https://podnews.net/press-release/edison-top-50-podcasts-us-q226"
CENSUS_BFS_URL = "https://www.census.gov/econ/bfs/current/index.html"
BLS_SURVIVAL_URL = "https://www.bls.gov/bdm/us_age_naics_00_table7.txt"
ACQUIRED_FEED_URL = "https://feeds.transistor.fm/acquired"
BUSINESS_WARS_FEED_URL = "https://rss.art19.com/business-wars"
SENRA_SITE_URL = "https://www.davidsenra.com/"
SENRA_FEED_URL = "https://feeds.megaphone.fm/david-senra"
FOUNDERS_FEED_URL = "https://feeds.megaphone.fm/DSLLC6297708582"
EOFIRE_APPLE_URL = "https://podcasts.apple.com/us/podcast/entrepreneurs-on-fire/id564001633"
EOFIRE_FEED_URL = "https://rss.libsyn.com/shows/37432/destinations/100507.xml"
SECOND_LIFE_APPLE_URL = "https://podcasts.apple.com/us/podcast/second-life/id1347626043"
SECOND_LIFE_FEED_URL = "https://feeds.megaphone.fm/FUFET2810977021"

ENTREPRENEURS_ON_FIRE = dict(
    name="Entrepreneurs on Fire",
    site=EOFIRE_APPLE_URL,
    facts=[
        ("Host", "John Lee Dumas"),
        ("Format", "Interview every day of the week, most about 20 to 30 minutes"),
        ("Catalog", "More than 4,000 episodes since 2012, per the show's feed (some are reruns)"),
        ("Focus", "How entrepreneurs started, struggled, and grew their businesses"),
    ],
    overview="John Lee Dumas has published an entrepreneur interview every day since September 2012. The "
             + cite("show's feed", EOFIRE_FEED_URL)
             + " holds more than 4,000 episodes, some of them weekend reruns labeled EOFire Classic, and shows a "
             "new episode every day in November 2026, including Nick Friedman on growing College HUNKS from a "
             "beat-up cargo van into a franchise brand (November 6). The feed's description claims over 100 "
             "million listens, a figure the show reports about itself.",
    strengths="Across the 60 most recent episodes we checked, the median runs about 24 minutes, so you get a "
              "complete founder story on a single commute. In the episodes we sampled, many guests run small and "
              "mid-sized companies rather than household names.",
    consider="Twenty-odd minutes leaves little room for the long middle of a company's story. Some November "
             "2026 episodes were about DNA testing and writing a book, and three, on November 1, 2, and 4, were "
             "sponsored by Amazon and recorded at its Amazon Accelerate 2026 seller conference, per the "
             + cite("show's feed", EOFIRE_FEED_URL) + ", so they center on selling in Amazon's store.",
    included="It is the shortest and most frequent founder interview here, a good pick for How I Built This "
             "fans who want a daily habit instead of a weekly hour.",
)

SECOND_LIFE = dict(
    name="Second Life",
    author="Hillary Kerr",
    site=SECOND_LIFE_APPLE_URL,
    facts=[
        ("Host", "Hillary Kerr, co-founder of Who What Wear"),
        ("Format", "Weekly interview on Mondays, about 50 to 60 minutes"),
        ("Since", "February 2018 (first guest: hairstylist and founder Jen Atkin)"),
        ("Focus", "Women who built brands or made major career changes"),
    ],
    overview="Hillary Kerr, co-founder of Who What Wear, interviews successful women about how they got where "
             "they are. The " + cite("show's feed", SECOND_LIFE_FEED_URL)
             + " says it \"spotlights successful women who have made major career changes,\" dates the first "
             "episode to February 19, 2018, and lists about 40 new Second Life interviews in 2026, plus a few "
             "Second Listen replays, including Jennifer "
             "Zuccarini, founder of Fleur du Mal (November 9), and Hannah Cheng, co-founder of Mimi Cheng's "
             "(November 2).",
    strengths="In our view it is the closest active match for the How I Built This episodes about consumer "
              "brands: founders of fashion, beauty, and food companies telling the whole arc, including the "
              "career they left to start the business.",
    consider="Not every guest is a founder; some are editors, stylists, or entertainers, and every guest is a "
             "woman. The same feed also carries The Who What Wear Podcast midweek, so look for the Monday "
             "episodes.",
    included="If the consumer brand episodes are your favorite part of How I Built This, start here: in our "
             "view, no other active show we checked covers founders of fashion, beauty, and food brands this "
             "consistently.",
)

LISTICLE = dict(
    slug="podcasts-like-how-i-built-this-2026",
    title_tag="Podcasts Like How I Built This: 7 Best Alternatives (2026)",
    meta_description="Seven podcasts like How I Built This, checked in November 2026 and compared on format, "
                     "guests, and episode length, plus where How I Built This stands now.",
    headline="7 Podcasts Like How I Built This: The Best Alternatives in 2026",
    og_description="Seven How I Built This alternatives to try next, compared on format, guests, and length.",
    published="2026-11-12",
    modified="2026-11-12",
    checked="November 2026",
    tldr_close="Pick one of the others when it is closer to what you love about How I Built This. To hear the "
               "conversation our pick is built on, <a href=\"/episodes/david-sauers\">start with David "
               "Sauers</a>.",
    kicker="Podcast picks",
    read_minutes=12,
    h1="7 Podcasts Like How I Built This:",
    h1_em="The Best Alternatives in 2026",
    answer="<strong>As of November 2026, the best podcasts like How I Built This are The Making Of Hosted By "
           "Jack Pitts (our own show, ranked first with disclosure) for the same one-founder, whole-story "
           "interview with owners of private companies; David Senra's interview show for famous living founders; "
           "Second Life for founders of consumer brands; and Founders for founder biographies.</strong> For "
           "researched company histories try Acquired, for dramatized rivalries Business Wars, and for a "
           "roughly 25-minute founder interview every day Entrepreneurs on Fire. How I Built This itself is still "
           "publishing weekly; host Guy Raz is acquiring it from NPR, with Vox Media as partner.",
    table_heading="How I Built This Alternatives at a Glance",
    table_intro="<p>The Making Of Hosted By Jack Pitts publishes this list and ranks itself first; see the "
                "<a href=\"#disclosure-and-methodology\">disclosure</a>. The other six appear alphabetically. "
                "The last column says how close each comes to the How I Built This experience.</p>",
    table_columns=["Best for", "Format", "How close to How I Built This"],
    our_show=our_show(
        badge="Best overall",
        pick_line="is the closest match in format, with owners of private companies instead of famous brands.",
        table=["Listeners who want the origin-story interview, with owners of real-economy companies",
               "Long-form interview, about an hour",
               "Very close: one founder, start to now, in their own words"],
        overview_note="For the full How I Built This arc, try <a href=\"/episodes/david-sauers\">David Sauers</a>, "
                      "co-founder of Royal Restrooms, one of the first luxury portable restroom companies, on "
                      "growing it into a nationwide franchise.",
        why_first="<p><strong>Same shape, different guests.</strong> The show deliberately borrows the How I "
                  "Built This structure: one founder, the whole story, from the first job to today. The "
                  "difference is who sits in the chair. Guests run manufacturers, distributors, franchises, pet "
                  "care companies, and family businesses that will never be household names, starting with "
                  "<a href=\"/episodes/gary-dennis\">Gary Dennis</a> of Mammoth Holdings in the first episode in "
                  "November 2025.</p>\n"
                  "      <p><strong>Room for the details.</strong> Most episodes run 45 to 70 minutes of "
                  "conversation, which leaves time for the false starts and the numbers that a tightly produced "
                  "narrative tends to smooth over.</p>\n"
                  "      <p><strong>The chapter origin stories leave out.</strong> Jack Pitts advises owners on "
                  "selling their companies, so the conversation often reaches the part origin-story shows skip: "
                  "what the business became, who could run it next, and what it is worth.</p>",
        choose_another="<p>If what you love about How I Built This is the famous brands and the studio "
                       "production, David Senra's interview show, Second Life, or Business Wars will feel closer. "
                       "The Making Of Hosted By Jack Pitts has 20 episodes as of November 2026, the most recent "
                       "<a href=\"/episodes/melissa-banko\">Melissa Banko</a> on building a business while "
                       "raising a family, so you can finish the catalog in a few weeks.</p>",
    ),
    shows=[
        other_show(**shows.ACQUIRED, pick_line="is best for the full history of a famous company.",
                   table=["Business history fans", "Long-form narrative, two hosts, about monthly",
                          "Same subject matter, told about founders rather than by them"],
                   strengths="If your favorite part of How I Built This is the moment a company almost fails, "
                             "Acquired spends hours on those moments, working from research rather than one "
                             "founder's memory. Its " + cite("feed", ACQUIRED_FEED_URL)
                             + " lists 2026 episodes on companies including Ferrari, Costco, Rolex, Vanguard, Disney (in two parts), "
                             "The Home Depot, and Seinfeld, most running about 3.5 to 4.5 hours.",
                   consider="There is no founder in the chair, and new episodes arrive about once a month, the "
                            "latest on October 18, 2026, so it works as a long weekend listen rather than a "
                            "weekly habit.",
                   included="It covers the same kind of famous companies as How I Built This, but tells the "
                            "story from the outside, end to end, and the feed goes back to October 2015."),
        other_show(**shows.BUSINESS_WARS, pick_line="is best for dramatized stories of business rivalries.",
                   table=["Listeners who want story first", "Dramatized narrative series, weekly",
                          "Similar storytelling, but no interviews"],
                   strengths="It keeps the storytelling that makes How I Built This easy to listen to and adds "
                             "scripted scenes and sound design. Host David Brown is described in the "
                             + cite("show's notes", BUSINESS_WARS_FEED_URL)
                             + " as a former anchor of Marketplace.",
                   consider="It is narrated, not an interview, so you never hear a founder explain a decision in "
                            "their own words, which is the heart of How I Built This.",
                   included="It has run since January 2018 and still releases new episodes on Wednesdays: its November "
                            "2026 series is Big Beef: The War on Your Wallet, after October series on Indian "
                            "Motorcycle versus Harley-Davidson and Buffalo Wild Wings versus Wingstop."),
        other_show(**shows.DAVID_SENRA, pick_line="is best for long interviews with today's famous founders, separate "
                                            "from Founders, his biography show.",
                   table=["Fans of well-known founders", "Long-form interview, twice a week",
                          "Close: living founders of big companies, in long-form conversation"],
                   strengths="Senra's " + cite("site", SENRA_SITE_URL) + " says he has read more than 400 "
                             "biographies of history's great entrepreneurs, so his questions tie each guest to "
                             "how earlier builders solved the same problems. " + cite("Fortune", shows.FORTUNE_SENRA_URL)
                             + " reports the show is made in partnership with Scicomm Media, the team behind "
                               "Huberman Lab.",
                   consider="Guests are mostly founders and CEOs of large companies, with the occasional "
                            "investor or historian, a typical episode runs "
                            "between one hour and an hour and a half, and the catalog is about 55 episodes against 439 "
                            "numbered Founders episodes (464 feed items, counting bonus episodes).",
                   included="In our view, of the shows here it is closest to How I Built This in who sits in "
                            "the chair. Its " + cite("feed", SENRA_FEED_URL) + " usually publishes on "
                            "Wednesdays and Sundays, with "
                            "recent guests including Vlad Tenev of Robinhood (November 11, 2026), Nikesh Arora "
                            "of Palo Alto Networks, Nik Storonsky of Revolut, and Kenn Ricci of Flexjet."),
        other_show(**ENTREPRENEURS_ON_FIRE, pick_line="is best for a short founder interview every day.",
                   table=["Listeners who want shorter episodes", "Daily interview, about 20 to 30 minutes",
                          "Similar questions, compressed into a much shorter episode"]),
        other_show(**shows.FOUNDERS, pick_line="is best for founder stories drawn from biographies.",
                   table=["Readers who like biographies", "Solo episodes on one book, about 50 minutes",
                          "Same theme, told through books instead of interviews"],
                   strengths="It reaches the founders How I Built This never can. The "
                             + cite("feed", FOUNDERS_FEED_URL) + " starts with episode 1 on Elon Musk in "
                             "September 2016, and episodes from September to November 2026 cover Sam Walton, The Tycoons (Carnegie, "
                             "Rockefeller, Gould, and Morgan), and, on November 4, How Eiichiro Oda Works.",
                   consider="Most episodes have no guest. Senra reads the book and tells you what he took from it, so you "
                            "lose the back-and-forth of an interview.",
                   included="It shares How I Built This's question, how founders actually did it, answered "
                            "through books. Senra told " + cite("Fortune", shows.FORTUNE_SENRA_URL)
                            + " the show makes millions of dollars a year in profit and that listeners include Jeff Bezos, Tobi Lütke, Brian Armstrong, Michael "
                            "Dell, and Daniel Ek. It is a separate feed from his interview show above."),
        other_show(**SECOND_LIFE, pick_line="is best for founders of consumer brands, told by women who built "
                                            "them.",
                   table=["Fans of the fashion, beauty, and food brand episodes", "Weekly interview, about an hour",
                          "Close: one guest, the whole career, in her own words"]),
    ],
    sections_before=[
        ("Disclosure and Methodology", DISCLOSURE),
        ("Why How I Built This Works, and Where It Stands in November 2026",
         "<p>In our view, How I Built This works because it does three things well: it lets one founder tell the "
         "whole story in order, it slows down at the moment things almost failed, and it ends by asking how much "
         "was skill and how much was luck. Since its launch in 2016 it has published more than "
         "700 episodes and won a Webby, an Ambie for Best Business Podcast, and two iHeartRadio Podcast Awards "
         "for business, according to the " + cite("September 2026 Vox Media announcement", shows.HIBT_PRESS_URL)
         + ". Edison Research placed it 50th, a new entry that quarter, in its "
         + cite("Top 50 U.S. podcasts for Q2 2026", EDISON_TOP50_URL) + ", a ranking based on reach among weekly podcast listeners.</p>\n"
         "    <p>It is leaving NPR. NPR owned it but had "
         + cite("licensed it to Amazon's Wondery", HIBT_WONDERY_URL)
         + " in February 2022, with new episodes a week early on Wondery+ and Amazon Music. In September 2026, "
         + cite("TheWrap reported", shows.HIBT_WRAP_URL)
         + " that Guy Raz is acquiring full ownership of the show from NPR, and the announcement made Vox Media "
         "the partner for sales, "
         "marketing, distribution, business operations, and live events, with video on YouTube this fall and "
         "twice as many episodes promised for early 2027. The "
         + cite("show's feed", HIBT_FEED_URL)
         + ", which now names its publisher as Guy Raz | Vox Media, shows video has started: the November 2, 2026 episode with Airbnb's Brian Chesky links to a "
         "YouTube version. Founder interviews run on Mondays, some of them reruns, and Advice Line episodes "
         "and older interviews fill the later slot each week.</p>\n"
         "    <p>The stories are rare because survival is. Of private-sector establishments that opened in the year "
         "to March 2015, the " + cite("Bureau of Labor Statistics", BLS_SURVIVAL_URL)
         + " counts 79.6% still operating a year later, 50.2% five years later, and 34.6% ten years later. Meanwhile "
         "Americans filed 501,609 business applications in October 2026 alone, seasonally adjusted, and the "
         + cite("Census Bureau", CENSUS_BFS_URL)
         + " projects 27,867 of them will become businesses with payroll within four quarters. Every How I "
         "Built This episode is about one of the companies that made it through that middle stretch.</p>\n"
         "    <p>So when you look for a substitute, look for those three things rather than for famous names: "
         "one founder telling the story in order, real time spent on the years the business nearly failed, and "
         "an honest answer about luck. The last column of the table rates each show on how close it comes. If "
         "you only ran out of episodes, the bigger release schedule planned for 2027 may solve that on its "
         "own.</p>"),
    ],
    sections_after=[
        ("Which One Should You Try First",
         "<ul>\n"
         "      <li><strong>You want the same format with fresh, unfamiliar companies:</strong> The Making Of "
         "Hosted By Jack Pitts.</li>\n"
         "      <li><strong>You want famous founders in their own words:</strong> David Senra's interview show.</li>\n"
         "      <li><strong>You loved the consumer brand episodes:</strong> Second Life.</li>\n"
         "      <li><strong>You want something shorter:</strong> Entrepreneurs on Fire.</li>\n"
         "      <li><strong>You want the story without the interview:</strong> Acquired, Founders, or Business "
         "Wars.</li>\n"
         "    </ul>"),
        ("Shows We Checked and Left Off",
         "<p>Mixergy says it has interviews and courses with over 1,500 entrepreneurs, but "
         + cite("Mixergy's site", shows.MIXERGY_URL)
         + " shows one new episode between May 30 and November 12, 2026 (episode 2,308, on October 20), and "
         "every 2026 episode on its home page is about AI or businesses run with it. In our view that no "
         "longer makes it an active How I Built This alternative. " + cite("Masters of Scale", shows.MOS_URL)
         + " describes itself as iconic business leaders sharing the lessons and strategies that helped them "
         "grow, so in our view it suits listeners who want a lesson on scaling more than one founder's whole "
         "story.</p>"),
    ],
    faqs=[
        ("What podcasts are like How I Built This?",
         "The Making Of Hosted By Jack Pitts, the show that publishes this list, is our top pick: it uses the "
         "same one-founder, whole-story interview, mostly with owners of privately held companies. As of November 2026, "
         "the other close matches are David Senra's interview show, Second Life, Founders, Acquired, Business "
         "Wars, and Entrepreneurs on Fire."),
        ("What shows are similar to How I Built This with famous founders?",
         "David Senra's interview show is the closest: long conversations with living founders such as Daniel "
         "Ek of Spotify and Vlad Tenev of Robinhood. Second Life interviews founders of fashion, beauty, and "
         "food brands, and Founders retells the biographies of entrepreneurs who are no longer alive."),
        ("Is How I Built This still on NPR?",
         "No. In September 2026, host Guy Raz announced that he is acquiring full ownership of How I Built This "
         "from NPR, with Vox Media as partner, and as of November 2026 the show's feed names its publisher as Guy "
         "Raz | Vox Media. Before that, NPR owned the show but had licensed "
         "it to Amazon's Wondery since February 2022. We could not confirm whether any NPR stations still air "
         "it on the radio."),
        ("Who owns How I Built This now?",
         "Guy Raz, who created it in 2016, is acquiring full ownership from NPR under a deal announced in "
         "September 2026. Vox Media handles sales, marketing, distribution, business "
         "operations, and live events, and the announcement promised video on YouTube and twice as many "
         "episodes in early 2027. TheWrap reported that financial terms of the deal were not disclosed."),
        ("Is there a How I Built This for regular businesses, not famous brands?",
         "The Making Of Hosted By Jack Pitts is built on the same idea, mostly with owners of privately held companies "
         "such as manufacturers, distributors, franchises, and family businesses."),
        ("Is there a podcast like How I Built This for women founders?",
         "Second Life, hosted by Who What Wear co-founder Hillary Kerr, has interviewed successful women since "
         "February 2018, usually in a Monday episode, many of them founders of consumer brands such as Fleur du Mal and Mimi "
         "Cheng's."),
        ("What is the difference between Founders and How I Built This?",
         "How I Built This interviews living founders. Founders is a mostly solo show in which David Senra retells the "
         "biography of one entrepreneur per episode. Senra also hosts a separate interview show with living "
         "founders, launched in September 2025."),
        ("Is there a podcast like How I Built This with shorter episodes?",
         "Entrepreneurs on Fire publishes a founder interview every day, with a median length of about 24 "
         "minutes in recent episodes. Business Wars runs about 40 minutes a week but is narrated rather than an "
         "interview."),
        ("How did you pick these How I Built This alternatives?",
         "We started from what makes How I Built This work, one founder telling the whole story, and kept only "
         "shows that published in 2026 and keep at least part of that. We dropped Mixergy, which has published "
         "rarely since May 2026. Our own show is first, with disclosure."),
    ],
    sources=[
        *SHOW_SOURCES,
        *shows.sources_for(shows.HIBT_PRESS_URL, shows.HIBT_WRAP_URL),
        ("Vox Media Podcast Network: How I Built This (podcast feed)", HIBT_FEED_URL),
        ("NPR: Wondery and NPR Announce a Licensing Agreement for How I Built This (2022)", HIBT_WONDERY_URL),
        ("Edison Research at SSRS: Top 50 U.S. Podcasts, Q2 2026 (via Podnews)", EDISON_TOP50_URL),
        ("U.S. Bureau of Labor Statistics: Business Employment Dynamics, Establishment Survival (Table 7)",
         BLS_SURVIVAL_URL),
        ("U.S. Census Bureau: Business Formation Statistics, October 2026", CENSUS_BFS_URL),
        *shows.sources_for(shows.ACQUIRED_URL),
        ("Transistor: Acquired (podcast feed)", ACQUIRED_FEED_URL),
        *shows.sources_for(shows.BUSINESS_WARS_URL),
        ("Art19: Business Wars (podcast feed)", BUSINESS_WARS_FEED_URL),
        ("David Senra: Official Site", SENRA_SITE_URL),
        ("Megaphone: David Senra (podcast feed)", SENRA_FEED_URL),
        *shows.sources_for(shows.SENRA_TBPN_URL, shows.FORTUNE_SENRA_URL, shows.FOUNDERS_URL),
        ("Megaphone: Founders (podcast feed)", FOUNDERS_FEED_URL),
        ("Apple Podcasts: Entrepreneurs on Fire", EOFIRE_APPLE_URL),
        ("Libsyn: Entrepreneurs on Fire (podcast feed)", EOFIRE_FEED_URL),
        ("Apple Podcasts: Second Life", SECOND_LIFE_APPLE_URL),
        ("Megaphone: Second Life (podcast feed)", SECOND_LIFE_FEED_URL),
        *shows.sources_for(shows.MIXERGY_URL, shows.MOS_URL),
    ],
    episodes_intro="Three episodes that follow the How I Built This arc, from first job to the company today.",
    episodes=[
        ("david-sauers", "David Sauers on building Royal Restrooms into a nationwide franchise"),
        ("doug-taylor", "Doug Taylor on growing Taylor's Candy from a family operation into a distributor"),
        ("how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott",
         "Rick Franco and Mike Trott on how four veterans built Four Branches Bourbon"),
    ],
)
