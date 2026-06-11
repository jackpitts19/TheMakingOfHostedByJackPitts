# Wire up autonomous deploy to Cloudflare Pages

One-time setup. After this, the scheduled task pushes new episodes to live automatically.

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

## Step 4. Save the secrets locally

In this folder there's already a file called `.env.example`. Make a copy named `.env` and fill in real values:

```
CLOUDFLARE_API_TOKEN=your_actual_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_PAGES_PROJECT=themakingofhostedbyjackpitts
```

`.env` is in `.gitignore` and never gets uploaded to Cloudflare. It only lives on your machine.

## Step 5. Test the deploy once, manually

From a terminal in this folder:

```bash
bash deploy.sh
```

You'll see Wrangler upload files, then "Deploy complete." Visit the site. The redesign with per-episode pages should be live.

If you see an authentication error, the token's missing a permission. Recreate the token with `Cloudflare Pages: Edit` for your account.

## Step 6. You're done

The scheduled task `update-tmo-episodes` already runs `bash deploy.sh` at the end of its workflow. So the next time an episode drops:

1. 8am, the task wakes up, sees the new episode on Spotify.
2. It updates `episodes.js`, bumps the masthead, regenerates the share card, regenerates the episode page.
3. It runs `deploy.sh`, which pushes everything to Cloudflare Pages.
4. The site is live within a minute or two.
5. You get a notification telling you what shipped.

No manual steps. Forever.
