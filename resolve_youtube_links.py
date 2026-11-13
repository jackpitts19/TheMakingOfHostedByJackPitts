#!/usr/bin/env python3
"""
Point each episode's YouTube button at its own video, not the channel page.

New episodes arrive from the podcast feed with links.youtube set to the
channel URL, because the feed knows nothing about YouTube. A visitor (or a
prospective guest's team) who clicks "YouTube" then lands on the channel page
instead of the conversation. This reads the channel's public uploads feed
(no API key), matches videos to episodes by normalised title, and fills in the
watch URL.

Rules:
  - Only an episode still pointing at the channel URL is changed. A watch URL
    set by hand is never overwritten.
  - The feed lists only the latest uploads, which is all a new episode needs;
    older episodes were mapped once by hand.
  - Enrichment only: if YouTube is unreachable it warns, leaves episodes.js
    exactly as it was, and exits 0 so the rest of the sync continues.

Run: python3 resolve_youtube_links.py   (CI runs it after resolve_episode_links.py)
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from typing import Callable

from sync_latest_episode import SHOW_YOUTUBE, fetch_text, load_episodes, norm_title, save_episodes

CHANNEL_ID = "UC0Oo8G_-OHHekbC5kpyIRBg"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}


def watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def parse_feed(xml_text: str) -> dict[str, str]:
    """Normalised video title -> watch URL. The first (newest) upload wins on a duplicate title."""
    root = ET.fromstring(xml_text)
    videos: dict[str, str] = {}
    for entry in root.findall("atom:entry", NS):
        video_id = entry.findtext("yt:videoId", default="", namespaces=NS).strip()
        key = norm_title(entry.findtext("atom:title", default="", namespaces=NS))
        if video_id and key and key not in videos:
            videos[key] = watch_url(video_id)
    return videos


def apply_youtube(episodes: list[dict], videos: dict[str, str]) -> list[str]:
    """Fill links.youtube for episodes still on the channel URL. Returns changed titles."""
    changed = []
    for ep in episodes:
        links = ep.get("links") or {}
        if links.get("youtube") not in (None, "", SHOW_YOUTUBE):
            continue  # already points at a video: never overwrite
        url = videos.get(norm_title(ep.get("title", "")))
        if url:
            ep["links"] = {**links, "youtube": url}
            changed.append(ep.get("title", "?"))
    return changed


def fetch_videos() -> dict[str, str]:
    return parse_feed(fetch_text(FEED_URL))


def main(fetch: Callable[[], dict[str, str]] = fetch_videos) -> int:
    prefix, episodes = load_episodes()
    try:
        videos = fetch()
    except (RuntimeError, ValueError, OSError, ET.ParseError) as exc:
        print(f"WARNING: YouTube feed unavailable, episodes.js left unchanged: {exc}", file=sys.stderr)
        return 0
    changed = apply_youtube(episodes, videos)
    if changed:
        save_episodes(prefix, episodes)
        for title in changed:
            print(f"Linked YouTube video: {title}")
    else:
        print("YouTube links unchanged.")
    for ep in episodes:
        if (ep.get("links") or {}).get("youtube") == SHOW_YOUTUBE:
            print(f"WARNING: no YouTube video found yet for: {ep.get('title', '?')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
