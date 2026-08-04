# The Making Of Hosted By Jack Pitts

The landing page and per-episode archive for the podcast.

Live site: https://themakingofhostedbyjackpitts.com

## What's in here

- `index.html` — the main landing page. Single file, inline CSS, inline render script.
- `episodes.js` — the source of truth for the episode list. Exposes `window.EPISODES`.
- `episodes/` — one polished, magazine-style page per episode.
- `episodes.html` — the episode archive served at `/episodes`.
- `articles.html`, `articles/` — the article archive and the articles themselves.
- `share-cards/` — branded 1200x630 PNG share cards, one per episode, plus a `latest.png` for OG.
- `sitemap.xml`, `robots.txt` — generated crawl surface. Do not hand-edit `sitemap.xml`.
- `seo_urls.py` — **single source of truth for public URLs.** Every generator imports it.
- `generate_share_cards.py` — regenerates the share cards from `episodes.js`.
- `generate_episode_pages.py` — regenerates the per-episode HTML pages from `episodes.js`.
- `generate_episode_archive.py` — regenerates `episodes.html` from `episodes.js`.
- `update_home_fallback.py` — refreshes the homepage's no-JS fallback markup.
- `generate_sitemap.py` — regenerates `sitemap.xml` from `episodes.js` + `articles/`.
- `validate_seo.py` — fails the build on any indexing defect. Run it before pushing.
- `logo.png`, `headshot.jpg` — show artwork.

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

### Adding an article

Drop a new `articles/<slug>.html` in place, then run `python3 generate_sitemap.py`
and `python3 validate_seo.py`. The sitemap discovers articles by globbing the
directory, so there is no URL list to update. CI does this on every push too.

## House style rules (the show)

- The show's full name is "The Making Of Hosted By Jack Pitts". Never abbreviate in copy.
- No em dashes anywhere. Use periods, commas, or "and".
- Palette: cream `#f3e8cf`, orange `#d87a2c`, ink `#14130f`. Fraunces serif + Inter.
