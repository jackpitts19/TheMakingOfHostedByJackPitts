// The Making Of Hosted By Jack Pitts -- episode data.
// This file is the SOURCE OF TRUTH for the episode list on the site.
// A GitHub Action (.github/workflows/episode-sync.yml) runs twice a day
// (11:05 and 12:05 UTC) and on every push to main. It reads the show's
// RSS feed (Riverside, found via Apple's lookup), adds any episode not
// already listed here (newest first), then fills in per-episode Apple
// links and full descriptions, and regenerates the episode pages, share
// cards, archive and sitemap. To add an episode by hand, prepend a new
// object to window.EPISODES below; the next run builds its page.
//
// FIELDS
//   date           ISO date "YYYY-MM-DD" (sort key only).
//   dateLabel      Date as it appears on the card.
//   title          Episode title exactly as published.
//   guest          Guest name as people should read it (marquee, guest
//                  card). Safe to correct: the URL comes from `slug`.
//   slug           URL slug: /episodes/<slug> and share-cards/<slug>.png.
//                  Set once and never changed, so links never break.
//                  The sync sets it for new episodes.
//   seoTitle       Optional. Search/share title used instead of `title`.
//   metaDescription
//                  Optional. Hand-written search snippet (140-160 chars)
//                  used instead of a trimmed `description`.
//   guid           Feed guid, written by the sync, used to spot duplicates.
//   description    Summary pulled from the show's listing. Hand edits
//                  are kept (see appleDescription).
//   duration       Free-form runtime label.
//   tag            Optional. "first" | "press" | "pick" -> pinned card.
//   guestLinkedIn  Optional. Paste the guest's LinkedIn URL here. When
//                  present, the card adds a "Connect" pill and the
//                  marquee makes that guest's name clickable.
//   links          Per-episode listen URLs (default to show-level URL).
//   appleEpisodeId, appleDescription
//                  Written by resolve_episode_links.py. appleDescription is
//                  what Apple last said, so a hand-edited description that
//                  differs from it is never overwritten.

