# The Making Of Hosted By Jack Pitts

The landing page and per-episode archive for the podcast.

Live site: https://themakingofhostedbyjackpitts.com

## What's in here

- `index.html`: the homepage (hero, latest episode, catalog picks, recent episodes, listen strip), with an inline render script.
- `about.html`, `press.html`, `be-a-guest.html`: the host bio (`/about`), press coverage and press kit (`/press`), and how to come on the show (`/be-a-guest`). Guest requests go by email from that page; there is no form or server code.
- `site.css`: the shared stylesheet for the homepage and those three pages.
- `site_nav.py`: the primary nav links and the minimal footer every page carries; generators import them, and the tests check every page against them. The footer does not list episodes; `/episodes` links them all.
- `marquee.js`: paints the past-guests band on `/be-a-guest` from `episodes.js`.
- `episodes.js`: the source of truth for the episode list. Exposes `window.EPISODES`.
- `episodes/`: one polished, magazine-style page per episode.
- `episodes.html`: the episode archive served at `/episodes`.
- `articles.html`, `articles/`: the article archive and the articles themselves.
- `share-cards/`: branded 1200x630 PNG link-preview cards: one per episode (that page's `og:image`), `latest.png` (newest episode), and `show.png` (the `og:image` for every page that is not an episode).
- `fonts/`: Newsreader and Libre Franklin as static TTFs, vendored so the share cards render the same on a Mac and in CI. Instanced from the variable fonts in github.com/google/fonts (`ofl/newsreader`, `ofl/librefranklin`) with fontTools' `varLib.instancer` (Newsreader opsz 72 at wght 600 and italic wght 500; Libre Franklin wght 500 and 600). SIL Open Font License; each family's `OFL.txt` sits beside it. Build-only, listed in `.assetsignore`. `fonts/kerning.json` holds each font's pair kerning, exported from its GPOS table by `fonts/bake_kern.py` (needs fontTools; re-run only if the fonts change). The cards need it because Pillow's BASIC layout engine, used so output is identical on every machine, does not kern.
- `sitemap.xml`, `robots.txt`: generated crawl surface. Do not hand-edit `sitemap.xml`.
- `seo_urls.py`: **single source of truth for public URLs.** Every generator imports it.
- `generate_share_cards.py`: regenerates the share cards from `episodes.js`. Type setting (fonts, kerning, ligatures) lives in `card_type.py`.
- `generate_episode_pages.py`: regenerates the per-episode HTML pages from `episodes.js`.
- `generate_episode_archive.py`: regenerates `episodes.html` from `episodes.js`.
- `update_home_fallback.py`: refreshes the homepage's no-JS fallback markup.
- `generate_sitemap.py`: regenerates `sitemap.xml` from `episodes.js` + `articles/`.
- `validate_seo.py`: fails the build on any indexing defect. Run it before pushing.
- `generate_logo_webp.py`: rebuilds `logo.webp` from `logo.png`. Run if the logo changes.
- `logo.png`, `headshot.jpg`: show artwork. **`logo.png` stays full-resolution**
  because the Press Kit offers it as a download; the homepage hero serves
  `logo.webp` (47 KB vs 1749 KB) via `<picture>`, with `logo.png` as fallback.

## URLs: no `.html`, ever

Cloudflare Pages serves these files at extensionless paths and **307-redirects**
the `.html` form (`/articles.html` -> `/articles`). A URL that keeps the suffix is
a redirect, not a page, and Google Search Console logs it as "Page with redirect,
not indexed". So canonical tags, `og:url`, JSON-LD, internal links, and every
sitemap entry use the extensionless form. `validate_seo.py` enforces this.

Build URLs with `seo_urls.py`, never by string-concatenating a slug and `.html`.

## How updates work

A scheduled task (`update-tmo-episodes`, defined in Cowork) runs every morning at 8am. It:

1. Checks Spotify for the newest episode.
2. If it's not already in `episodes.js`, prepends a new entry, bumps the masthead Issue No. on `index.html`.
3. Runs `python3 generate_share_cards.py` to produce a branded card for the new guest.
4. Runs `python3 generate_episode_pages.py` to produce the new episode page and refresh the related-episode strips on every other page.
5. Commits the changes and pushes to this GitHub repo. Cloudflare Pages auto-deploys.
6. Sends a completion notification.

So new episodes appear on the live site the morning after they drop, with no manual work.

## Manual regenerate

If you change `episodes.js` by hand and want to refresh everything, run these in
order (the sitemap validates against the files the earlier steps produce):

```bash
python3 generate_share_cards.py       # needs Pillow: pip install pillow
python3 generate_episode_pages.py
python3 generate_episode_archive.py
python3 update_home_fallback.py
python3 generate_sitemap.py
python3 validate_seo.py               # must print "all checks green"
```

Tests:

```bash
python3 -m unittest discover tests
```

### Adding an article

Drop a new `articles/<slug>.html` in place, then run `python3 generate_sitemap.py`
and `python3 validate_seo.py`. The sitemap discovers articles by globbing the
directory, so there is no URL list to update. CI does this on every push too.

## House style rules (the show)

- The show's full name is "The Making Of Hosted By Jack Pitts". Never abbreviate in copy.
- No em dashes anywhere. Use periods, commas, or "and".
- Palette: cream `#f3e8cf`, orange `#d87a2c`, brown `#8a521f`, ink `#14130f`. Newsreader for headings and reading, Libre Franklin for labels and UI.
