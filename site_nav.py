#!/usr/bin/env python3
"""
The site's primary navigation, in one place.

Every page carries the same five links: Episodes, Press, Be a Guest, About,
Listen. The homepage and the three section pages (/about, /press,
/be-a-guest) style them with site.css; every other page (episode pages, the
archive, articles, legal pages, 404) uses the compact `.topnav` bar defined
here. Generators import `topnav_html()` and `TOPNAV_CSS`, and the tests check
every page against `NAV_ITEMS`, so the links cannot drift apart.
"""

from __future__ import annotations

# Where every guest call to action points (same tab). Guest requests now go by
# email from that page; there is no form.
GUEST_PAGE = "/be-a-guest"

NAV_ITEMS: tuple[tuple[str, str], ...] = (
    ("/episodes", "Episodes"),
    ("/press", "Press"),
    (GUEST_PAGE, "Be a Guest"),
    ("/about", "About"),
    ("/#listen", "Listen"),
)


def nav_links_html(current: str = "", indent: str = "      ") -> str:
    """The five links, marking `current` (a path) with aria-current."""
    lines = []
    for href, label in NAV_ITEMS:
        mark = ' aria-current="page"' if href == current else ""
        lines.append(f'{indent}<a href="{href}"{mark}>{label}</a>')
    return "\n".join(lines)


def topnav_html(current: str = "") -> str:
    """The compact sticky bar used on every page outside site.css."""
    return (
        '<nav class="topnav" aria-label="Primary">\n'
        '  <div class="wrap">\n'
        '    <a class="mark" href="/">The Making <span>Of</span> Hosted By Jack Pitts</a>\n'
        '    <div class="topnav-links">\n'
        f"{nav_links_html(current)}\n"
        "    </div>\n"
        "  </div>\n"
        "</nav>"
    )


# Appended to each .topnav page's own stylesheet. On phones the links drop to a
# single scrollable row under the name (the homepage's mobile pattern), so the
# sticky bar stays two short lines instead of growing.
TOPNAV_CSS = r"""
/* Primary links (site_nav.py) */
.topnav-links { display: flex; gap: 20px; font-size: 13px; font-weight: 600; letter-spacing: 0.02em; }
.topnav-links a {
  color: var(--ink-soft); text-decoration: none; white-space: nowrap;
  display: inline-flex; align-items: center; min-height: 36px;
}
.topnav-links a:hover { color: var(--orange-dark); }
.topnav-links a[aria-current="page"] {
  color: var(--ink); text-decoration: underline; text-decoration-color: var(--orange);
  text-decoration-thickness: 2px; text-underline-offset: 5px;
}
@media (max-width: 760px) {
  .topnav { padding: 10px 0 0; }
  .topnav .wrap { flex-wrap: wrap; row-gap: 0; }
  .topnav .mark { flex-basis: 100%; font-size: clamp(14px, 4vw, 16px); line-height: 1.2; }
  .topnav-links {
    width: 100%; gap: 18px; font-size: 12.5px;
    overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none;
    -webkit-mask-image: linear-gradient(90deg, #000 85%, transparent);
    mask-image: linear-gradient(90deg, #000 85%, transparent);
    padding-right: 24px;
  }
  .topnav-links::-webkit-scrollbar { display: none; }
  .topnav-links a { min-height: 40px; }
}
"""



# ---------------------------------------------------------------------------
# Footer: the same minimal block on every page (wordmark, platform icons, one
# quiet row of links, copyright). The archive at /episodes links every
# episode, so the footer does not list them. Static pages carry a copy of
# footer_html(); the tests check every page against it.

JACK_SITE = "https://thejackpitts.com/"

FOOTER_LINKS: tuple[tuple[str, str], ...] = (
    ("/episodes", "Episodes"),
    ("/about", "About"),
    ("/press", "Press"),
    (GUEST_PAGE, "Be a Guest"),
    ("/privacy", "Privacy"),
    ("/terms", "Terms"),
)

_FOOTER_SOCIALS = r"""    <div class="socials">
      <a href="https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH" target="_blank" rel="noopener" aria-label="Spotify">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0a12 12 0 100 24 12 12 0 000-24zm5.52 17.3a.75.75 0 01-1.03.25c-2.82-1.72-6.37-2.11-10.55-1.16a.75.75 0 01-.33-1.46c4.58-1.04 8.51-.6 11.66 1.34.35.21.46.68.25 1.03zm1.47-3.27a.94.94 0 01-1.29.31c-3.23-1.98-8.15-2.55-11.97-1.4a.94.94 0 11-.55-1.8c4.36-1.31 9.79-.67 13.5 1.6.44.27.58.85.31 1.29zm.13-3.4C15.25 8.4 8.8 8.18 5.1 9.3a1.12 1.12 0 11-.66-2.16c4.25-1.29 11.37-1.04 15.85 1.62a1.12 1.12 0 11-1.17 1.91z"/></svg>
      </a>
      <a href="https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144" target="_blank" rel="noopener" aria-label="Apple Podcasts">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a4 4 0 00-4 4v6a4 4 0 008 0V5a4 4 0 00-4-4zm6 10a1 1 0 00-2 0 4 4 0 01-8 0 1 1 0 00-2 0 6 6 0 005 5.91V20H9a1 1 0 000 2h6a1 1 0 000-2h-2v-3.09A6 6 0 0018 11z"/></svg>
      </a>
      <a href="https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg" target="_blank" rel="noopener" aria-label="YouTube">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3 3 0 00-2.1-2.1C19.6 3.6 12 3.6 12 3.6s-7.6 0-9.4.5A3 3 0 00.5 6.2C0 8 0 12 0 12s0 4 .5 5.8a3 3 0 002.1 2.1c1.8.5 9.4.5 9.4.5s7.6 0 9.4-.5a3 3 0 002.1-2.1C24 16 24 12 24 12s0-4-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>
      </a>
      <a href="https://www.linkedin.com/in/jack-pitts" target="_blank" rel="noopener" aria-label="LinkedIn">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM0 8h5v16H0V8zm7.5 0H12v2.2h.07c.63-1.18 2.17-2.43 4.47-2.43C21.4 7.77 24 10.1 24 14.73V24h-5v-8.2c0-1.96-.04-4.48-2.73-4.48-2.74 0-3.16 2.13-3.16 4.34V24h-5V8z"/></svg>
      </a>
    </div>"""


