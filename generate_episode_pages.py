#!/usr/bin/env python3
"""
Generate one polished page per episode of The Making Of Hosted By Jack Pitts.

Reads episodes.js, writes ./episodes/<slug>.html for each entry. Each page is
self-contained editorial HTML: oversized serif headline, Spotify embed, lede,
guest LinkedIn CTA (when known), share-card hero image, and a "More from the
show" related-episodes strip at the bottom.

Pages share the slug system used by generate_share_cards.py so the OG image
URL (../share-cards/<slug>.png) always matches.
"""

import json
import re
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"
OUT_DIR = ROOT / "episodes"
OUT_DIR.mkdir(exist_ok=True)

SITE = "The Making Of Hosted By Jack Pitts"
SITE_URL = "https://themakingofhostedbyjackpitts.com"
SHOW_SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
SHOW_APPLE = "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
SHOW_YT = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"
JACK_LI = "https://www.linkedin.com/in/jack-pitts"
BOOK_CAL = "https://calendar.app.google/8s9JEAriAqG2qS7MA"


def load_episodes():
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise RuntimeError("Could not parse episodes.js")
    return json.loads(m.group(1))


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "-", name.lower()).strip("-")
    return s or "episode"


def split_title(title):
    """Pull the strong half ('The Making Of Alex Dixon') from the subtitle."""
    if ":" in title:
        head, sub = title.split(":", 1)
        return head.strip(), sub.strip()
    return title.strip(), ""


def spotify_embed_src(spotify_url):
    if not spotify_url:
        return None
    m = re.search(r"episode/([A-Za-z0-9]+)", spotify_url)
    if m:
        return f"https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&theme=0"
    m = re.search(r"show/([A-Za-z0-9]+)", spotify_url)
    if m:
        return f"https://open.spotify.com/embed/show/{m.group(1)}?utm_source=generator&theme=0"
    return None


def issue_label(n):
    return f"No. {n:02d}"


