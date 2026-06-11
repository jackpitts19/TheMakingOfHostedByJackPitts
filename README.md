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
- `sync_latest_episode.py` — checks Apple Podcasts for a new episode and prepends it to `episodes.js` when found.
- `logo.png`, `headshot.jpg` — show artwork.

## How updates work

Updates are integrated through GitHub Actions so each new episode can flow through the same pipeline:

1. `.github/workflows/episode-sync.yml` runs at 8:00am Eastern on a 21-day cadence anchored to June 11, 2026 (and on manual dispatch).
2. It checks Apple Podcasts for the newest episode and updates `episodes.js` only when new content exists.
3. It regenerates share cards and episode pages.
4. It commits and pushes to `main`.
5. Vercel auto-deploys from GitHub on push.
6. `.github/workflows/deploy-cloudflare.yml` deploys that same commit to Cloudflare Pages.

This supports recurring updates (every ~3 weeks) without rebuilding the process each time.

## Required GitHub Secrets

For Cloudflare deploys from Actions, configure repo secrets:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PAGES_PROJECT` (optional, defaults to `themakingofhostedbyjackpitts`)

## Manual regenerate

If you change `episodes.js` by hand and want to refresh everything:

```bash
python3 generate_share_cards.py
python3 generate_episode_pages.py
```

To force an immediate sync/deploy, run these workflows manually in GitHub Actions:

- `Episode Sync`
- `Deploy Cloudflare Pages`

## House style rules (the show)

- The show's full name is "The Making Of Hosted By Jack Pitts". Never abbreviate in copy.
- No em dashes anywhere. Use periods, commas, or "and".
- Palette: cream `#f3e8cf`, orange `#d87a2c`, ink `#14130f`. Fraunces serif + Inter.
