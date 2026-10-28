# Cloudflare setup

## Current setup (Oct 2026)

- **Production is the Cloudflare Worker `frosty-pond-4366`**, deployed by Cloudflare's Git integration on every push to `main`. It serves the static site (the repo root, minus whatever `.assetsignore` lists) plus one small script for `/api/*`. Config lives in `wrangler.toml`.
- There is no GitHub Actions deploy workflow. `.github/workflows/episode-sync.yml` only syncs episodes and commits; the push is what triggers the deploy.
- `deploy.sh` is a manual fallback (`npx --yes wrangler@4 deploy`). You rarely need it.
- The old **Pages** instructions further down ("Wire up autonomous deploy to Cloudflare Pages") are **outdated** and kept only for reference. The Pages project `themakingofhostedbyjackpitts` (pages.dev) is a stale copy and is not the live site.
- `_headers` adds basic security headers to every page. `.assetsignore` keeps source files (`*.py`, `worker/`, `tests/`, config) from being publicly served.

## Enable guest requests

The "Request to Be a Guest" form on the homepage posts to `/api/guest-request`. The Worker checks it, filters spam, and emails it to you with Reply-To set to the guest. Until steps 1 to 4 are done, the form shows "Guest requests are temporarily unavailable. Please message Jack on LinkedIn."

Do step 1 **before** deploying the `send_email` binding, in case Cloudflare rejects the binding on a domain without Email Routing.

1. **Turn on Email Routing for the podcast domain.** Cloudflare dashboard → `themakingofhostedbyjackpitts.com` → **Email** → **Email Routing** → **Enable**. Accept the MX and SPF records it offers. (The domain has no mail today, so nothing breaks.)
2. **Add and verify the inbox that should receive requests.** Email Routing → **Destination addresses** → add your address → click the link in the verification email. The Worker can only send to verified destination addresses.
3. **Tell the Worker where to send.** From this folder run:
   ```bash
   npx wrangler secret put GUEST_REQUEST_TO
   ```
   and paste the verified address. (Or: Workers & Pages → `frosty-pond-4366` → **Settings** → **Variables and Secrets** → add `GUEST_REQUEST_TO` as a Secret.) It is a secret so your address never appears in this public repo.
4. **Deploy.** Push to `main` (Git integration deploys it), or run `./deploy.sh`.
5. **Verify.**
   - `curl -i https://themakingofhostedbyjackpitts.com/api/guest-request` should return **405**.
   - A cross-origin POST should return **403**:
     ```bash
     curl -i -X POST https://themakingofhostedbyjackpitts.com/api/guest-request \
       -H "Origin: https://example.com" -H "Content-Type: application/json" -d '{}'
     ```
   - Submit the real form on the homepage with your own details. Wait at least a few seconds before submitting (fast submits are treated as bots and silently dropped).
   - Check the inbox: the email should arrive from `guest-requests@themakingofhostedbyjackpitts.com`, and hitting Reply should address the guest.
   - Optional: `npx wrangler tail frosty-pond-4366` while testing to watch for errors. The logs never include the guest's story.
6. **Optional backup sender (Resend).** If Cloudflare email ever fails, the Worker can retry through Resend. Create a new Resend API key limited to sending on an already verified domain (do not reuse another app's production key), then:
   ```bash
   npx wrangler secret put RESEND_API_KEY
   npx wrangler secret put RESEND_FROM   # e.g. The Making Of Hosted By Jack Pitts <podcast@your-verified-domain>
   ```
7. **Optional later: Cloudflare Turnstile.** If spam gets through the honeypot, time check, and rate limit (3 per minute per IP), add a free Turnstile widget and verify its token in `worker/guest-request.js`.

Local testing: `npx wrangler@4 dev --var ALLOW_LOCAL_ORIGINS:1` lets the form post from `http://localhost`. Unit tests: `node --test tests/worker/*.test.mjs`.

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
