# Cloudflare setup

## Current setup (Oct 2026)

- **Production is the Cloudflare Worker `frosty-pond-4366`**, deployed by Cloudflare's Git integration on every push to `main`. It serves the static site (the repo root, minus whatever `.assetsignore` lists). There is no Worker script. Config lives in `wrangler.toml`.
- There is no GitHub Actions deploy workflow. `.github/workflows/episode-sync.yml` only syncs episodes and commits; the push is what triggers the deploy.
- `deploy.sh` is a manual fallback (`npx --yes wrangler@4 deploy`). You rarely need it.
- The old **Pages** instructions further down ("Wire up autonomous deploy to Cloudflare Pages") are **outdated** and kept only for reference. The Pages project `themakingofhostedbyjackpitts` (pages.dev) is a stale copy and is not the live site.
- `_headers` adds basic security headers to every page. `.assetsignore` keeps source files (`*.py`, `tests/`, config) from being publicly served.

## Guest requests

Guest requests go by email. The `/be-a-guest` page has an "Email me about being a guest" button that opens a prefilled draft to jack@saltcreekadvisory.com, shows the address as plain text, and offers LinkedIn as an alternative. Nothing on Cloudflare needs to be configured for it: no Worker, Email Routing, secrets, or rate limits.

If an old `GUEST_REQUEST_TO` secret or Email Routing setup exists from the retired form, it can be removed from the dashboard; nothing uses it anymore.

---

## Outdated: Wire up autonomous deploy to Cloudflare Pages

> Outdated (kept for reference). Production no longer uses Pages; see "Current setup" above.

One-time setup. After this, GitHub Actions deploys every push (including recurring episode-sync commits) automatically.

## What you need before you start

You're already on Cloudflare. You need:

- A Cloudflare Pages project pointed at `themakingofhostedbyjackpitts.com`. If you have one, perfect. If not, see Step 1.
- About 4 minutes.

## Step 1. Make sure a Pages project exists

Log in to Cloudflare → **Workers & Pages** → **Pages tab** → look for a project serving `themakingofhostedbyjackpitts.com`.

If there is one, note its name. Most likely `themakingofhostedbyjackpitts`.

If there isn't, click **Create application** → **Pages** → **Upload assets**. Name it `themakingofhostedbyjackpitts`. Drop the whole folder in for the first deployment. Then point the custom domain at the project.

## Step 2. Create an API token

This token lets the scheduled task push deployments without you in the loop.

1. Cloudflare dashboard → top-right profile menu → **My Profile** → **API Tokens**.
2. Click **Create Token**.
3. Use the template **"Edit Cloudflare Workers"** (it covers Pages too), OR pick **"Create Custom Token"** with these permissions:
   - Account → Cloudflare Pages → **Edit**
4. Limit to your specific account.
5. Click Continue → Create. Copy the token immediately. Cloudflare won't show it again.

## Step 3. Grab your Account ID

Workers & Pages → click your `themakingofhostedbyjackpitts` project → look at the right sidebar. **Account ID** is there. Copy it.

## Step 4. Save the secrets in GitHub

In your GitHub repo, go to **Settings → Secrets and variables → Actions → New repository secret** and add:

- `CLOUDFLARE_API_TOKEN` = your token
- `CLOUDFLARE_ACCOUNT_ID` = your account ID
- `CLOUDFLARE_PAGES_PROJECT` = `themakingofhostedbyjackpitts` (optional but recommended)

## Step 5. Verify Actions workflows are enabled

The repo includes two workflows:

- `.github/workflows/episode-sync.yml` (weekly sync + regeneration + commit)
- `.github/workflows/deploy-cloudflare.yml` (deploy to Cloudflare on every push to `main`)

Open **Actions** in GitHub and run `Deploy Cloudflare Pages` manually once to verify setup.

## Step 6. You're done

From now on:

1. Weekly sync checks for a new episode.
2. If new, it updates `episodes.js` and regenerates assets.
3. It commits to `main`.
4. Push to `main` auto-deploys to Cloudflare Pages and Vercel.

No manual deploy loop required.
