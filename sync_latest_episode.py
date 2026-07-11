#!/usr/bin/env python3
"""
Sync the newest episode from Apple Podcasts RSS into episodes.js.

This script is safe to run on a schedule:
- If the latest feed episode already exists, it exits without changes.
- If a new episode exists, it prepends one entry to window.EPISODES.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"

APPLE_PODCAST_ID = "1853933144"
SHOW_SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
SHOW_APPLE = "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
SHOW_YOUTUBE = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"

UA = "Mozilla/5.0 (TheMakingOf Episode Sync Bot)"


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fmt_date_label(dt: datetime) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


DESCRIPTION_LIMIT = 400


def truncate_at_word(text: str, limit: int = DESCRIPTION_LIMIT) -> str:
    """Truncate to at most `limit` chars without cutting mid-word; add an ellipsis."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,;:.-") + "…"


def normalize_duration(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return "Full episode"
    if raw.isdigit():
        n = int(raw)
        h, rem = divmod(n, 3600)
        m = rem // 60
        if h > 0:
            return f"{h}h {m}m"
        return f"{m} min"
    if ":" in raw:
        parts = [int(p) if p.isdigit() else 0 for p in raw.split(":")]
        if len(parts) == 3:
            h, m, _ = parts
            if h > 0:
                return f"{h}h {m}m"
            return f"{m} min"
        if len(parts) == 2:
            m, _ = parts
            return f"{m} min"
    return raw


def extract_guest_name(title: str) -> str:
    t = title or ""
    t = re.sub(r"^In\s+The\s+Making\s+Of:\s*", "", t, flags=re.I)
    t = re.sub(r"^The\s+Making\s+(Of|of)\s+", "", t, flags=re.I)
    t = re.split(r":|\s+with\s+|\s+from\s+", t, maxsplit=1, flags=re.I)[0]
    t = re.sub(r"^[\"“”'\s]+|[\"“”'\s]+$", "", t)
    return t or title


def load_episodes() -> tuple[str, list[dict]]:
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"^(.*?window\.EPISODES\s*=\s*)(\[.*\])\s*;\s*$", text, re.S)
    if not m:
        raise RuntimeError("Could not parse episodes.js window.EPISODES block")
    prefix = m.group(1)
    episodes = json.loads(m.group(2))
    return prefix, episodes


def save_episodes(prefix: str, episodes: list[dict]) -> None:
    content = prefix + json.dumps(episodes, indent=2, ensure_ascii=False) + ";\n"
    EPISODES_JS.write_text(content, encoding="utf-8")


def fetch_latest_from_feed() -> dict:
    lookup_url = (
        "https://itunes.apple.com/lookup?"
        + urllib.parse.urlencode({"id": APPLE_PODCAST_ID, "entity": "podcast"})
    )
    lookup = json.loads(fetch_text(lookup_url))
    results = lookup.get("results") or []
    if not results or not results[0].get("feedUrl"):
        raise RuntimeError("No feedUrl returned from Apple lookup")

    feed_url = results[0]["feedUrl"]
    feed_xml = fetch_text(feed_url)
    root = ET.fromstring(feed_xml)
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("Invalid RSS feed: missing channel")

    item = channel.find("item")
    if item is None:
        raise RuntimeError("RSS feed contains no episodes")

    title = (item.findtext("title") or "").strip()
    pub_date_raw = (item.findtext("pubDate") or "").strip()
    description = (item.findtext("description") or "").strip()
    itunes_summary = item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}summary")
    duration_raw = item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}duration") or ""

    if not title:
        raise RuntimeError("Latest feed item missing title")
    if not pub_date_raw:
        raise RuntimeError("Latest feed item missing pubDate")

    dt = parsedate_to_datetime(pub_date_raw)
    if dt.tzinfo is not None:
        dt = dt.astimezone(tz=None).replace(tzinfo=None)

    # Store the FULL description; card renderers truncate at display time.
    clean_desc = strip_tags(itunes_summary or description) or "Latest episode from the show."

    return {
        "date": dt.strftime("%Y-%m-%d"),
        "dateLabel": fmt_date_label(dt),
        "title": title,
        "guest": extract_guest_name(title),
        "description": clean_desc,
        "duration": normalize_duration(duration_raw),
        "guestLinkedIn": "",
        "links": {
            "spotify": SHOW_SPOTIFY,
            "apple": SHOW_APPLE,
            "youtube": SHOW_YOUTUBE,
        },
    }


def main() -> int:
    prefix, episodes = load_episodes()
    latest = fetch_latest_from_feed()

    existing_titles = {str(ep.get("title", "")).strip().lower() for ep in episodes}
    if latest["title"].strip().lower() in existing_titles:
        print("No new episode detected. episodes.js unchanged.")
        return 0

    episodes.insert(0, latest)
    save_episodes(prefix, episodes)
    print(f"Added new episode: {latest['title']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
