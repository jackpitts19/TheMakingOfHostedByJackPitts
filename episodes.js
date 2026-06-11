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
    "date": "2026-05-21",
    "dateLabel": "May 21, 2026",
    "title": "The Making Of Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas",
    "guest": "Alex Dixon",
    "description": "Alex Dixon, former CEO of Resorts World Las Vegas, on growing up a third-generation casino kid in Vegas, advising on Disney's acquisition of Pixar at Goldman Sachs, and leading billion-dollar gaming operations at MGM, Caesars, and Resorts World.",
    "duration": "50 min",
    "guestLinkedIn": "https://www.linkedin.com/in/alexfdixon",
    "links": {
      "spotify": "https://open.spotify.com/episode/58DPxKdLPZjdwvoVm6xdrr",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-05-07",
    "dateLabel": "May 7, 2026",
    "title": "The Making Of David Sauers: Building Royal Restrooms Into a Nationwide Franchise",
    "guest": "David Sauers",
    "description": "David Sauers, co-founder of Royal Restrooms, on his path from Savannah through golf and banking to building a luxury portable restroom franchise over 20+ years.",
    "duration": "1h 8m",
    "guestLinkedIn": "https://www.linkedin.com/in/davidsauers/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-04-30",
    "dateLabel": "April 30, 2026",
    "title": "In The Making Of: Jesse Choe",
    "guest": "Jesse Choe",
    "description": "Jesse Choe, CEO and co-founder of Bidflow, on raising $1M at 19, Y Combinator, and finding product-market fit through customer validation.",
    "duration": "54 min",
    "guestLinkedIn": "https://www.linkedin.com/in/jc10/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-04-23",
    "dateLabel": "April 23, 2026",
    "title": "The Making Of Shane Crocker: From Family Business to Multi-Industry Operator",
    "guest": "Shane Crocker",
    "description": "Shane Crocker on the transition from family business roots to scaling across healthcare, oilfield services, and franchising, including private equity involvement.",
    "duration": "1h 16m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-04-09",
    "dateLabel": "April 9, 2026",
    "title": "The Making Of Dave \"Laundromat Millionaire\" Menz",
    "guest": "Dave Menz",
    "description": "Dave Menz on going from poverty in Flint, Michigan and 17 years of corporate work to building profitable laundromats with his wife through aggressive saving and 90 to 100 hour weeks.",
    "duration": "1h 23m",
    "guestLinkedIn": "https://www.linkedin.com/in/dave-laundromat-millionaire-menz/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-03-26",
    "dateLabel": "March 26, 2026",
    "title": "The Making Of Lou Mongello: From Lawyer to Disney Entrepreneur",
    "guest": "Lou Mongello",
    "description": "Lou Mongello on trading law for a Disney-focused career, with an emphasis on community building, positive impact, and Walt Disney principles over metrics.",
    "duration": "1h 12m",
    "guestLinkedIn": "https://www.linkedin.com/in/loumongello/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-03-12",
    "dateLabel": "March 12, 2026",
    "title": "In The Making Of: Niilo Pirttijärvi",
    "guest": "Niilo Pirttijärvi",
    "description": "Niilo Pirttijärvi, co-founder and CEO of Inven, on how AI is transforming private equity deal sourcing and analysis, from McKinsey to startup founder.",
    "duration": "51 min",
    "guestLinkedIn": "https://www.linkedin.com/in/niilo-pirttijarvi/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-02-26",
    "dateLabel": "February 26, 2026",
    "title": "The Making of Kris Carlson: From Sales to Seafood",
    "guest": "Kris Carlson",
    "description": "Kris Carlson, President and COO of The Fish Guys, on his Reuters sales career and leading a food distribution company through COVID-19 adaptation and e-commerce.",
    "duration": "1h 24m",
    "guestLinkedIn": "https://www.linkedin.com/in/kris-carlson-b57b682",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-02-05",
    "dateLabel": "February 5, 2026",
    "title": "In The Making Of: Ian Hicks",
    "guest": "Ian Hicks",
    "description": "A candid conversation with Ian Hicks, a broker at King Industrial in Atlanta, on NYC living, business building, and long-distance friendships.",
    "duration": "1h 3m",
    "guestLinkedIn": "",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-01-22",
    "dateLabel": "January 22, 2026",
    "title": "The Making of Robbie Ferman: From Brokerage to Building Sollevare Group",
    "guest": "Robbie Ferman",
    "description": "Robbie Ferman, co-founder of Sollevare Group, on his real estate journey, the importance of relationship building, and demographic-driven investment strategies.",
    "duration": "46 min",
    "guestLinkedIn": "https://www.linkedin.com/in/robert-ferman-2824b2153/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2026-01-08",
    "dateLabel": "January 8, 2026",
    "title": "The Making of Doug Taylor: Taylor's Candy",
    "guest": "Doug Taylor",
    "description": "Doug Taylor, the Candyman, on building Taylor's Candy from a family operation into a distribution and manufacturing business. Featured in the Riverside-Brookfield Landmark.",
    "duration": "1h 5m",
    "tag": "press",
    "guestLinkedIn": "https://www.linkedin.com/in/doug-taylor-21a73917/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2025-12-18",
    "dateLabel": "December 18, 2025",
    "title": "The Making of Adam Stevenson: From Flipping Burgers to Building Businesses",
    "guest": "Adam Stevenson",
    "description": "Adam Stevenson on a low-income Detroit upbringing through landscaping, Grassroots Records, B-Side Cafe, AdRock marketing, and current focus at NASS Holdings.",
    "duration": "1h 32m",
    "guestLinkedIn": "https://www.linkedin.com/in/adamstevenson/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  },
  {
    "date": "2025-11-18",
    "dateLabel": "November 18, 2025",
    "title": "The Making of Mammoth Holdings with Gary Dennis",
    "guest": "Gary Dennis",
    "description": "Gary Dennis, co-founder and former CEO of Mammoth Holdings, on building a leading car wash platform from humble Georgia beginnings through Georgia Tech, investment banking, and 20+ years of operations. The first episode of the show.",
    "duration": "1h 22m",
    "tag": "first",
    "guestLinkedIn": "https://www.linkedin.com/in/gary-dennis-000010b/",
    "links": {
      "spotify": "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH",
      "apple": "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144",
      "youtube": "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
    }
  }
];
