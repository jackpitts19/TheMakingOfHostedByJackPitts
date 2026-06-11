# The Making Of Hosted By Jack Pitts

The landing page and per-episode archive for the podcast.

Live site: https://themakingofhostedbyjackpitts.com

## What's in here

- `index.html` — the main landing page. Single file, inline CSS, inline render script.
- `episodes.js` — the source of truth for the episode list. Exposes `window.EPISODES`.
- `episodes/` — one polished, magazine-style page per episode.
- `share-cards/` — branded 1200x630 PNG share cards, one per episode, plus a `latest.png` for OG.
- `generate_share_cards.py` — regenerates the share cards from `episodes.js`.
- `generate_episode_pages.py` — regenerates the per-episode HTML pages from `episodes.js`.
- `logo.png`, `headshot.jpg` — show artwork.

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

If you change `episodes.js` by hand and want to refresh everything:

```bash
python3 generate_share_cards.py
python3 generate_episode_pages.py
```

## House style rules (the show)

- The show's full name is "The Making Of Hosted By Jack Pitts". Never abbreviate in copy.
- No em dashes anywhere. Use periods, commas, or "and".
- Palette: cream `#f3e8cf`, orange `#d87a2c`, ink `#14130f`. Fraunces serif + Inter.
