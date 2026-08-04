// The Making Of Hosted By Jack Pitts -- episode data.
// This file is the SOURCE OF TRUTH for the episode list on the site.
// A scheduled task (update-tmo-episodes) runs daily, checks Spotify,
// Apple Podcasts, and YouTube for new episodes, and prepends them
// here. The site no longer overrides this list with the Apple feed,
// because Apple's feed lags by weeks. To add an episode by hand,
// prepend a new object to window.EPISODES below.
//
// FIELDS
//   date           ISO date "YYYY-MM-DD" (sort key only).
//   dateLabel      Date as it appears on the card.
//   title          Episode title exactly as published.
//   guest          Canonical guest name (used in the past-guests marquee).
//   description    Real summary pulled from the show's listing.
//   duration       Free-form runtime label.
//   tag            Optional. "first" | "press" | "pick" -> pinned card.
//   guestLinkedIn  Optional. Paste the guest's LinkedIn URL here. When
//                  present, the card adds a "Connect" pill and the
//                  marquee makes that guest's name clickable.
//   links          Per-episode listen URLs (default to show-level URL).

window.EPISODES = [
  {
    "date": "2026-07-30",
    "dateLabel": "July 30, 2026",
    "title": "Davies Hood of Induron Protective Coatings: Building an 80-Year Family Business",
    "guest": "Davies Hood of Induron Protective Coatings",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, Jack sits down with Davies Hood, President of Induron Protective Coatings, a third-generation family business founded in Birmingham in 1947. Davies shares how he went from working difficult summer jobs in the plant to becoming a regional salesperson, company president, and eventually owner. He explains how Induron protects critical water, wastewater, and power infrastructure, why relationships matter so much in industrial sales, and how learning to put the right people in the right roles changed the trajectory of the company. The conversation also covers family-business succession, buying the company from his father, leading through uncertainty, building a strong team, and Davies’ hope of eventually passing Induron to a fourth generation. A great episode for business owners, entrepreneurs, operators, and anyone interested in leadership, legacy, and building a company that lasts.",
    "duration": "45 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/davies-hood-of-induron-protective-coatings-building/id1853933144?i=1000779100503&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000779100503"
  },
  {
    "date": "2026-07-09",
    "dateLabel": "July 9, 2026",
    "title": "Concentrate AI: The LLM Gateway for Fast-Growing Teams",
    "guest": "Concentrate AI",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sat down with Ari Jacoby, Co-Founder & CEO of Concentrate AI, and Zach Moskow, Founding GTM & Ops at Concentrate AI. Concentrate recently launched out of stealth after raising $5.1 million and is building an LLM gateway that gives teams one API to access leading AI models, manage token spend, improve reliability, and add security and compliance controls as they scale AI products. We talked about the company’s journey from GPU cloud to AI infrastructure, why managing AI models is becoming more complex, how companies should think about vendor lock-in, the importance of multi-cloud resiliency, and why compliance may become one of the biggest themes in AI. I’m also a customer of Concentrate AI myself, and it has been great to use. If you’re building with AI models or thinking about cost, uptime, and compliance, definitely check them out. Check out Concentrate AI: Concentrate AI (concentrate.ai), the Best LLM Gateway for Fast Growing Teams. Guest: Ari Jacoby and Zach Moskow Company: Concentrate AI Hosted by: Jack Pitts Check out Concentrate AI: https://concentrate.ai/ Connect with Ari: https://www.linkedin.com/in/arijacoby/ Connect with Zach: https://www.linkedin.com/in/moskow/",
    "duration": "31 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/concentrate-ai-the-llm-gateway-for-fast-growing-teams/id1853933144?i=1000776113175&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000776113175"
  },
  {
    "date": "2026-06-11",
    "dateLabel": "June 11, 2026",
    "title": "In The Making Of: Nishank Gite",
    "guest": "Nishank Gite",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, host Jack Pitts sits down with Nishank Gite, Co-Founder & CTO of Nirvana Robotics, to explore Nishank’s journey from physics and AI research into building a robotics company. The conversation covers Nishank’s background in collider physics, machine learning, neural networks, and robotics, along with the realities of building a hard-tech startup. Nishank shares his perspective on fundraising, startup risk, industrial automation, humanoid robots, dark factories, and what it takes to deploy robotics in real-world manufacturing environments. At its core, this episode is about Nishank’s path as a young founder building in one of the hardest and most exciting areas of technology: bringing AI into the physical world.",
    "duration": "1h 3m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-nishank-gite/id1853933144?i=1000772197716&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000772197716"
  },
  {
    "date": "2026-05-21",
    "dateLabel": "May 21, 2026",
    "title": "The Making Of Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas",
    "guest": "Alex Dixon",
    "description": "In this episode of The Making Of, I sit down with Alex Dixon, former CEO of Resorts World Las Vegas and former executive at MGM Resorts and Caesars Entertainment. Alex shares his journey from growing up in Las Vegas as a third-generation casino employee to working at Goldman Sachs in New York and London, where he advised on major deals including Disney’s acquisition of Pixar and multi-billion dollar financings. We dive into what it was really like helping build and operate massive casino properties including Horseshoe Baltimore, MGM Springfield, Circus Circus, and Resorts World Las Vegas. Alex also talks about leadership, scaling teams from a handful of employees to thousands, navigating private equity, economic development, casino operations, and the sacrifices required to rise through the gaming and hospitality industry. This episode is packed with insights on business, career growth, hospitality, finance, entrepreneurship, and what it takes to lead billion-dollar operations at some of the biggest names in Las Vegas.",
    "duration": "50 min",
    "guestLinkedIn": "https://www.linkedin.com/in/alexfdixon",
    "links": {
      "spotify": "https://open.spotify.com/episode/58DPxKdLPZjdwvoVm6xdrr",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-alex-dixon-from-goldman-sachs-to/id1853933144?i=1000768906935&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000768906935"
  },
  {
    "date": "2026-05-07",
    "dateLabel": "May 7, 2026",
    "title": "The Making Of David Sauers: Building Royal Restrooms Into a Nationwide Franchise",
    "guest": "David Sauers",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with David Sauers, co-founder of Royal Restrooms, one of the first luxury portable restroom companies in the country. David shares his journey growing up in Savannah, Georgia, working odd jobs as a kid, pursuing professional golf, getting into banking, and eventually building a nationwide franchise business after a frustrating experience at a local festival sparked an idea. We talk about entrepreneurship, risk-taking, franchising, balancing family and business, private equity interest, AI in marketing, and what it really takes to grow a company over 20+ years. David also shares lessons on leadership, sacrifice, branding, and why execution matters more than just having ideas. If you’re interested in entrepreneurship, franchising, business growth, or hearing the real stories behind successful companies, this episode is for you.",
    "duration": "1h 8m",
    "guestLinkedIn": "https://www.linkedin.com/in/davidsauers/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-david-sauers-building-royal-restrooms/id1853933144?i=1000766608021&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000766608021"
  },
  {
    "date": "2026-04-30",
    "dateLabel": "April 30, 2026",
    "title": "In The Making Of: Jesse Choe",
    "guest": "Jesse Choe",
    "description": "In this episode of The Making Of Hosted by Jack Pitts, I sit down with Jesse Choe, CEO and Co-Founder of Bidflow. He breaks down his journey from early startup experiments to raising $1M at 19, dropping out of college, and getting into Y Combinator. Jesse shares how his path started with building “fake startups” in high school, learning through failure, and eventually realizing the importance of customer validation and solving real problems. The conversation covers the pivots that actually mattered, the pressure of the YC process, and how rejection and iteration shaped his approach. They also dive into co-founder dynamics, burnout, and how they landed on Bidflow by focusing on a real pain point in electrical estimation. A grounded look at what it actually takes to build something from scratch and figure it out in real time.",
    "duration": "54 min",
    "guestLinkedIn": "https://www.linkedin.com/in/jc10/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-jesse-choe/id1853933144?i=1000764732791&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000764732791"
  },
  {
    "date": "2026-04-23",
    "dateLabel": "April 23, 2026",
    "title": "The Making Of Shane Crocker: From Family Business to Multi-Industry Operator",
    "guest": "Shane Crocker",
    "description": "On this episode of The Making Of Hosted By Jack Pitts, Shane Crocker shares his journey from growing up in a family business to building and operating across healthcare, oilfield services, and franchising. He breaks down how he approaches scaling in niche markets, making strategic decisions, and navigating private equity involvement from an operator’s perspective. The conversation also gets into leadership, risk-taking, and how he balances building businesses with family life.",
    "duration": "1h 16m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-shane-crocker-from-family-business/id1853933144?i=1000763236988&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000763236988"
  },
  {
    "date": "2026-04-09",
    "dateLabel": "April 9, 2026",
    "title": "The Making Of Dave \"Laundromat Millionaire\" Menz",
    "guest": "Dave Menz",
    "description": "Dave “Laundromat Millionaire” Menz didn’t start with much. He grew up in poverty in Flint, Michigan, wearing hand-me-down clothes and learning early that if he wanted something, he had to go get it. After spending 17 years in a stable corporate job, Dave found himself stuck, comfortable but unfulfilled. Instead of coasting, he made a bet on himself. Alongside his wife Carla, he saved aggressively, lived below their means, and bought a rundown laundromat that was losing money at the time. What followed was years of sacrifice. Working 90–100 hour weeks, reinvesting every dollar, and slowly turning broken businesses into profitable ones. No shortcuts, no outside capital, just grit and consistency. In this episode, Dave breaks down what it actually takes to build something from nothing, the risks most people avoid, and why delayed gratification is the real edge in business.",
    "duration": "1h 23m",
    "guestLinkedIn": "https://www.linkedin.com/in/dave-laundromat-millionaire-menz/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-dave-laundromat-millionaire-menz/id1853933144?i=1000760449322&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000760449322"
  },
  {
    "date": "2026-03-26",
    "dateLabel": "March 26, 2026",
    "title": "The Making Of Lou Mongello: From Lawyer to Disney Entrepreneur",
    "guest": "Lou Mongello",
    "description": "In this conversation, Lou Mongello shares how he went from practicing law to building a career around his passion for Disney. He talks about the early influences that shaped his entrepreneurial mindset, the challenge of balancing family and work, and why focusing on community became the foundation of his success. Drawing inspiration from Walt Disney, Lou explains the principles that guide both his business and his life, and why making a positive impact and giving back matter more than metrics. Listen to the full episode for a real look at how to turn passion into a career, build a loyal community, and make decisions without regret, all through the lens of Lou Mongello’s journey.",
    "duration": "1h 12m",
    "guestLinkedIn": "https://www.linkedin.com/in/loumongello/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-lou-mongello-from-lawyer-to/id1853933144?i=1000757482795&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000757482795"
  },
  {
    "date": "2026-03-12",
    "dateLabel": "March 12, 2026",
    "title": "In The Making Of: Niilo Pirttijärvi",
    "guest": "Niilo Pirttijärvi",
    "description": "On this episode of The Making Of Hosted By Jack Pitts, I sat down with Niilo Pirttijärvi, the co-founder & CEO of Inven, to talk about how AI is changing the way private equity firms find and analyze deals. We talked about how sourcing has traditionally worked in private equity and why Niilo believed there was an opportunity to rethink it using AI. He walked me through his path from McKinsey & Company to starting Inven, the early days of building the product, and what it took to land their first customers. What stood out to me was how much relationships still matter in private equity, even as technology gets more powerful. We also got into the realities of building a SaaS startup, working with VCs, and where tools like Inven could take the industry next. If you're interested in startups, private equity, or how AI is actually being used in business today, I think you’ll enjoy this conversation.",
    "duration": "51 min",
    "guestLinkedIn": "https://www.linkedin.com/in/niilo-pirttijarvi/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-niilo-pirttij%C3%A4rvi/id1853933144?i=1000754836096&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000754836096"
  },
  {
    "date": "2026-02-26",
    "dateLabel": "February 26, 2026",
    "title": "The Making of Kris Carlson: From Sales to Seafood",
    "guest": "Kris Carlson",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, Jack interviews Kris Carlson, President and COO of The Fish Guys. Kris shares his journey from growing up in Champaign, Illinois, to building a career in sales at Reuters, and ultimately leading a growing food distribution company. He discusses how sports, Greek life, and teamwork shaped his leadership, and the lessons he learned navigating challenges early in his career. Kris also explains how he helped The Fish Guys adapt and grow during COVID-19, including launching an e-commerce platform, and shares insights on leadership, community, and building a dedicated team. This episode is packed with practical advice and inspiration for anyone interested in entrepreneurship, leadership, and overcoming challenges in business.",
    "duration": "1h 24m",
    "guestLinkedIn": "https://www.linkedin.com/in/kris-carlson-b57b682",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-kris-carlson-from-sales-to-seafood/id1853933144?i=1000751740327&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000751740327"
  },
  {
    "date": "2026-02-05",
    "dateLabel": "February 5, 2026",
    "title": "In The Making Of: Ian Hicks",
    "guest": "Ian Hicks",
    "description": "This a new style for my podcast. Join my conversation with my good friend, Ian Hicks. Ian works at King Industrial in Atlanta as a broker. Ian came and visited me in NYC in December. In this episode, we share candid stories about life in New York City, building businesses, navigating friendships across distances, and the realities of entrepreneurship. Whether you're into real estate, travel, or just seeking to listen to a genuine conversation between two long time pals, this convo offers unfiltered insights into living intentionally and embracing the chaos.",
    "duration": "1h 3m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-ian-hicks/id1853933144?i=1000748365273&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000748365273"
  },
  {
    "date": "2026-01-22",
    "dateLabel": "January 22, 2026",
    "title": "The Making of Robbie Ferman: From Brokerage to Building Sollevare Group",
    "guest": "Robbie Ferman",
    "description": "In this episode, Robbie Ferman, co-founder and managing partners of Sollevare Group, shares his journey from corporate real estate to entrepreneurship. He discusses the importance of building relationships, the challenges of navigating the New York real estate market, and the significance of discipline and mentorship in achieving success. Robbie also reflects on his first deal, the importance of managing investor expectations, and the compelling demographic trends driving their investment strategy. As he looks to the future, he emphasizes the need for discipline in their investment approach and the goal of raising more capital for upcoming projects.",
    "duration": "46 min",
    "guestLinkedIn": "https://www.linkedin.com/in/robert-ferman-2824b2153/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-robbie-ferman-from-brokerage-to/id1853933144?i=1000746199517&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000746199517"
  },
  {
    "date": "2026-01-08",
    "dateLabel": "January 8, 2026",
    "title": "The Making of Doug Taylor: Taylor's Candy",
    "guest": "Doug Taylor",
    "description": "In this episode, Jack Pitts interviews Doug Taylor, known as the Candyman, who shares his journey of building Taylor's Candy from a small family-run operation into a successful candy distribution and manufacturing business. Doug discusses his upbringing, early jobs, and the transition into the candy industry, highlighting the importance of hard work, family dynamics, and adapting to market changes. He also reflects on the impact of COVID-19, the acquisition of Windy City Popcorn, and future plans for the business, emphasizing the significance of relationships and networking in the industry.",
    "duration": "1h 5m",
    "tag": "press",
    "guestLinkedIn": "https://www.linkedin.com/in/doug-taylor-21a73917/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-doug-taylor-taylors-candy/id1853933144?i=1000744284254&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000744284254"
  },
  {
    "date": "2025-12-18",
    "dateLabel": "December 18, 2025",
    "title": "The Making of Adam Stevenson: From Flipping Burgers to Building Businesses",
    "guest": "Adam Stevenson",
    "description": "In this conversation, Adam Stevenson shares his inspiring journey from a low-income upbringing in Detroit to becoming a successful entrepreneur. He discusses his early experiences flipping burgers, starting a landscaping business, and navigating college life while balancing sports and side hustles. The birth of Grassroots Records, a music label he co-founded, highlights his passion for music and community. Throughout the conversation, Adam reflects on the challenges of imposter syndrome and the importance of seizing opportunities, networking, and hard work in achieving success. In this conversation, Adam Stevenson shares his journey through the music industry, the challenges of entrepreneurship, and the importance of perseverance. He discusses the founding of B-Side Cafe, the struggles with partnerships, and the eventual success of AdRock, a marketing and merchandising company. Adam also highlights his experience with Xtreme Xperience, a supercar driving venture, and his current focus on NASS Holdings, where he aims to invest in and mentor young entrepreneurs. Throughout the discussion, he emphasizes the significance of recognizing opportunities, the impact of timing, and the value of personal growth and accountability.",
    "duration": "1h 32m",
    "guestLinkedIn": "https://www.linkedin.com/in/adamstevenson/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-adam-stevenson-from-flipping-burgers/id1853933144?i=1000741828291&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000741828291"
  },
  {
    "date": "2025-11-18",
    "dateLabel": "November 18, 2025",
    "title": "The Making of Mammoth Holdings with Gary Dennis",
    "guest": "Gary Dennis",
    "description": "In this episode of The Making Of, Jack Pitts sits down with Gary Dennis, co-founder and former CEO of Mammoth Holdings, to unpack how a kid from Macon, Georgia ended up building one of the leading car wash platforms in the country. Gary walks through his path from humble beginnings, with a dad who was a maintenance mechanic and a mom who was a secretary, to Georgia Tech, an MBA from Vanderbilt, and an early career in equity research and investment banking. He shares how getting humbled by a boss during his college co-op and by money managers on Wall Street shaped the way he thinks about work, preparation, and actually understanding the numbers. From there, Gary breaks down the jump from a comfortable investment banking career into owning and operating car washes. He explains: How a “side hustle” idea turned into Mammoth’s first self-serve washThe trip to Louisiana that exposed him to the express wash modelWhy he thinks of car washes as manufacturing plants, not retailWhat the 2008–2009 downturn and months of nonstop rain did to the businessHow a mispriced early subscription product almost flopped, and the data that helped them finally get it rightTaking site-level break-even from ~7,000 cars a month to zero with membershipsGary also talks about building Mammoth into a true multi-state platform through development and more than 30 acquisitions, why their internal rule was “no jerks allowed,” and how they structured deals so great owner-operators could roll equity and stay involved. Finally, he reflects on partnering with institutional capital (including the Pritzker Organization), stepping back from the CEO role after nearly 20 years, staying involved as chairman, and how he now splits his time between board work, investing, his alma maters, and advocacy around long-term housing for adults with developmental disabilities. If you’re thinking about leaving a “safe” job, scaling a gritty real-world business, or just want an honest look at the grind behind a 20+ year “overnight success,” this conversation with Gary is worth a listen.",
    "duration": "1h 22m",
    "tag": "first",
    "guestLinkedIn": "https://www.linkedin.com/in/gary-dennis-000010b/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-mammoth-holdings-with-gary-dennis/id1853933144?i=1000737312111&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000737312111"
  }
];
