#!/usr/bin/env bash
# Manual deploy of the Worker "frosty-pond-4366" (static assets + the
# /api/guest-request script) using wrangler.toml in this folder.
#
# Production normally deploys through Cloudflare's Git integration on every
# push to main, so you rarely need this. Use it for a hotfix or to test a
# deploy from your machine. Run after generate_share_cards.py and
# generate_episode_pages.py.
#
# Reads CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID from a .env file next
# to this script. Files that must not be public are excluded by .assetsignore
# (the old rsync staging step was removed because `wrangler deploy` reads the
# assets directory from wrangler.toml, not from a staging folder).

set -e
cd "$(dirname "$0")"

# Load secrets from .env (one KEY=VALUE per line)
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [ -z "${CLOUDFLARE_API_TOKEN:-}" ] || [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  echo "ERROR: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set."
  echo "Create a .env file next to this script with:"
  echo "  CLOUDFLARE_API_TOKEN=your_token_here"
  echo "  CLOUDFLARE_ACCOUNT_ID=your_account_id_here"
  exit 1
fi

echo "Deploying Worker frosty-pond-4366 (see wrangler.toml)"

CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CLOUDFLARE_ACCOUNT_ID" \
  npx --yes wrangler@4 deploy \
    --message="Manual deploy $(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "Deploy complete."
