#!/usr/bin/env python3
"""
Hand-written search titles and guest-card lines for episode pages.

Both maps are keyed by episode slug (seo_urls.episode_slug), so they keep
working when a guest's display name is corrected, as long as the slug is
pinned in episodes.js.

SEO_TITLES
    Used for <title>, og:title and twitter:title when an episode's published
    title leaves out the guest or the company. The visible headline stays the
    published title. An episodes.js "seoTitle" field overrides an entry here.
    Rules: 50-65 characters, guest first, then company, no em dashes, never
    the show name (page_title() appends it when there is room).

GUEST_LINES
    One factual line for the "About the guest" card. Every fact comes from that
    episode's own description in episodes.js. Episodes without an entry get a
    short neutral line instead, so a new episode never ships invented copy.
"""

SEO_TITLES: dict[str, str] = {
    "from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley":
        "Scott Burnley: From Delivering Ice to Pet Station Country Club",
    "how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott":
        "Rick Franco and Mike Trott on Building Four Branches Bourbon",
    "dave-moorman":
        "Dave Moorman on Building DynaSis and Exiting Twice",
    "davies-hood-of-induron-protective-coatings":
        "Davies Hood on Running Induron, a Family Business Since 1947",
    "concentrate-ai":
        "Ari Jacoby and Zach Moskow of Concentrate AI: The LLM Gateway",
    "nishank-gite":
        "Nishank Gite of Nirvana Robotics: From Physics to Robotics",
    "jesse-choe":
        "Jesse Choe of Bidflow: Raising $1M at 19 and Getting Into YC",
    "niilo-pirttij-rvi":
        "Niilo Pirttijärvi of Inven: AI for Private Equity Deal Sourcing",
    "kris-carlson":
        "Kris Carlson of The Fish Guys: From Reuters Sales to Seafood",
    "ian-hicks":
        "Ian Hicks of King Industrial on Brokerage, NYC and Friendship",
    "doug-taylor":
        "Doug Taylor on Growing Taylor's Candy From a Family Operation",
    "adam-stevenson":
        "Adam Stevenson: From Flipping Burgers to Grassroots Records",
    "alex-dixon":
        "Alex Dixon: From Goldman Sachs to CEO of Resorts World Las Vegas",
    "david-sauers":
        "David Sauers: Growing Royal Restrooms Into a Nationwide Franchise",
    "shane-crocker":
        "Shane Crocker: From Family Business to Multi-Industry Operator",
    "robbie-ferman":
        "Robbie Ferman: From Brokerage to Building Sollevare Group",
}

GUEST_LINES: dict[str, str] = {
    "from-selling-ice-to-building-a-140-person-pet-care-business-scott-burnley":
        "Went from delivering bags of ice to helping build Pet Station Country "
        "Club into three locations with around 140 employees.",
    "how-four-veterans-built-four-branches-bourbon-rick-franco-mike-trott":
        "Co-founders of Four Branches Bourbon, which started as an honor barrel "
        "created by four veterans.",
    "dave-moorman":
        "Built DynaSis over 26 years, sold it to Novatech, and later went "
        "through a second exit.",
    "davies-hood-of-induron-protective-coatings":
        "President of Induron Protective Coatings, a third-generation family "
        "business founded in Birmingham in 1947.",
    "concentrate-ai":
        "Ari Jacoby is Co-Founder and CEO of Concentrate AI. Zach Moskow is "
        "Founding GTM and Ops at the company.",
    "nishank-gite":
        "Co-Founder and CTO of Nirvana Robotics, with a background in collider "
        "physics and AI research.",
    "alex-dixon":
        "Former CEO of Resorts World Las Vegas and a former executive at MGM "
        "Resorts and Caesars Entertainment.",
    "david-sauers":
        "Co-founder of Royal Restrooms, which he built into a nationwide "
        "franchise business.",
    "jesse-choe":
        "CEO and Co-Founder of Bidflow. Raised $1M at 19, left college, and got "
        "into Y Combinator.",
    "shane-crocker":
        "Grew up in a family business and now operates across healthcare, "
        "oilfield services, and franchising.",
    "dave-menz":
        "Left a 17-year corporate job and, with his wife Carla, bought a "
        "rundown laundromat that was losing money.",
    "lou-mongello":
        "Went from practicing law to building a career around his passion for "
        "Disney.",
    "niilo-pirttij-rvi":
        "Co-founder and CEO of Inven, which he started after McKinsey & Company.",
    "kris-carlson":
        "President and COO of The Fish Guys, after an early career in sales at "
        "Reuters.",
    "ian-hicks":
        "A broker at King Industrial in Atlanta, and a longtime friend of Jack's.",
    "robbie-ferman":
        "Co-founder and managing partner of Sollevare Group, after starting out "
        "in corporate real estate.",
    "doug-taylor":
        "Known as the Candyman. Built Taylor's Candy from a small family-run "
        "operation into a candy distribution and manufacturing business.",
    "adam-stevenson":
        "Grew up in Detroit, started a landscaping business, and co-founded the "
        "music label Grassroots Records.",
    "gary-dennis":
        "Co-founder and former CEO of Mammoth Holdings, one of the leading car "
        "wash platforms in the country.",
}