CSS = r"""
:root {
  --cream: #f3e8cf;
  --cream-deep: #ecd9a8;
  --orange: #d87a2c;
  --orange-dark: #b85f18;
  --ink: #14130f;
  --ink-soft: #3a352b;
  --line: rgba(20,19,15,0.12);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--cream); color: var(--ink); }
body { font-family: 'Inter', system-ui, -apple-system, sans-serif; line-height: 1.55; }
a { color: inherit; }
img { max-width: 100%; display: block; }

/* Paper grain, very subtle, magazine feel */
body::before {
  content: '';
  position: fixed; inset: 0;
  pointer-events: none; z-index: 1;
  opacity: 0.045; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='nf'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23nf)'/%3E%3C/svg%3E");
}
body > * { position: relative; z-index: 2; }

.wrap { max-width: 780px; margin: 0 auto; padding: 0 28px; }

/* Top nav */
.topnav {
  border-bottom: 1px solid var(--line);
  padding: 18px 0;
  background: rgba(243,232,207,0.92);
  backdrop-filter: blur(6px);
  position: sticky; top: 0; z-index: 5;
}
.topnav .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.topnav .mark {
  font-family: 'Fraunces', serif; font-weight: 800; font-size: 18px;
  letter-spacing: -0.01em; color: var(--ink); text-decoration: none;
}
.topnav .mark span { color: var(--orange); font-style: italic; font-weight: 600; }
.topnav .back {
  text-decoration: none; color: var(--ink-soft);
  font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase;
  font-weight: 600;
  display: inline-flex; align-items: center; gap: 8px;
}
.topnav .back::before { content: "\2190"; color: var(--orange-dark); font-size: 16px; }
.topnav .back:hover { color: var(--ink); }

/* Masthead meta line under nav */
.masthead {
  padding: 56px 0 18px;
  display: flex; flex-wrap: wrap; gap: 14px;
  font-family: 'Inter', sans-serif;
  font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--ink-soft); font-weight: 600;
}
.masthead .issue { color: var(--orange-dark); font-weight: 800; }
.masthead .dot { width: 4px; height: 4px; background: var(--ink-soft); border-radius: 50%; opacity: 0.6; align-self: center; }

/* Hero headline */
.hero-title {
  font-family: 'Fraunces', serif;
  font-weight: 800; line-height: 1.02;
  font-size: clamp(38px, 6.4vw, 76px);
  letter-spacing: -0.025em;
  margin: 0 0 18px;
  color: var(--ink);
}
.hero-title em { font-style: italic; color: var(--orange-dark); font-weight: 700; }
.hero-sub {
  font-family: 'Fraunces', serif; font-weight: 500;
  font-size: clamp(20px, 2.4vw, 30px);
  line-height: 1.28; color: var(--ink-soft);
  letter-spacing: -0.005em;
  margin: 0 0 36px;
  max-width: 660px;
}
.hero-lede {
  font-family: 'Fraunces', serif; font-weight: 400;
  font-size: clamp(19px, 2vw, 24px);
  line-height: 1.45; color: var(--ink);
  margin: 0 0 40px;
  padding-left: 18px;
  border-left: 3px solid var(--orange);
}

/* Spotify player */
.player {
  margin: 0 0 28px;
  border-radius: 14px; overflow: hidden;
  box-shadow: 0 28px 60px -36px rgba(20,19,15,0.6);
}
.player iframe { display: block; width: 100%; border: 0; background: transparent; }

/* Listen anywhere row */
.listen-row { display: flex; flex-wrap: wrap; gap: 10px; margin: 0 0 44px; }
.listen-row a {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 16px; border-radius: 999px;
  border: 1px solid var(--line); background: rgba(255,255,255,0.4);
  text-decoration: none; color: var(--ink);
  font-size: 13.5px; font-weight: 600; letter-spacing: 0.02em;
  transition: transform .15s, background .15s, border-color .15s;
}
.listen-row a:hover { transform: translateY(-2px); background: var(--ink); color: var(--cream); border-color: var(--ink); }
.listen-row a svg { width: 14px; height: 14px; }

/* Section heading */
.sec-eyebrow {
  font-family: 'Fraunces', serif; font-style: italic; font-weight: 600;
  font-size: 18px; color: var(--orange-dark); margin: 56px 0 12px;
}
.sec-rule { height: 1px; background: var(--line); margin: 0 0 28px; }

/* Long body copy */
.body p {
  font-family: 'Fraunces', serif; font-weight: 400;
  font-size: 20px; line-height: 1.62; color: var(--ink);
  margin: 0 0 22px;
  letter-spacing: -0.003em;
}

/* About the guest */
.guest-card {
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 28px 26px;
  background: rgba(236, 217, 168, 0.45);
  margin: 14px 0 0;
}
.guest-card .gc-eyebrow {
  font-family: 'Inter', sans-serif; font-size: 11.5px;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--ink-soft); font-weight: 700;
  margin-bottom: 10px;
}
.guest-card h3 {
  font-family: 'Fraunces', serif; font-weight: 800;
  font-size: 30px; letter-spacing: -0.015em;
  margin: 0 0 8px; color: var(--ink);
}
.guest-card p {
  font-family: 'Fraunces', serif; font-size: 17px;
  color: var(--ink-soft); margin: 0 0 18px; line-height: 1.5;
}
.guest-card .gc-cta {
  display: inline-flex; align-items: center; gap: 8px;
  background: #0a66c2; color: #fff;
  padding: 12px 20px; border-radius: 999px;
  text-decoration: none; font-weight: 700; font-size: 14px;
  letter-spacing: 0.01em;
}
.guest-card .gc-cta:hover { transform: translateY(-2px); }
.guest-card .gc-cta svg { width: 16px; height: 16px; }

/* Share card figure */
.share-fig {
  margin: 60px 0 24px;
  border-radius: 16px; overflow: hidden;
  box-shadow: 0 30px 60px -30px rgba(20,19,15,0.5);
  border: 1px solid var(--line);
}
.share-fig figcaption {
  font-family: 'Inter', sans-serif; font-size: 11.5px;
  text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--ink-soft); padding: 12px 16px;
  background: rgba(255,255,255,0.4);
  border-top: 1px solid var(--line);
}

/* More from the show */
.related {
  border-top: 1px solid var(--line);
  margin-top: 70px;
  padding-top: 36px;
}
.related h2 {
  font-family: 'Fraunces', serif; font-weight: 800;
  font-size: 30px; letter-spacing: -0.015em;
  margin: 0 0 24px;
}
.related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.r-card {
  border: 1px solid var(--line); border-radius: 12px;
  padding: 18px 18px 20px; background: rgba(255,255,255,0.35);
  text-decoration: none; color: var(--ink);
  display: block;
  transition: transform .15s, border-color .15s, background .15s;
}
.r-card:hover { transform: translateY(-3px); border-color: var(--orange); background: rgba(255,255,255,0.6); }
.r-card .r-issue {
  font-family: 'Inter', sans-serif; font-size: 11px;
  letter-spacing: 0.16em; text-transform: uppercase; font-weight: 700;
  color: var(--orange-dark); margin-bottom: 8px;
}
.r-card .r-title {
  font-family: 'Fraunces', serif; font-weight: 700;
  font-size: 18px; line-height: 1.25; color: var(--ink);
  margin: 0 0 10px; letter-spacing: -0.01em;
}
.r-card .r-dur {
  font-size: 12px; color: var(--ink-soft);
  font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
}

/* CTA strip to book */
.book-strip {
  margin: 70px 0 50px;
  padding: 36px 32px;
  background: var(--ink); color: var(--cream);
  border-radius: 18px;
  display: flex; align-items: center; justify-content: space-between;
  gap: 28px; flex-wrap: wrap;
}
.book-strip h3 {
  font-family: 'Fraunces', serif; font-weight: 800;
  font-size: 24px; margin: 0 0 6px; letter-spacing: -0.01em;
  color: var(--cream);
}
.book-strip h3 em { color: var(--orange); font-style: italic; }
.book-strip p { margin: 0; font-size: 14.5px; color: rgba(243,232,207,0.78); max-width: 460px; }
.book-strip a {
  background: var(--orange); color: var(--ink);
  padding: 14px 22px; border-radius: 999px;
  font-weight: 700; text-decoration: none; font-size: 14px;
  letter-spacing: 0.01em; white-space: nowrap;
  transition: transform .15s, background .15s;
}
.book-strip a:hover { transform: translateY(-2px); background: #ffb361; }

footer {
  background: var(--ink); color: var(--cream);
  padding: 40px 0 36px; margin-top: 30px;
}
footer .wrap { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; align-items: center; }
footer .mark { font-family: 'Fraunces', serif; font-weight: 800; font-size: 18px; }
footer .mark span { color: var(--orange); font-style: italic; font-weight: 600; }
footer small { color: rgba(243,232,207,0.55); font-size: 12px; }

@media (max-width: 720px) {
  .related-grid { grid-template-columns: 1fr; }
  .masthead { padding-top: 40px; }
  .book-strip { padding: 28px 22px; }
}
"""


PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#f3e8cf" />
<title>{title_full} | The Making Of Hosted By Jack Pitts</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="The Making Of Hosted By Jack Pitts" />
<meta property="og:title" content="{title_full}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{share_card_url}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title_full}" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:image" content="{share_card_url}" />
<link rel="icon" type="image/svg+xml" href='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%23f3e8cf"/><text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-weight="900" font-size="42" fill="%23d87a2c">M</text></svg>' />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<script type="application/ld+json">{json_ld}</script>
<style>{css}</style>
</head>
<body>

<nav class="topnav">
  <div class="wrap">
    <a class="mark" href="../index.html">The Making <span>Of</span> Hosted By Jack Pitts</a>
    <a class="back" href="../index.html#episodes">All episodes</a>
  </div>
</nav>

<main class="wrap">
  <div class="masthead">
    <span class="issue">ISSUE {issue}</span>
    <span class="dot"></span>
    <span>{date_label}</span>
    <span class="dot"></span>
    <span>{duration}</span>
    <span class="dot"></span>
    <span>HOSTED BY JACK PITTS</span>
  </div>

  <h1 class="hero-title">{headline_html}</h1>
  {subhead_block}

  <p class="hero-lede">{lede}</p>

  <div class="player" aria-label="Spotify player">
    {player_html}
  </div>

  <div class="listen-row">
    <a href="{spotify}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0a12 12 0 100 24 12 12 0 000-24zm5.52 17.3a.75.75 0 01-1.03.25c-2.82-1.72-6.37-2.11-10.55-1.16a.75.75 0 01-.33-1.46c4.58-1.04 8.51-.6 11.66 1.34.35.21.46.68.25 1.03zm1.47-3.27a.94.94 0 01-1.29.31c-3.23-1.98-8.15-2.55-11.97-1.4a.94.94 0 11-.55-1.8c4.36-1.31 9.79-.67 13.5 1.6.44.27.58.85.31 1.29zm.13-3.4C15.25 8.4 8.8 8.18 5.1 9.3a1.12 1.12 0 11-.66-2.16c4.25-1.29 11.37-1.04 15.85 1.62a1.12 1.12 0 11-1.17 1.91z"/></svg>
      Listen on Spotify
    </a>
    <a href="{apple}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a4 4 0 00-4 4v6a4 4 0 008 0V5a4 4 0 00-4-4zm6 10a1 1 0 00-2 0 4 4 0 01-8 0 1 1 0 00-2 0 6 6 0 005 5.91V20H9a1 1 0 000 2h6a1 1 0 000-2h-2v-3.09A6 6 0 0018 11z"/></svg>
      Apple Podcasts
    </a>
    <a href="{youtube}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3 3 0 00-2.1-2.1C19.6 3.6 12 3.6 12 3.6s-7.6 0-9.4.5A3 3 0 00.5 6.2C0 8 0 12 0 12s0 4 .5 5.8a3 3 0 002.1 2.1c1.8.5 9.4.5 9.4.5s7.6 0 9.4-.5a3 3 0 002.1-2.1C24 16 24 12 24 12s0-4-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>
      YouTube
    </a>
  </div>

  <div class="sec-eyebrow">On this episode</div>
  <div class="sec-rule"></div>
  <div class="body">
    <p>{description_long}</p>
  </div>

  {guest_block}

  <figure class="share-fig">
    <img src="../share-cards/{slug}.png" alt="Cover card for {guest_safe} on The Making Of Hosted By Jack Pitts" />
    <figcaption>The cover card for this issue. Right-click to save and share.</figcaption>
  </figure>

  <section class="related" aria-label="More from the show">
    <h2>More from the show</h2>
    <div class="related-grid">
      {related_cards}
    </div>
  </section>

  <aside class="book-strip" aria-label="Be a guest">
    <div>
      <h3>Have a story like this? <em>Come on the show.</em></h3>
      <p>Sixty to seventy-five minutes, remote, no prep deck. Pick a time and we'll figure out the angle together.</p>
    </div>
    <a href="{book_cal}" target="_blank" rel="noopener">Book a guest call</a>
  </aside>
