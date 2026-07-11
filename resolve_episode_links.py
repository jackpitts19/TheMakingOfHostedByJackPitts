#!/usr/bin/env python3
"""
Resolve per-episode Apple Podcasts links and full descriptions into episodes.js.

Apple's public lookup API (no credentials) returns every episode of the show
with its own trackId, per-episode URL, and full description. This script:
  - sets links.apple to the episode's own Apple URL (was the show-level URL),
  - stores appleEpisodeId so pages can embed that episode's player,
  - upgrades stored descriptions that are shorter than Apple's full text
    (fixes entries that were truncated before syncing stored full summaries).

Safe to run on a schedule: it only writes when something actually changed.
Episodes not found on Apple (title mismatch) are left untouched and reported.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

from sync_latest_episode import APPLE_PODCAST_ID, UA, load_episodes, save_episodes, strip_tags

LOOKUP_URL = (
    "https://itunes.apple.com/lookup?id="
    + APPLE_PODCAST_ID
    + "&entity=podcastEpisode&limit=300"
)


def norm_title(title: str) -> str:
    """Normalize a title for matching: casefold, drop punctuation/quote variants."""
    return re.sub(r"[^a-z0-9]+", " ", str(title or "").casefold()).strip()


def fetch_apple_episodes() -> dict[str, dict]:
    req = urllib.request.Request(LOOKUP_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    items = [r for r in data.get("results", []) if r.get("kind") == "podcast-episode"]
    if not items:
        raise RuntimeError("Apple lookup returned no podcast episodes")
    return {norm_title(it.get("trackName", "")): it for it in items}


def apply_apple_data(ep: dict, apple: dict) -> bool:
    """Fill one episode entry from its Apple lookup item. Returns True if changed."""
    changed = False

    track_id = str(apple.get("trackId") or "")
    if track_id and ep.get("appleEpisodeId") != track_id:
        ep["appleEpisodeId"] = track_id
        changed = True

    view_url = apple.get("trackViewUrl") or ""
    links = ep.get("links") or {}
    if view_url and links.get("apple") != view_url:
        links["apple"] = view_url
        ep["links"] = links
        changed = True

    full_desc = strip_tags(apple.get("description") or "")
    stored = (ep.get("description") or "").strip()
    # Upgrade only when Apple's text is a strict improvement: never overwrite a
    # longer hand-written description with a shorter feed one.
    if full_desc and len(full_desc) > len(stored):
        ep["description"] = full_desc
        changed = True

    return changed


def main() -> int:
    prefix, episodes = load_episodes()
    apple_by_title = fetch_apple_episodes()

    changed_titles = []
    missing_titles = []
    for ep in episodes:
        apple = apple_by_title.get(norm_title(ep.get("title", "")))
        if apple is None:
            missing_titles.append(ep.get("title", "?"))
            continue
        if apply_apple_data(ep, apple):
            changed_titles.append(ep.get("title", "?"))

    if changed_titles:
        save_episodes(prefix, episodes)
        for t in changed_titles:
            print(f"Resolved Apple data: {t}")
    else:
        print("All episodes already resolved. episodes.js unchanged.")

    for t in missing_titles:
        print(f"WARNING: no Apple match for: {t}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
