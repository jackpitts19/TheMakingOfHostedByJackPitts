"""
Stylesheet and HTML template for the per-episode pages.

Split out of generate_episode_pages.py to keep that module focused on data and
markup builders. CSS is also reused by generate_episode_archive.py (imported
through generate_episode_pages, which re-exports it). Pure constants: changing
anything here changes every generated episode page on the next run.
"""

from site_nav import CHROME_CSS, FOOTER_CSS, TOPNAV_CSS, footer_html

CSS = r"""
:root {
  --cream: #f3e8cf;
  --cream-deep: #ecd9a8;
  --orange: #d87a2c;
  --orange-dark: #934c13;
  --ink: #14130f;
  --ink-soft: #3a352b;
  --line: rgba(20,19,15,0.12);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--cream); color: var(--ink); }
body { font-family: "Libre Franklin", "Helvetica Neue", Arial, sans-serif; line-height: 1.55; }
a { color: inherit; }
img { max-width: 100%; display: block; }

/* Keyboard focus: ink ring on cream, orange ring on the dark panels (>= 3:1). */
a:focus-visible, button:focus-visible {
  outline: 3px solid var(--ink); outline-offset: 3px; border-radius: 4px;
}
.book-strip a:focus-visible, .book-strip button:focus-visible,
footer a:focus-visible { outline-color: var(--orange); }
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.nb { white-space: nowrap; }

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
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700; font-size: 18px;
  letter-spacing: -0.01em; color: var(--ink); text-decoration: none;
}
.topnav .mark span { color: var(--orange); font-style: italic; font-weight: 600; margin-right: 0.12em; }

/* Masthead meta line under nav */
.masthead {
  padding: 56px 0 18px;
  display: flex; flex-wrap: wrap; gap: 14px;
  font-family: "Libre Franklin", "Helvetica Neue", Arial, sans-serif;
  font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-soft); font-weight: 600;
}
.masthead .issue { color: var(--orange-dark); font-weight: 700; }
.masthead .dot { width: 4px; height: 4px; background: var(--ink-soft); border-radius: 50%; opacity: 0.6; align-self: center; }

/* Hero headline */
.hero-title {
  font-family: "Newsreader", Georgia, "Times New Roman", serif;
  font-weight: 700; line-height: 1.08;
  font-size: clamp(34px, 6.4vw, 76px);
  letter-spacing: -0.01em;
  margin: 0 0 18px;
  color: var(--ink);
  overflow-wrap: break-word;
  hyphens: manual;
}
.hero-title em { font-style: italic; color: var(--orange-dark); font-weight: 700; }
.hero-sub {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 500;
  font-size: clamp(19px, 2.4vw, 30px);
  line-height: 1.28; color: var(--ink-soft);
  overflow-wrap: break-word;
  letter-spacing: -0.005em;
  margin: 0 0 36px;
  max-width: 660px;
}
/* Episode player (Apple or Spotify embed) */
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

/* Share this episode: same pills, quieter, under the listen row */
.share-row { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: -26px 0 44px; }
.share-row .share-label {
  font-size: 11.5px; letter-spacing: 0.12em; text-transform: uppercase;
  font-weight: 700; color: var(--ink-soft); margin-right: 4px;
}
.share-row a, .share-row button {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 44px; min-width: 44px;
  padding: 7px 13px; border-radius: 999px;
  border: 1px solid var(--line); background: transparent;
  color: var(--ink-soft); text-decoration: none; cursor: pointer;
  font: 600 12.5px/1.2 "Libre Franklin", "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.02em;
  transition: background .15s, color .15s, border-color .15s;
}
.share-row a:hover, .share-row button:hover { background: var(--ink); color: var(--cream); border-color: var(--ink); }
.share-row .share-status { font-size: 12.5px; color: var(--orange-dark); font-weight: 600; }

/* Section heading */
.sec-eyebrow {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-style: italic; font-weight: 600;
  font-size: 18px; color: var(--orange-dark); margin: 56px 0 12px;
}
.sec-rule { height: 1px; background: var(--line); margin: 0 0 28px; }

/* Long body copy */
.body p {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 400;
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
  font-family: "Libre Franklin", "Helvetica Neue", Arial, sans-serif; font-size: 11.5px;
  letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-soft); font-weight: 700;
  margin-bottom: 10px;
}
.guest-card h2 {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700;
  font-size: 30px; letter-spacing: -0.01em;
  margin: 0 0 8px; color: var(--ink);
}
.guest-card p {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-size: 17px;
  color: var(--ink-soft); margin: 0 0 18px; line-height: 1.5;
}
.guest-card .gc-cta {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--ink);
  border: 1.5px solid var(--ink-soft);
  padding: 12px 20px; border-radius: 999px;
  text-decoration: none; font-weight: 700; font-size: 14px;
  letter-spacing: 0.01em;
  transition: background .15s ease, color .15s ease, border-color .15s ease, transform .15s ease;
}
.guest-card .gc-cta:hover { background: var(--ink); color: var(--cream); border-color: var(--ink); transform: translateY(-1px); }
.guest-card .gc-cta svg { width: 16px; height: 16px; }

/* More from the show */
.related {
  border-top: 1px solid var(--line);
  margin-top: 70px;
  padding-top: 36px;
}
.related h2 {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700;
  font-size: 30px; letter-spacing: -0.01em;
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
  font-family: "Libre Franklin", "Helvetica Neue", Arial, sans-serif; font-size: 11px;
  letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700;
  color: var(--orange-dark); margin-bottom: 8px;
}
.r-card .r-title {
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700;
  font-size: 18px; line-height: 1.25; color: var(--ink);
  margin: 0 0 10px; letter-spacing: -0.01em;
}
.r-card .r-dur {
  font-size: 12px; color: var(--ink-soft);
  font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
}

/* Related reading: links out to the guides */
.read-list { display: flex; flex-direction: column; gap: 2px; }
.read-list a {
  display: block; text-decoration: none; color: var(--ink);
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 600; font-size: 18px;
  line-height: 1.35; letter-spacing: -0.01em;
  padding: 15px 0; border-bottom: 1px solid var(--line);
  transition: color .15s, padding-left .15s;
}
.read-list a:first-child { border-top: 1px solid var(--line); }
.read-list a:hover { color: var(--orange-dark); padding-left: 8px; }
.read-list a .read-arrow { color: var(--orange-dark); }

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
  font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700;
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
footer .mark { font-family: "Newsreader", Georgia, "Times New Roman", serif; font-weight: 700; font-size: 18px; }
footer .mark span { color: var(--orange); font-style: italic; font-weight: 600; }
footer small { color: rgba(243,232,207,0.55); font-size: 12px; }
/* Bigger tap area without changing the line: padding offset by negative margin. */
footer .foot-link { display: inline-block; padding: 14px 6px; margin: -14px 0; }

@media (max-width: 720px) {
  .related-grid { grid-template-columns: 1fr; }
  .masthead { padding-top: 40px; }
  .book-strip { padding: 28px 22px; }
  .topnav { padding: 12px 0; }
  .topnav .mark { font-size: clamp(13px, 3.9vw, 15px); line-height: 1.2; min-width: 0; }
  /* Balanced lines only on phones, so the desktop headline is unchanged. */
  .hero-title { line-height: 1.06; text-wrap: balance; }
  .hero-sub { text-wrap: balance; }
}
@media (max-width: 480px) {
  .wrap { padding: 0 16px; }
}
"""
CSS += TOPNAV_CSS
CSS += FOOTER_CSS
CSS += CHROME_CSS


PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#f3e8cf" />
<title>{page_title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="The Making Of Hosted By Jack Pitts" />
<meta property="og:title" content="{social_title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{share_card_url}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{social_title}" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:image" content="{share_card_url}" />
<link rel="icon" type="image/svg+xml" href='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%23f3e8cf"/><text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-weight="900" font-size="42" fill="%23d87a2c">M</text></svg>' />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400..700&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap" rel="stylesheet" />
<script type="application/ld+json">{json_ld}</script>
<style>{css}</style>
</head>
<body>

{topnav}

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

  <div class="player" role="group" aria-label="{player_label}">
    {player_html}
  </div>

  <div class="listen-row">
    <a href="{spotify}" target="_blank" rel="noopener" aria-label="Listen on Spotify: {guest_label}">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0a12 12 0 100 24 12 12 0 000-24zm5.52 17.3a.75.75 0 01-1.03.25c-2.82-1.72-6.37-2.11-10.55-1.16a.75.75 0 01-.33-1.46c4.58-1.04 8.51-.6 11.66 1.34.35.21.46.68.25 1.03zm1.47-3.27a.94.94 0 01-1.29.31c-3.23-1.98-8.15-2.55-11.97-1.4a.94.94 0 11-.55-1.8c4.36-1.31 9.79-.67 13.5 1.6.44.27.58.85.31 1.29zm.13-3.4C15.25 8.4 8.8 8.18 5.1 9.3a1.12 1.12 0 11-.66-2.16c4.25-1.29 11.37-1.04 15.85 1.62a1.12 1.12 0 11-1.17 1.91z"/></svg>
      Listen on Spotify
    </a>
    <a href="{apple}" target="_blank" rel="noopener" aria-label="Apple Podcasts: {guest_label}">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a4 4 0 00-4 4v6a4 4 0 008 0V5a4 4 0 00-4-4zm6 10a1 1 0 00-2 0 4 4 0 01-8 0 1 1 0 00-2 0 6 6 0 005 5.91V20H9a1 1 0 000 2h6a1 1 0 000-2h-2v-3.09A6 6 0 0018 11z"/></svg>
      Apple Podcasts
    </a>
    <a href="{youtube}" target="_blank" rel="noopener" aria-label="YouTube: {guest_label}">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3 3 0 00-2.1-2.1C19.6 3.6 12 3.6 12 3.6s-7.6 0-9.4.5A3 3 0 00.5 6.2C0 8 0 12 0 12s0 4 .5 5.8a3 3 0 002.1 2.1c1.8.5 9.4.5 9.4.5s7.6 0 9.4-.5a3 3 0 002.1-2.1C24 16 24 12 24 12s0-4-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>
      YouTube
    </a>
  </div>

  {share_row}

  <div class="sec-eyebrow">On this episode</div>
  <div class="sec-rule"></div>
  <div class="body">
    <p>{description_long}</p>
  </div>

  {guest_block}

  <section class="related" aria-label="More from the show">
    <h2>More from the show</h2>
    <div class="related-grid">
      {related_cards}
    </div>
  </section>

  <section class="related" aria-label="Related reading">
    <h2>Related reading</h2>
    <div class="read-list">
      {related_reading}
    </div>
  </section>

  <aside class="book-strip" aria-label="Be a guest">
    <div>
      <h3>Be a guest on <em>the show</em>.</h3>
      <p>About an hour, recorded remotely on Riverside. No prep needed. Email me if you're interested.</p>
    </div>
    <a href="{guest_request}">Be a Guest</a>
  </aside>
</main>

<!--SITE_FOOTER-->

{share_script}
</body>
</html>
"""

# The shared footer has no braces, so it is safe to splice into the format string.
PAGE_TMPL = PAGE_TMPL.replace("<!--SITE_FOOTER-->", footer_html())