def footer_html() -> str:
    """The site footer, identical on every page."""
    links = "\n".join(f'      <a href="{href}">{label}</a>' for href, label in FOOTER_LINKS)
    return (
        "<footer>\n"
        '  <div class="wrap">\n'
        '    <div class="mark">The Making <span>Of</span> Hosted By Jack Pitts</div>\n'
        f"{_FOOTER_SOCIALS}\n"
        '    <nav class="footer-links" aria-label="Footer">\n'
        f"{links}\n"
        "    </nav>\n"
        f'    <small>&copy; 2026 The Making Of Hosted By <a href="{JACK_SITE}" target="_blank" rel="noopener">Jack Pitts</a></small>\n'
        "  </div>\n"
        "</footer>"
    )


# Footer rules for pages outside site.css (site.css carries the same rules).
FOOTER_CSS = r"""
/* Footer (site_nav.py) */
footer .socials { display: flex; gap: 16px; }
footer .socials a {
  color: var(--cream); width: 38px; height: 38px; border-radius: 50%;
  background: rgba(255,255,255,0.08);
  display: grid; place-items: center;
  transition: background .15s ease, color .15s ease;
}
footer .socials a:hover { background: var(--orange); color: var(--ink); }
footer .socials svg { width: 16px; height: 16px; }
footer .footer-links { flex-basis: 100%; display: flex; flex-wrap: wrap; justify-content: flex-start; gap: 8px 24px; padding: 6px 0 0; }
footer .footer-links a {
  color: rgba(243,232,207,0.75); font-size: 13px; font-weight: 500;
  letter-spacing: 0.02em; text-decoration: none;
}
footer .footer-links a:hover { color: var(--orange); }
footer small a { color: inherit; text-decoration: underline; text-underline-offset: 3px; }
footer small a:hover { color: var(--orange); }
"""


# Shared header and footer look for every page outside site.css. Appended
# last, so it wins over each page's own older .topnav and footer rules and
# the header matches the homepage, /about, /press and /be-a-guest exactly:
# same 1120px container, upright orange "Of", same link size and weight, no
# rule under the bar. Font families are left to each page.
CHROME_CSS = r"""
/* Shared header and footer (site_nav.py CHROME_CSS) */
.topnav {
  position: static; border-bottom: 0; background: transparent;
  -webkit-backdrop-filter: none; backdrop-filter: none; padding: 28px 0 10px;
}
.topnav .wrap, footer .wrap { max-width: 1120px; padding: 0 28px; }
.topnav .mark { font-size: 18px; letter-spacing: 0.02em; color: var(--ink); }
.topnav .mark span { color: var(--orange); font-style: normal; font-weight: 700; margin-right: 0; }
.topnav-links { gap: 28px; font-size: 14px; font-weight: 500; letter-spacing: 0; }
.topnav-links a[aria-current="page"] { font-weight: 700; text-underline-offset: 6px; }
footer { padding: 50px 0 40px; margin-top: 60px; }
footer .mark { font-size: 20px; }
footer .mark span { font-style: normal; font-weight: 700; }
@media (max-width: 860px) {
  .topnav { padding: 20px 0 0; }
  .topnav .wrap { flex-wrap: wrap; row-gap: 2px; }
  .topnav .mark { flex-basis: 100%; font-size: 15px; }
  .topnav-links {
    width: 100%; gap: 20px; font-size: 13px;
    overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none;
    -webkit-mask-image: linear-gradient(90deg, #000 85%, transparent);
    mask-image: linear-gradient(90deg, #000 85%, transparent);
    padding-right: 24px;
  }
  .topnav-links a { min-height: 44px; }
  footer .mark { font-size: 16px; }
}
@media (max-width: 600px) {
  .topnav .wrap, footer .wrap { padding: 0 16px; }
}
/* Phones: all five links fit, so no clipped last item and no fade. */
@media (max-width: 440px) {
  .topnav-links {
    gap: 14px; font-size: 12.5px; padding-right: 0;
    -webkit-mask-image: none; mask-image: none;
  }
}
"""