window.EPISODES = [
  {
    "date": "2026-10-29",
    "dateLabel": "October 29, 2026",
    "title": "Melissa Banko: The Reality of Building a Business and Raising a Family",
    "guest": "Melissa Banko",
    "slug": "melissa-banko",
    "description": "Melissa Banko started Banko Design in a spare bedroom in 2014 and built it into a multi-brand organization serving senior living, multifamily, and private club clients across the country. But along the way, she learned that bigger isn't always better. Melissa, founder of Banko Design and CEO of BD Studio Collection, joins Jack Pitts to talk about entrepreneurship, leadership, acquisitions, and what it really takes to build a sustainable business. They discuss how she found her first clients, built her team, acquired other design firms, and eventually realized that growth doesn't always mean success. Melissa also shares the lessons she's learned about company culture, knowing when to scale back, and balancing running a business with raising a family. From the early days of working late nights with her daughter coloring under her desk to leading a portfolio of companies, Melissa shares what she's learned about building a business on her own terms. Learn more about Melissa and her businesses: Banko Design: https://bankodesign.com BD Studio Collection: https://www.bdstudiocollection.com Melissa on Instagram: https://www.instagram.com/msbbymelissa/ Enjoyed the episode? Follow The Making Of Hosted By Jack Pitts on Spotify or Apple Podcasts, leave a five-star rating, and share it with a friend!",
    "duration": "1h 2m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/melissa-banko-the-reality-of-building-a/id1853933144?i=1000798702938&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "guid": "a7b047ee-37f7-4949-9902-481ff3abc9fb",
    "appleEpisodeId": "1000798702938",
    "appleDescription": "Melissa Banko started Banko Design in a spare bedroom in 2014 and built it into a multi-brand organization serving senior living, multifamily, and private club clients across the country. But along the way, she learned that bigger isn't always better. Melissa, founder of Banko Design and CEO of BD Studio Collection, joins Jack Pitts to talk about entrepreneurship, leadership, acquisitions, and what it really takes to build a sustainable business. They discuss how she found her first clients, built her team, acquired other design firms, and eventually realized that growth doesn't always mean success. Melissa also shares the lessons she's learned about company culture, knowing when to scale back, and balancing running a business with raising a family. From the early days of working late nights with her daughter coloring under her desk to leading a portfolio of companies, Melissa shares what she's learned about building a business on her own terms. Learn more about Melissa and her businesses: Banko Design: https://bankodesign.com BD Studio Collection: https://www.bdstudiocollection.com Melissa on Instagram: https://www.instagram.com/msbbymelissa/ Enjoyed the episode? Follow The Making Of Hosted By Jack Pitts on Spotify or Apple Podcasts, leave a five-star rating, and share it with a friend!"
  },
  {
    "date": "2026-10-08",
    "dateLabel": "October 8, 2026",
    "title": "From Selling Ice to Building a 140-Person Pet Care Business | Scott Burnley",
    "guest": "Scott Burnley",
    "slug": "from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley",
    "description": "Scott Burnley went from delivering bags of ice and working in sales to quitting his job, becoming a dog trainer, and helping build Pet Station Country Club into three locations with around 140 employees. Scott shares what it took to build the business from the ground up, including doing nearly every job himself, surviving a dog flu outbreak that left the company struggling to make payroll, getting through COVID, and learning how to scale a multi-location pet care business. He also talks about building company culture, hiring for attitude over experience, developing leaders, and why his role today is less about taking care of dogs and more about taking care of the people who take care of them. Learn more about Pet Station Country Club: petstationcountryclub.com",
    "duration": "1h 9m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/from-selling-ice-to-building-a-140-person-pet-care/id1853933144?i=1000793858044&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000793858044",
    "appleDescription": "Scott Burnley went from delivering bags of ice and working in sales to quitting his job, becoming a dog trainer, and helping build Pet Station Country Club into three locations with around 140 employees. Scott shares what it took to build the business from the ground up, including doing nearly every job himself, surviving a dog flu outbreak that left the company struggling to make payroll, getting through COVID, and learning how to scale a multi-location pet care business. He also talks about building company culture, hiring for attitude over experience, developing leaders, and why his role today is less about taking care of dogs and more about taking care of the people who take care of them. Learn more about Pet Station Country Club: petstationcountryclub.com",
    "guid": "0529392d-592e-4f0a-a555-08205c0ab26d"
  },
  {
    "date": "2026-09-17",
    "dateLabel": "September 17, 2026",
    "title": "How Four Veterans Built Four Branches Bourbon | Rick Franco & Mike Trott",
    "guest": "Rick Franco & Mike Trott",
    "slug": "how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Rick Franco and Mike Trott, co-founders of Four Branches Bourbon. Four Branches didn’t start as a business. It started as an honor barrel created by four veterans who wanted to remember friends they lost and give back to the military community. Rick and Mike share how that idea turned into an award-winning bourbon brand, what it takes to compete in the crowded spirits industry, and why their message of “Serve Honorably. Drink Honorably. Sip to Remember.” is at the center of everything they do. We also talk about building a premium product, getting onto shelves, mental health, entrepreneurship, and what they hope Four Branches becomes over the next 40 years. If you like stories about service, business, and building something with a real mission behind it, this one is worth a listen. Check out Four Branches Bourbon: https://www.fourbranches.com/",
    "duration": "39 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/how-four-veterans-built-four-branches-bourbon-rick/id1853933144?i=1000790341270&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000790341270",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Rick Franco and Mike Trott, co-founders of Four Branches Bourbon. Four Branches didn’t start as a business. It started as an honor barrel created by four veterans who wanted to remember friends they lost and give back to the military community. Rick and Mike share how that idea turned into an award-winning bourbon brand, what it takes to compete in the crowded spirits industry, and why their message of “Serve Honorably. Drink Honorably. Sip to Remember.” is at the center of everything they do. We also talk about building a premium product, getting onto shelves, mental health, entrepreneurship, and what they hope Four Branches becomes over the next 40 years. If you like stories about service, business, and building something with a real mission behind it, this one is worth a listen. Check out Four Branches Bourbon: https://www.fourbranches.com/",
    "guid": "cfaeaf31-fe48-4248-aea6-d4b22547c034"
  },
  {
    "date": "2026-08-20",
    "dateLabel": "August 20, 2026",
    "title": "Dave Moorman: Building an MSP, Scaling Through M&A & Exiting Twice",
    "guest": "Dave Moorman",
    "slug": "dave-moorman",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Dave Moorman, who spent more than 30 years in the IT and MSP world building, scaling, acquiring, and selling businesses. Dave shares how he went from working at 10 years old and discovering computers through a heavy metal band to building DynaSis for 26 years. He later sold the business to Novatech, became President and CISO, helped complete more than 10 acquisitions, and eventually went through a second exit. We talk about building a great company, culture, leadership, private equity, M&A, AI, selling a business, and how much success comes down to hard work versus luck. A great conversation for founders, operators, and anyone interested in building something that lasts.",
    "duration": "56 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/dave-moorman-building-an-msp-scaling-through-m/id1853933144?i=1000784580073&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000784580073",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Dave Moorman, who spent more than 30 years in the IT and MSP world building, scaling, acquiring, and selling businesses. Dave shares how he went from working at 10 years old and discovering computers through a heavy metal band to building DynaSis for 26 years. He later sold the business to Novatech, became President and CISO, helped complete more than 10 acquisitions, and eventually went through a second exit. We talk about building a great company, culture, leadership, private equity, M&A, AI, selling a business, and how much success comes down to hard work versus luck. A great conversation for founders, operators, and anyone interested in building something that lasts.",
    "guid": "cc0c552a-af24-4538-82c4-744949856f2c"
  },
  {
    "date": "2026-07-30",
    "dateLabel": "July 30, 2026",
    "title": "Davies Hood of Induron Protective Coatings: Building an 80-Year Family Business",
    "guest": "Davies Hood",
    "slug": "davies-hood-of-induron-protective-coatings",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, Jack sits down with Davies Hood, President of Induron Protective Coatings, a third-generation family business founded in Birmingham in 1947. Davies shares how he went from working difficult summer jobs in the plant to becoming a regional salesperson, company president, and eventually owner. He explains how Induron protects critical water, wastewater, and power infrastructure, why relationships matter so much in industrial sales, and how learning to put the right people in the right roles changed the trajectory of the company. The conversation also covers family-business succession, buying the company from his father, leading through uncertainty, building a strong team, and Davies’ hope of eventually passing Induron to a fourth generation. A great episode for business owners, entrepreneurs, operators, and anyone interested in leadership, legacy, and building a company that lasts.",
    "duration": "45 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/davies-hood-of-induron-protective-coatings-building/id1853933144?i=1000779100503&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000779100503",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, Jack sits down with Davies Hood, President of Induron Protective Coatings, a third-generation family business founded in Birmingham in 1947. Davies shares how he went from working difficult summer jobs in the plant to becoming a regional salesperson, company president, and eventually owner. He explains how Induron protects critical water, wastewater, and power infrastructure, why relationships matter so much in industrial sales, and how learning to put the right people in the right roles changed the trajectory of the company. The conversation also covers family-business succession, buying the company from his father, leading through uncertainty, building a strong team, and Davies’ hope of eventually passing Induron to a fourth generation. A great episode for business owners, entrepreneurs, operators, and anyone interested in leadership, legacy, and building a company that lasts.",
    "guid": "352440c3-61be-49cb-83ec-379dfcbb0850"
  },
  {
    "date": "2026-07-09",
    "dateLabel": "July 9, 2026",
    "title": "Concentrate AI: The LLM Gateway for Fast-Growing Teams",
    "guest": "Ari Jacoby & Zach Moskow",
    "slug": "concentrate-ai",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sat down with Ari Jacoby, Co-Founder & CEO of Concentrate AI, and Zach Moskow, Founding GTM & Ops at Concentrate AI. Concentrate recently launched out of stealth after raising $5.1 million and is building an LLM gateway that gives teams one API to access leading AI models, manage token spend, improve reliability, and add security and compliance controls as they scale AI products. We talked about the company’s journey from GPU cloud to AI infrastructure, why managing AI models is becoming more complex, how companies should think about vendor lock-in, the importance of multi-cloud resiliency, and why compliance may become one of the biggest themes in AI. I’m also a customer of Concentrate AI myself, and it has been great to use. If you’re building with AI models or thinking about cost, uptime, and compliance, definitely check them out. Check out Concentrate AI: Concentrate AI (concentrate.ai), the Best LLM Gateway for Fast Growing Teams. Guest: Ari Jacoby and Zach Moskow Company: Concentrate AI Hosted by: Jack Pitts Check out Concentrate AI: https://concentrate.ai/ Connect with Ari: https://www.linkedin.com/in/arijacoby/ Connect with Zach: https://www.linkedin.com/in/moskow/",
    "metaDescription": "Jack Pitts sits down with Ari Jacoby, Co-Founder and CEO of Concentrate AI, and Zach Moskow, Founding GTM and Ops, on building an LLM gateway.",
    "duration": "31 min",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/concentrate-ai-the-llm-gateway-for-fast-growing-teams/id1853933144?i=1000776113175&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000776113175",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sat down with Ari Jacoby, Co-Founder & CEO of Concentrate AI, and Zach Moskow, Founding GTM & Ops at Concentrate AI. Concentrate recently launched out of stealth after raising $5.1 million and is building an LLM gateway that gives teams one API to access leading AI models, manage token spend, improve reliability, and add security and compliance controls as they scale AI products. We talked about the company’s journey from GPU cloud to AI infrastructure, why managing AI models is becoming more complex, how companies should think about vendor lock-in, the importance of multi-cloud resiliency, and why compliance may become one of the biggest themes in AI. I’m also a customer of Concentrate AI myself, and it has been great to use. If you’re building with AI models or thinking about cost, uptime, and compliance, definitely check them out. Check out Concentrate AI: Concentrate AI (concentrate.ai), the Best LLM Gateway for Fast Growing Teams. Guest: Ari Jacoby and Zach Moskow Company: Concentrate AI Hosted by: Jack Pitts Check out Concentrate AI: https://concentrate.ai/ Connect with Ari: https://www.linkedin.com/in/arijacoby/ Connect with Zach: https://www.linkedin.com/in/moskow/",
    "guid": "a33f6e19-d404-466f-9f12-c4c377dbd091"
  },
  {
    "date": "2026-06-11",
    "dateLabel": "June 11, 2026",
    "title": "In The Making Of: Nishank Gite",
    "guest": "Nishank Gite",
    "slug": "nishank-gite",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, host Jack Pitts sits down with Nishank Gite, Co-Founder & CTO of Nirvana Robotics, to explore Nishank’s journey from physics and AI research into building a robotics company. The conversation covers Nishank’s background in collider physics, machine learning, neural networks, and robotics, along with the realities of building a hard-tech startup. Nishank shares his perspective on fundraising, startup risk, industrial automation, humanoid robots, dark factories, and what it takes to deploy robotics in real-world manufacturing environments. At its core, this episode is about Nishank’s path as a young founder building in one of the hardest and most exciting areas of technology: bringing AI into the physical world.",
    "duration": "1h 3m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-nishank-gite/id1853933144?i=1000772197716&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000772197716",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, host Jack Pitts sits down with Nishank Gite, Co-Founder & CTO of Nirvana Robotics, to explore Nishank’s journey from physics and AI research into building a robotics company. The conversation covers Nishank’s background in collider physics, machine learning, neural networks, and robotics, along with the realities of building a hard-tech startup. Nishank shares his perspective on fundraising, startup risk, industrial automation, humanoid robots, dark factories, and what it takes to deploy robotics in real-world manufacturing environments. At its core, this episode is about Nishank’s path as a young founder building in one of the hardest and most exciting areas of technology: bringing AI into the physical world.",
    "guid": "38496b2a-5305-43c1-8c3b-e2156557e31e"
  },
  {
    "date": "2026-05-21",
    "dateLabel": "May 21, 2026",
    "title": "The Making Of Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas",
    "guest": "Alex Dixon",
    "slug": "alex-dixon",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Alex Dixon, former CEO of Resorts World Las Vegas and former executive at MGM Resorts and Caesars Entertainment. Alex shares his journey from growing up in Las Vegas as a third-generation casino employee to working at Goldman Sachs in New York and London, where he advised on major deals including Disney’s acquisition of Pixar and multi-billion dollar financings. We dive into what it was really like helping build and operate massive casino properties including Horseshoe Baltimore, MGM Springfield, Circus Circus, and Resorts World Las Vegas. Alex also talks about leadership, scaling teams from a handful of employees to thousands, navigating private equity, economic development, casino operations, and the sacrifices required to rise through the gaming and hospitality industry. This episode is packed with insights on business, career growth, hospitality, finance, entrepreneurship, and what it takes to lead billion-dollar operations at some of the biggest names in Las Vegas.",
    "duration": "50 min",
    "guestLinkedIn": "https://www.linkedin.com/in/alexfdixon",
    "links": {
      "spotify": "https://open.spotify.com/episode/58DPxKdLPZjdwvoVm6xdrr",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-alex-dixon-from-goldman-sachs-to/id1853933144?i=1000768906935&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000768906935",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Alex Dixon, former CEO of Resorts World Las Vegas and former executive at MGM Resorts and Caesars Entertainment. Alex shares his journey from growing up in Las Vegas as a third-generation casino employee to working at Goldman Sachs in New York and London, where he advised on major deals including Disney’s acquisition of Pixar and multi-billion dollar financings. We dive into what it was really like helping build and operate massive casino properties including Horseshoe Baltimore, MGM Springfield, Circus Circus, and Resorts World Las Vegas. Alex also talks about leadership, scaling teams from a handful of employees to thousands, navigating private equity, economic development, casino operations, and the sacrifices required to rise through the gaming and hospitality industry. This episode is packed with insights on business, career growth, hospitality, finance, entrepreneurship, and what it takes to lead billion-dollar operations at some of the biggest names in Las Vegas.",
    "guid": "c27c0715-54c4-47b0-861e-ff75b59aaa7b"
  },
  {
    "date": "2026-05-07",
    "dateLabel": "May 7, 2026",
    "title": "The Making Of David Sauers: Building Royal Restrooms Into a Nationwide Franchise",
    "guest": "David Sauers",
    "slug": "david-sauers",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with David Sauers, co-founder of Royal Restrooms, one of the first luxury portable restroom companies in the country. David shares his journey growing up in Savannah, Georgia, working odd jobs as a kid, pursuing professional golf, getting into banking, and eventually building a nationwide franchise business after a frustrating experience at a local festival sparked an idea. We talk about entrepreneurship, risk-taking, franchising, balancing family and business, private equity interest, AI in marketing, and what it really takes to grow a company over 20+ years. David also shares lessons on leadership, sacrifice, branding, and why execution matters more than just having ideas. If you’re interested in entrepreneurship, franchising, business growth, or hearing the real stories behind successful companies, this episode is for you.",
    "duration": "1h 8m",
    "guestLinkedIn": "https://www.linkedin.com/in/davidsauers/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-david-sauers-building-royal-restrooms/id1853933144?i=1000766608021&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000766608021",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with David Sauers, co-founder of Royal Restrooms, one of the first luxury portable restroom companies in the country. David shares his journey growing up in Savannah, Georgia, working odd jobs as a kid, pursuing professional golf, getting into banking, and eventually building a nationwide franchise business after a frustrating experience at a local festival sparked an idea. We talk about entrepreneurship, risk-taking, franchising, balancing family and business, private equity interest, AI in marketing, and what it really takes to grow a company over 20+ years. David also shares lessons on leadership, sacrifice, branding, and why execution matters more than just having ideas. If you’re interested in entrepreneurship, franchising, business growth, or hearing the real stories behind successful companies, this episode is for you.",
    "guid": "7d343e1d-3f0c-48c3-86d4-cf19b359d6db"
  },
  {
    "date": "2026-04-30",
    "dateLabel": "April 30, 2026",
    "title": "In The Making Of: Jesse Choe",
    "guest": "Jesse Choe",
    "slug": "jesse-choe",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Jesse Choe, CEO and Co-Founder of Bidflow. He breaks down his journey from early startup experiments to raising $1M at 19, dropping out of college, and getting into Y Combinator. Jesse shares how his path started with building “fake startups” in high school, learning through failure, and eventually realizing the importance of customer validation and solving real problems. The conversation covers the pivots that actually mattered, the pressure of the YC process, and how rejection and iteration shaped his approach. They also dive into co-founder dynamics, burnout, and how they landed on Bidflow by focusing on a real pain point in electrical estimation. A grounded look at what it actually takes to build something from scratch and figure it out in real time.",
    "duration": "54 min",
    "guestLinkedIn": "https://www.linkedin.com/in/jc10/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-jesse-choe/id1853933144?i=1000764732791&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000764732791",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, I sit down with Jesse Choe, CEO and Co-Founder of Bidflow. He breaks down his journey from early startup experiments to raising $1M at 19, dropping out of college, and getting into Y Combinator. Jesse shares how his path started with building “fake startups” in high school, learning through failure, and eventually realizing the importance of customer validation and solving real problems. The conversation covers the pivots that actually mattered, the pressure of the YC process, and how rejection and iteration shaped his approach. They also dive into co-founder dynamics, burnout, and how they landed on Bidflow by focusing on a real pain point in electrical estimation. A grounded look at what it actually takes to build something from scratch and figure it out in real time.",
    "guid": "3f2bbe93-5018-4e29-bad8-abecfb44a787"
  },
  {
    "date": "2026-04-23",
    "dateLabel": "April 23, 2026",
    "title": "The Making Of Shane Crocker: From Family Business to Multi-Industry Operator",
    "guest": "Shane Crocker",
    "slug": "shane-crocker",
    "description": "On this episode of The Making Of Hosted By Jack Pitts, Shane Crocker shares his journey from growing up in a family business to building and operating across healthcare, oilfield services, and franchising. He breaks down how he approaches scaling in niche markets, making strategic decisions, and navigating private equity involvement from an operator’s perspective. The conversation also gets into leadership, risk-taking, and how he balances building businesses with family life.",
    "duration": "1h 16m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-shane-crocker-from-family-business/id1853933144?i=1000763236988&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000763236988",
    "appleDescription": "On this episode of The Making Of Hosted By Jack Pitts, Shane Crocker shares his journey from growing up in a family business to building and operating across healthcare, oilfield services, and franchising. He breaks down how he approaches scaling in niche markets, making strategic decisions, and navigating private equity involvement from an operator’s perspective. The conversation also gets into leadership, risk-taking, and how he balances building businesses with family life.",
    "guid": "0014fb4d-86ab-4d64-a17e-840e7e8c9f6e"
  },
  {
    "date": "2026-04-09",
    "dateLabel": "April 9, 2026",
    "title": "The Making Of Dave \"Laundromat Millionaire\" Menz",
    "guest": "Dave Menz",
    "slug": "dave-menz",
    "description": "Dave “Laundromat Millionaire” Menz didn’t start with much. He grew up in poverty in Flint, Michigan, wearing hand-me-down clothes and learning early that if he wanted something, he had to go get it. After spending 17 years in a stable corporate job, Dave found himself stuck, comfortable but unfulfilled. Instead of coasting, he made a bet on himself. Alongside his wife Carla, he saved aggressively, lived below their means, and bought a rundown laundromat that was losing money at the time. What followed was years of sacrifice. Working 90–100 hour weeks, reinvesting every dollar, and slowly turning broken businesses into profitable ones. No shortcuts, no outside capital, just grit and consistency. In this episode, Dave breaks down what it actually takes to build something from nothing, the risks most people avoid, and why delayed gratification is the real edge in business.",
    "metaDescription": "Dave Menz grew up in poverty in Flint, Michigan, left a 17-year corporate job, and with his wife Carla bought a rundown laundromat that was losing money.",
    "duration": "1h 23m",
    "guestLinkedIn": "https://www.linkedin.com/in/dave-laundromat-millionaire-menz/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-dave-laundromat-millionaire-menz/id1853933144?i=1000760449322&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000760449322",
    "appleDescription": "Dave “Laundromat Millionaire” Menz didn’t start with much. He grew up in poverty in Flint, Michigan, wearing hand-me-down clothes and learning early that if he wanted something, he had to go get it. After spending 17 years in a stable corporate job, Dave found himself stuck, comfortable but unfulfilled. Instead of coasting, he made a bet on himself. Alongside his wife Carla, he saved aggressively, lived below their means, and bought a rundown laundromat that was losing money at the time. What followed was years of sacrifice. Working 90–100 hour weeks, reinvesting every dollar, and slowly turning broken businesses into profitable ones. No shortcuts, no outside capital, just grit and consistency. In this episode, Dave breaks down what it actually takes to build something from nothing, the risks most people avoid, and why delayed gratification is the real edge in business.",
    "guid": "ab0f5e58-a52f-4cd0-958f-dfcac62eab14"
  },
  {
    "date": "2026-03-26",
    "dateLabel": "March 26, 2026",
    "title": "The Making Of Lou Mongello: From Lawyer to Disney Entrepreneur",
    "guest": "Lou Mongello",
    "slug": "lou-mongello",
    "description": "In this conversation, Lou Mongello shares how he went from practicing law to building a career around his passion for Disney. He talks about the early influences that shaped his entrepreneurial mindset, the challenge of balancing family and work, and why focusing on community became the foundation of his success. Drawing inspiration from Walt Disney, Lou explains the principles that guide both his business and his life, and why making a positive impact and giving back matter more than metrics. Listen to the full episode for a real look at how to turn passion into a career, build a loyal community, and make decisions without regret, all through the lens of Lou Mongello’s journey.",
    "duration": "1h 12m",
    "guestLinkedIn": "https://www.linkedin.com/in/loumongello/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-lou-mongello-from-lawyer-to/id1853933144?i=1000757482795&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000757482795",
    "appleDescription": "In this conversation, Lou Mongello shares how he went from practicing law to building a career around his passion for Disney. He talks about the early influences that shaped his entrepreneurial mindset, the challenge of balancing family and work, and why focusing on community became the foundation of his success. Drawing inspiration from Walt Disney, Lou explains the principles that guide both his business and his life, and why making a positive impact and giving back matter more than metrics. Listen to the full episode for a real look at how to turn passion into a career, build a loyal community, and make decisions without regret, all through the lens of Lou Mongello’s journey.",
    "guid": "413b0304-5e3c-4bc8-873d-ffe9dbc8433d"
  },
  {
    "date": "2026-03-12",
    "dateLabel": "March 12, 2026",
    "title": "In The Making Of: Niilo Pirttijärvi",
    "guest": "Niilo Pirttijärvi",
    "slug": "niilo-pirttij-rvi",
    "description": "On this episode of The Making Of Hosted By Jack Pitts, I sat down with Niilo Pirttijärvi, the co-founder & CEO of Inven, to talk about how AI is changing the way private equity firms find and analyze deals. We talked about how sourcing has traditionally worked in private equity and why Niilo believed there was an opportunity to rethink it using AI. He walked me through his path from McKinsey & Company to starting Inven, the early days of building the product, and what it took to land their first customers. What stood out to me was how much relationships still matter in private equity, even as technology gets more powerful. We also got into the realities of building a SaaS startup, working with VCs, and where tools like Inven could take the industry next. If you're interested in startups, private equity, or how AI is actually being used in business today, I think you’ll enjoy this conversation.",
    "duration": "51 min",
    "guestLinkedIn": "https://www.linkedin.com/in/niilo-pirttijarvi/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-niilo-pirttij%C3%A4rvi/id1853933144?i=1000754836096&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000754836096",
    "appleDescription": "On this episode of The Making Of Hosted By Jack Pitts, I sat down with Niilo Pirttijärvi, the co-founder & CEO of Inven, to talk about how AI is changing the way private equity firms find and analyze deals. We talked about how sourcing has traditionally worked in private equity and why Niilo believed there was an opportunity to rethink it using AI. He walked me through his path from McKinsey & Company to starting Inven, the early days of building the product, and what it took to land their first customers. What stood out to me was how much relationships still matter in private equity, even as technology gets more powerful. We also got into the realities of building a SaaS startup, working with VCs, and where tools like Inven could take the industry next. If you're interested in startups, private equity, or how AI is actually being used in business today, I think you’ll enjoy this conversation.",
    "guid": "2d4678c0-2f51-4bf4-bace-4129f862225b"
  },
  {
    "date": "2026-02-26",
    "dateLabel": "February 26, 2026",
    "title": "The Making of Kris Carlson: From Sales to Seafood",
    "guest": "Kris Carlson",
    "slug": "kris-carlson",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, Jack interviews Kris Carlson, President and COO of The Fish Guys. Kris shares his journey from growing up in Champaign, Illinois, to building a career in sales at Reuters, and ultimately leading a growing food distribution company. He discusses how sports, Greek life, and teamwork shaped his leadership, and the lessons he learned navigating challenges early in his career. Kris also explains how he helped The Fish Guys adapt and grow during COVID-19, including launching an e-commerce platform, and shares insights on leadership, community, and building a dedicated team. This episode is packed with practical advice and inspiration for anyone interested in entrepreneurship, leadership, and overcoming challenges in business.",
    "duration": "1h 24m",
    "guestLinkedIn": "https://www.linkedin.com/in/kris-carlson-b57b682",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-kris-carlson-from-sales-to-seafood/id1853933144?i=1000751740327&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000751740327",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, Jack interviews Kris Carlson, President and COO of The Fish Guys. Kris shares his journey from growing up in Champaign, Illinois, to building a career in sales at Reuters, and ultimately leading a growing food distribution company. He discusses how sports, Greek life, and teamwork shaped his leadership, and the lessons he learned navigating challenges early in his career. Kris also explains how he helped The Fish Guys adapt and grow during COVID-19, including launching an e-commerce platform, and shares insights on leadership, community, and building a dedicated team. This episode is packed with practical advice and inspiration for anyone interested in entrepreneurship, leadership, and overcoming challenges in business.",
    "guid": "8751ff19-3413-4406-a4cd-6e9e10e42562"
  },
  {
    "date": "2026-02-05",
    "dateLabel": "February 5, 2026",
    "title": "In The Making Of: Ian Hicks",
    "guest": "Ian Hicks",
    "slug": "ian-hicks",
    "description": "This is a new style for my podcast. Join my conversation with my good friend, Ian Hicks. Ian works at King Industrial in Atlanta as a broker. Ian came and visited me in NYC in December. In this episode, we share candid stories about life in New York City, building businesses, navigating friendships across distances, and the realities of entrepreneurship. Whether you're into real estate, travel, or just seeking to listen to a genuine conversation between two long time pals, this convo offers unfiltered insights into living intentionally and embracing the chaos.",
    "metaDescription": "Jack Pitts talks with his longtime friend Ian Hicks, a broker at King Industrial in Atlanta, about life in New York City, friendship, and building businesses.",
    "duration": "1h 3m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/in-the-making-of-ian-hicks/id1853933144?i=1000748365273&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000748365273",
    "appleDescription": "This a new style for my podcast. Join my conversation with my good friend, Ian Hicks. Ian works at King Industrial in Atlanta as a broker. Ian came and visited me in NYC in December. In this episode, we share candid stories about life in New York City, building businesses, navigating friendships across distances, and the realities of entrepreneurship. Whether you're into real estate, travel, or just seeking to listen to a genuine conversation between two long time pals, this convo offers unfiltered insights into living intentionally and embracing the chaos.",
    "guid": "a35fefa2-47a8-4f7f-8016-e29874bbb495"
  },
  {
    "date": "2026-01-22",
    "dateLabel": "January 22, 2026",
    "title": "The Making of Robbie Ferman: From Brokerage to Building Sollevare Group",
    "guest": "Robbie Ferman",
    "slug": "robbie-ferman",
    "description": "In this episode, Robbie Ferman, co-founder and managing partner of Sollevare Group, shares his journey from corporate real estate to entrepreneurship. He discusses the importance of building relationships, the challenges of navigating the New York real estate market, and the significance of discipline and mentorship in achieving success. Robbie also reflects on his first deal, the importance of managing investor expectations, and the compelling demographic trends driving their investment strategy. As he looks to the future, he emphasizes the need for discipline in their investment approach and the goal of raising more capital for upcoming projects.",
    "duration": "46 min",
    "guestLinkedIn": "https://www.linkedin.com/in/robert-ferman-2824b2153/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-robbie-ferman-from-brokerage-to/id1853933144?i=1000746199517&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000746199517",
    "appleDescription": "In this episode, Robbie Ferman, co-founder and managing partners of Sollevare Group, shares his journey from corporate real estate to entrepreneurship. He discusses the importance of building relationships, the challenges of navigating the New York real estate market, and the significance of discipline and mentorship in achieving success. Robbie also reflects on his first deal, the importance of managing investor expectations, and the compelling demographic trends driving their investment strategy. As he looks to the future, he emphasizes the need for discipline in their investment approach and the goal of raising more capital for upcoming projects.",
    "guid": "f5718eb3-5794-4cda-bc7a-7633d8ff6708"
  },
  {
    "date": "2026-01-08",
    "dateLabel": "January 8, 2026",
    "title": "The Making of Doug Taylor: Taylor's Candy",
    "guest": "Doug Taylor",
    "slug": "doug-taylor",
    "description": "In this episode, Jack Pitts interviews Doug Taylor, known as the Candyman, who shares his journey of building Taylor's Candy from a small family-run operation into a successful candy distribution and manufacturing business. Doug discusses his upbringing, early jobs, and the transition into the candy industry, highlighting the importance of hard work, family dynamics, and adapting to market changes. He also reflects on the impact of COVID-19, the acquisition of Windy City Popcorn, and future plans for the business, emphasizing the significance of relationships and networking in the industry.",
    "duration": "1h 5m",
    "tag": "press",
    "guestLinkedIn": "https://www.linkedin.com/in/doug-taylor-21a73917/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-doug-taylor-taylors-candy/id1853933144?i=1000744284254&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000744284254",
    "appleDescription": "In this episode, Jack Pitts interviews Doug Taylor, known as the Candyman, who shares his journey of building Taylor's Candy from a small family-run operation into a successful candy distribution and manufacturing business. Doug discusses his upbringing, early jobs, and the transition into the candy industry, highlighting the importance of hard work, family dynamics, and adapting to market changes. He also reflects on the impact of COVID-19, the acquisition of Windy City Popcorn, and future plans for the business, emphasizing the significance of relationships and networking in the industry.",
    "guid": "11dac819-c961-4a23-8295-7e2ea0812eaa"
  },
  {
    "date": "2025-12-18",
    "dateLabel": "December 18, 2025",
    "title": "The Making of Adam Stevenson: From Flipping Burgers to Building Businesses",
    "guest": "Adam Stevenson",
    "slug": "adam-stevenson",
    "description": "In this conversation, Adam Stevenson shares his inspiring journey from a low-income upbringing in Detroit to becoming a successful entrepreneur. He discusses his early experiences flipping burgers, starting a landscaping business, and navigating college life while balancing sports and side hustles. The birth of Grassroots Records, a music label he co-founded, highlights his passion for music and community. Throughout the conversation, Adam reflects on the challenges of imposter syndrome and the importance of seizing opportunities, networking, and hard work in achieving success. In this conversation, Adam Stevenson shares his journey through the music industry, the challenges of entrepreneurship, and the importance of perseverance. He discusses the founding of B-Side Cafe, the struggles with partnerships, and the eventual success of AdRock, a marketing and merchandising company. Adam also highlights his experience with Xtreme Xperience, a supercar driving venture, and his current focus on NASS Holdings, where he aims to invest in and mentor young entrepreneurs. Throughout the discussion, he emphasizes the significance of recognizing opportunities, the impact of timing, and the value of personal growth and accountability.",
    "metaDescription": "Adam Stevenson on growing up in Detroit, flipping burgers, starting a landscaping business, and co-founding the music label Grassroots Records.",
    "duration": "1h 32m",
    "guestLinkedIn": "https://www.linkedin.com/in/adamstevenson/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-adam-stevenson-from-flipping-burgers/id1853933144?i=1000741828291&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000741828291",
    "appleDescription": "In this conversation, Adam Stevenson shares his inspiring journey from a low-income upbringing in Detroit to becoming a successful entrepreneur. He discusses his early experiences flipping burgers, starting a landscaping business, and navigating college life while balancing sports and side hustles. The birth of Grassroots Records, a music label he co-founded, highlights his passion for music and community. Throughout the conversation, Adam reflects on the challenges of imposter syndrome and the importance of seizing opportunities, networking, and hard work in achieving success. In this conversation, Adam Stevenson shares his journey through the music industry, the challenges of entrepreneurship, and the importance of perseverance. He discusses the founding of B-Side Cafe, the struggles with partnerships, and the eventual success of AdRock, a marketing and merchandising company. Adam also highlights his experience with Xtreme Xperience, a supercar driving venture, and his current focus on NASS Holdings, where he aims to invest in and mentor young entrepreneurs. Throughout the discussion, he emphasizes the significance of recognizing opportunities, the impact of timing, and the value of personal growth and accountability.",
    "guid": "63dad01c-bd2a-42bb-87a5-364960a41727"
  },
  {
    "date": "2025-11-18",
    "dateLabel": "November 18, 2025",
    "title": "The Making of Mammoth Holdings with Gary Dennis",
    "guest": "Gary Dennis",
    "slug": "gary-dennis",
    "description": "In this episode of The Making Of Hosted By Jack Pitts, Jack sits down with Gary Dennis, co-founder and former CEO of Mammoth Holdings, to unpack how a kid from Macon, Georgia ended up building one of the leading car wash platforms in the country. Gary walks through his path from humble beginnings, with a dad who was a maintenance mechanic and a mom who was a secretary, to Georgia Tech, an MBA from Vanderbilt, and an early career in equity research and investment banking. He shares how getting humbled by a boss during his college co-op and by money managers on Wall Street shaped the way he thinks about work, preparation, and actually understanding the numbers. From there, Gary breaks down the jump from a comfortable investment banking career into owning and operating car washes. He explains: How a “side hustle” idea turned into Mammoth’s first self-serve washThe trip to Louisiana that exposed him to the express wash modelWhy he thinks of car washes as manufacturing plants, not retailWhat the 2008–2009 downturn and months of nonstop rain did to the businessHow a mispriced early subscription product almost flopped, and the data that helped them finally get it rightTaking site-level break-even from ~7,000 cars a month to zero with membershipsGary also talks about building Mammoth into a true multi-state platform through development and more than 30 acquisitions, why their internal rule was “no jerks allowed,” and how they structured deals so great owner-operators could roll equity and stay involved. Finally, he reflects on partnering with institutional capital (including the Pritzker Organization), stepping back from the CEO role after nearly 20 years, staying involved as chairman, and how he now splits his time between board work, investing, his alma maters, and advocacy around long-term housing for adults with developmental disabilities. If you’re thinking about leaving a “safe” job, scaling a gritty real-world business, or just want an honest look at the grind behind a 20+ year “overnight success,” this conversation with Gary is worth a listen.",
    "duration": "1h 22m",
    "tag": "first",
    "guestLinkedIn": "https://www.linkedin.com/in/gary-dennis-000010b/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-mammoth-holdings-with-gary-dennis/id1853933144?i=1000737312111&uo=4",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    },
    "appleEpisodeId": "1000737312111",
    "appleDescription": "In this episode of The Making Of Hosted By Jack Pitts, Jack Pitts sits down with Gary Dennis, co-founder and former CEO of Mammoth Holdings, to unpack how a kid from Macon, Georgia ended up building one of the leading car wash platforms in the country. Gary walks through his path from humble beginnings, with a dad who was a maintenance mechanic and a mom who was a secretary, to Georgia Tech, an MBA from Vanderbilt, and an early career in equity research and investment banking. He shares how getting humbled by a boss during his college co-op and by money managers on Wall Street shaped the way he thinks about work, preparation, and actually understanding the numbers. From there, Gary breaks down the jump from a comfortable investment banking career into owning and operating car washes. He explains: How a “side hustle” idea turned into Mammoth’s first self-serve washThe trip to Louisiana that exposed him to the express wash modelWhy he thinks of car washes as manufacturing plants, not retailWhat the 2008–2009 downturn and months of nonstop rain did to the businessHow a mispriced early subscription product almost flopped, and the data that helped them finally get it rightTaking site-level break-even from ~7,000 cars a month to zero with membershipsGary also talks about building Mammoth into a true multi-state platform through development and more than 30 acquisitions, why their internal rule was “no jerks allowed,” and how they structured deals so great owner-operators could roll equity and stay involved. Finally, he reflects on partnering with institutional capital (including the Pritzker Organization), stepping back from the CEO role after nearly 20 years, staying involved as chairman, and how he now splits his time between board work, investing, his alma maters, and advocacy around long-term housing for adults with developmental disabilities. If you’re thinking about leaving a “safe” job, scaling a gritty real-world business, or just want an honest look at the grind behind a 20+ year “overnight success,” this conversation with Gary is worth a listen.",
    "guid": "Buzzsprout-18213112"
  }
];