</main>

<footer>
  <div class="wrap">
    <div class="mark">The Making <span>Of</span> Hosted By Jack Pitts</div>
    <small>&copy; 2026 Jack Pitts. Every conversation is a long one. Have a story? <a href="{book_cal}" target="_blank" rel="noopener" style="color: var(--orange); text-decoration: underline;">Come on the show.</a></small>
  </div>
</footer>

</body>
</html>
"""


def build_player(ep):
    embed = spotify_embed_src((ep.get("links") or {}).get("spotify") or SHOW_SPOTIFY)
    if not embed:
        return ""
    return (
        f'<iframe title="Play this episode on Spotify" src="{embed}" '
        f'height="232" frameBorder="0" allowfullscreen="" '
        f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" '
        f'loading="lazy"></iframe>'
    )


def build_guest_block(ep):
    name = ep.get("guest", "").strip()
    li = (ep.get("guestLinkedIn") or "").strip()
    if not name:
        return ""
    cta = ""
    if li:
        cta = (
            f'<a class="gc-cta" href="{escape(li)}" target="_blank" rel="noopener">'
            '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM0 8h5v16H0V8zm7.5 0H12v2.2h.07c.63-1.18 2.17-2.43 4.47-2.43C21.4 7.77 24 10.1 24 14.73V24h-5v-8.2c0-1.96-.04-4.48-2.73-4.48-2.74 0-3.16 2.13-3.16 4.34V24h-5V8z"/></svg>'
            f'Connect with {escape(name)} on LinkedIn'
            "</a>"
        )
    else:
        cta = ""
    pitch = f"This episode's guest. {escape(name)} sat down with Jack to walk through the path, the false starts, and what actually compounded."
    return (
        '<div class="guest-card">'
        '<div class="gc-eyebrow">About the guest</div>'
        f'<h3>{escape(name)}</h3>'
        f'<p>{pitch}</p>'
        f'{cta}'
        '</div>'
    )


def build_related_cards(all_eps, current_idx, total):
    out = []
    pool = []
    # Show 3 nearest by index, skipping current.
    for offset in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
        i = current_idx + offset
        if 0 <= i < len(all_eps) and i != current_idx:
            pool.append((i, all_eps[i]))
        if len(pool) >= 3:
            break
    for i, ep in pool:
        ep_issue = total - i
        slug = slugify(ep.get("guest", "") or ep.get("title", ""))
        title = escape(ep.get("title", "") or "")
        dur = escape(ep.get("duration", "") or "")
        out.append(
            f'<a class="r-card" href="{slug}.html">'
            f'<div class="r-issue">ISSUE {issue_label(ep_issue)}</div>'
            f'<div class="r-title">{title}</div>'
            f'<div class="r-dur">{dur}</div>'
            '</a>'
        )
    return "\n".join(out) or '<p style="color: var(--ink-soft);">More episodes coming soon.</p>'


def json_ld_for(ep, issue_no, slug):
    canonical = f"{SITE_URL}/episodes/{slug}.html"
    description = (ep.get("description") or "")[:500]
    obj = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "name": ep.get("title", ""),
        "description": description,
        "url": canonical,
        "datePublished": ep.get("date", ""),
        "image": f"{SITE_URL}/share-cards/{slug}.png",
        "associatedMedia": [
            {"@type": "AudioObject", "contentUrl": (ep.get("links") or {}).get("spotify", SHOW_SPOTIFY)}
        ],
        "partOfSeries": {
            "@type": "PodcastSeries",
            "name": SITE,
            "url": SITE_URL,
        },
        "author": {"@type": "Person", "name": "Jack Pitts", "url": JACK_LI},
    }
    return json.dumps(obj)


def long_description_for(ep):
    """Use the existing short description as a confident standfirst.
    Pages stay clean even when only one sentence is on file."""
    desc = (ep.get("description") or "").strip()
    if not desc:
        return "A conversation about what it actually takes to build something real."
    return desc


def render_page(idx, ep, all_eps, total):
    slug = slugify(ep.get("guest", "") or ep.get("title", ""))
    issue_no = total - idx
    title = ep.get("title", "")
    head, sub = split_title(title)
    guest = ep.get("guest", "")
    headline_html = escape(head)
    # If it's a "The Making Of NAME" pattern, italicize the name for visual rhythm
    if guest and guest in head:
        headline_html = escape(head).replace(escape(guest), f"<em>{escape(guest)}</em>")
    subhead_block = f'<p class="hero-sub">{escape(sub)}</p>' if sub else ""

    lede = ep.get("description", "") or ""
    # Lede is the short standfirst from episodes.js
    lede = escape(lede)

    description_long = escape(long_description_for(ep))

    links = ep.get("links") or {}
    canonical = f"{SITE_URL}/episodes/{slug}.html"

    page = PAGE_TMPL.format(
        title_full=escape(title),
        meta_desc=escape(ep.get("description", "")[:200]),
        canonical=canonical,
        share_card_url=f"{SITE_URL}/share-cards/{slug}.png",
        json_ld=json_ld_for(ep, issue_no, slug),
        css=CSS,
        issue=issue_label(issue_no),
        date_label=escape(ep.get("dateLabel", "")),
        duration=escape(ep.get("duration", "")),
        headline_html=headline_html,
        subhead_block=subhead_block,
        lede=lede,
        player_html=build_player(ep),
        spotify=links.get("spotify", SHOW_SPOTIFY),
        apple=links.get("apple", SHOW_APPLE),
        youtube=links.get("youtube", SHOW_YT),
        description_long=description_long,
        guest_block=build_guest_block(ep),
        slug=slug,
        guest_safe=escape(guest or title),
        related_cards=build_related_cards(all_eps, idx, total),
        book_cal=BOOK_CAL,
    )

    out = OUT_DIR / f"{slug}.html"
    out.write_text(page, encoding="utf-8")
    return out


def main():
    eps = load_episodes()
    total = len(eps)
    print(f"Generating {total} episode pages...")
    for idx, ep in enumerate(eps):
        path = render_page(idx, ep, eps, total)
        print(f"  wrote {path.name}")
    print("Done.")


if __name__ == "__main__":
    main()
