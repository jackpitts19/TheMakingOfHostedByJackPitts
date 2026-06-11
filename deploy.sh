#!/usr/bin/env bash
# Deploys the site to Cloudflare Pages using Wrangler's direct upload.
# Reads CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID from a .env file
# next to this script. Run after generate_share_cards.py and
# generate_episode_pages.py.

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
  echo "  CLOUDFLARE_PAGES_PROJECT=themakingofhostedbyjackpitts   # optional"
  exit 1
fi

PROJECT="${CLOUDFLARE_PAGES_PROJECT:-themakingofhostedbyjackpitts}"

# Stage a clean copy that excludes source files and local junk.
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# Files and folders that ship to production.
rsync -a \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.*' \
  --exclude='__pycache__' \
  --exclude='*.py' \
  --exclude='*.sh' \
  --exclude='.gitignore' \
  --exclude='README.md' \
  --exclude='SETUP-CLOUDFLARE.md' \
  --exclude='tmo-podcast.skill' \
  --exclude='episodes.json' \
  --exclude='*.log' \
  --exclude='*.tmp' \
  ./ "$STAGE/"

echo "Deploying $(find "$STAGE" -type f | wc -l) files to Cloudflare Pages project: $PROJECT"

CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CLOUDFLARE_ACCOUNT_ID" \
  npx --yes wrangler@latest pages deploy "$STAGE" \
    --project-name="$PROJECT" \
    --commit-message="Autonomous episode update $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --branch="main"

echo "Deploy complete."
