#!/usr/bin/env python3
"""
Sync new episodes from the show's RSS feed into episodes.js.

This script is safe to run on a schedule:
- Every feed item not already in episodes.js is added (newest ends up
  first), up to MAX_NEW_PER_RUN per run. Nothing new means no write.
- Existing entries are matched by feed guid, then by normalised title,
  then by date + guest, so a punctuation edit in the feed never creates a
  duplicate episode.
- A feed or network outage exits non-zero WITHOUT touching episodes.js,
  and save_episodes() refuses to ever write a shorter list.
"""

from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Callable

# One implementation shared with the generators, so a title parses to the
# same guest name (and the same URL slug) everywhere.
from seo_urls import episode_slug, extract_guest_name  # noqa: F401 (re-exported)

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"

APPLE_PODCAST_ID = "1853933144"
SHOW_SPOTIFY = "https://open.spotify.com/show/4vUJmF28QI4N7WViFmFofH"
SHOW_APPLE = "https://podcasts.apple.com/us/podcast/the-making-of-hosted-by-jack-pitts/id1853933144"
SHOW_YOUTUBE = "https://www.youtube.com/channel/UC0Oo8G_-OHHekbC5kpyIRBg"

# Riverside hosts the show. Apple's lookup normally tells us this URL, but if
# Apple is down we still know where the feed lives (index.html publishes the
# same address as webFeed).
FEED_URL_FALLBACK = "https://api.riverside.fm/hosting/wMWn2YqB.rss"

SHOW_NAME = "The Making Of Hosted By Jack Pitts"

UA = "Mozilla/5.0 (TheMakingOf Episode Sync Bot)"

FETCH_TIMEOUT_SECONDS = 30
FETCH_ATTEMPTS = 3
FETCH_BACKOFF_SECONDS = 5  # waits 5s, then 10s, between attempts

# More than this many new items in one run almost always means matching broke,
# so add the newest few and shout about it instead of flooding the site.
MAX_NEW_PER_RUN = 10

ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def fetch_text(url: str) -> str:
    """GET a URL as text, retrying transient failures with backoff.

    Raises RuntimeError with a readable message once every attempt failed.
    """
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last_error: Exception | None = None
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < FETCH_ATTEMPTS:
                delay = FETCH_BACKOFF_SECONDS * 2 ** (attempt - 1)
                warn(f"fetch {url} failed ({exc}); retry {attempt}/{FETCH_ATTEMPTS - 1} in {delay}s")
                time.sleep(delay)
    raise RuntimeError(f"Could not fetch {url} after {FETCH_ATTEMPTS} attempts: {last_error}")


def normalize_show_name(text: str) -> str:
    """Rewrite feed variants of the show name to the house form.

    The feed says "The Making Of, Hosted by Jack Pitts," and "The Making Of, I
    sit down...". Both become "The Making Of Hosted By Jack Pitts,". A title
    like "The Making of Kris Carlson: ..." is left alone (no comma after Of).
    """
    text = re.sub(
        r"The Making Of,?\s+Hosted\s+By\s+Jack\s+Pitts(?:\s+(?=[,.;:!?]))?",
        SHOW_NAME,
        text,
        flags=re.I,
    )
    return re.sub(r"The Making Of\s*,", SHOW_NAME + ",", text, flags=re.I)


def remove_em_dashes(text: str) -> str:
    return re.sub(r"\s*\u2014\s*", ", ", text)


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = unescape(text)
    # House style bans em dashes. This is the single funnel every Apple
    # description passes through on its way into episodes.js, so normalising
    # here is the only fix that survives: editing episodes.js by hand gets
    # reverted the next time resolve_episode_links.py upgrades a description
    # from the feed. En dashes are left alone because they carry meaning in
    # numeric ranges like "2008-2009".
    text = remove_em_dashes(text)
    text = re.sub(r"\s+", " ", text).strip()
    # Same reasoning: the show name is always written one way on the site.
    return normalize_show_name(text)


def fmt_date_label(dt: datetime) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


DESCRIPTION_LIMIT = 400


def truncate_at_word(text: str, limit: int = DESCRIPTION_LIMIT) -> str:
    """Truncate to at most `limit` chars, preferring to end on a complete
    sentence so cards never read as cut off mid-thought. Falls back to a
    word-boundary cut with an ellipsis when no sentence ends late enough."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    # A sentence end is . ! or ? followed by whitespace (or the cut edge),
    # so decimals like "$5.1 million" don't count. Only use it when it isn't
    # absurdly early, otherwise a one-word opener would swallow the card.
    sentence_ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", cut)]
    if sentence_ends and sentence_ends[-1] >= limit // 3:
        return cut[: sentence_ends[-1]]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,;:.-") + "…"


# Feed descriptions often open with the same lead-in ("In this episode of The
# Making Of Hosted By Jack Pitts, I sit down with ..."). Cards drop it at
# display time so a row of cards does not repeat it; episodes.js keeps the
# original text. Mirrors cardBlurb() in index.html.
_LEAD_IN_WITH_VERB = re.compile(
    r"^(?:in|on) this (?:episode|conversation)(?: of the making of hosted by jack pitts)?,\s*"
    r"(?:host jack pitts|jack pitts|jack|i)\s+(?:sits down with|sit down with|sat down with|interviews)\s+",
    re.I,
)
_LEAD_IN = re.compile(r"^(?:in|on) this (?:episode|conversation)(?: of the making of hosted by jack pitts)?,\s*", re.I)


def card_blurb(text: str, limit: int = DESCRIPTION_LIMIT) -> str:
    """Strip the stock feed lead-in, then trim like truncate_at_word."""
    text = (text or "").strip()
    stripped = _LEAD_IN_WITH_VERB.sub("", text, count=1)
    if stripped == text:
        stripped = _LEAD_IN.sub("", text, count=1)
    if stripped and stripped != text:
        text = stripped[0].upper() + stripped[1:]
    return truncate_at_word(text, limit)


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


def norm_title(title: str) -> str:
    """Normalize a title for matching.

    Casefolds, folds accents, and turns every run of punctuation, quotes,
    dashes and whitespace into one space, so curly vs straight quotes, an
    en dash vs a hyphen, or a doubled space never count as a different title.
    """
    text = unicodedata.normalize("NFKD", str(title or "").casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def load_episodes() -> tuple[str, list[dict]]:
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"^(.*?window\.EPISODES\s*=\s*)(\[.*\])\s*;\s*$", text, re.S)
    if not m:
        raise RuntimeError("Could not parse episodes.js window.EPISODES block")
    prefix = m.group(1)
    episodes = json.loads(m.group(2))
    return prefix, episodes


def save_episodes(prefix: str, episodes: list[dict]) -> None:
    """Write episodes.js atomically. Never writes a shorter list than is on disk."""
    if not episodes:
        raise RuntimeError("Refusing to write an empty episode list to episodes.js")
    if EPISODES_JS.exists():
        _, current = load_episodes()
        if len(episodes) < len(current):
            raise RuntimeError(
                f"Refusing to shrink episodes.js from {len(current)} to {len(episodes)} entries"
            )
    content = prefix + json.dumps(episodes, indent=2, ensure_ascii=False) + ";\n"
    tmp = EPISODES_JS.with_name(EPISODES_JS.name + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(EPISODES_JS)


def discover_feed_url(fetch: Callable[[str], str] = fetch_text) -> str:
    """The show's RSS URL from Apple's lookup, or the known Riverside feed."""
    lookup_url = (
        "https://itunes.apple.com/lookup?"
        + urllib.parse.urlencode({"id": APPLE_PODCAST_ID, "entity": "podcast"})
    )
    try:
        results = json.loads(fetch(lookup_url)).get("results") or []
        feed_url = results[0].get("feedUrl") if results else None
    except (RuntimeError, ValueError, AttributeError) as exc:
        warn(f"Apple lookup failed ({exc}); using the known feed URL")
        return FEED_URL_FALLBACK
    if not feed_url:
        warn("Apple lookup returned no feedUrl; using the known feed URL")
        return FEED_URL_FALLBACK
    return feed_url


def parse_feed_item(item: ET.Element) -> dict:
    """One RSS <item> as an episodes.js entry (slug pinned, guid stored)."""
    title = remove_em_dashes((item.findtext("title") or "").strip())
    pub_date_raw = (item.findtext("pubDate") or "").strip()
    description = (item.findtext("description") or "").strip()
    itunes_summary = item.findtext(f"{ITUNES_NS}summary")
    duration_raw = item.findtext(f"{ITUNES_NS}duration") or ""
    guid = (item.findtext("guid") or "").strip()

    if not title:
        raise RuntimeError("Feed item missing title")
    if not pub_date_raw:
        raise RuntimeError(f"Feed item missing pubDate: {title}")

    # UTC, so the stored date never depends on the machine running the sync.
    dt = parsedate_to_datetime(pub_date_raw)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

    guest = extract_guest_name(title)
    entry = {
        "date": dt.strftime("%Y-%m-%d"),
        "dateLabel": fmt_date_label(dt),
        "title": title,
        "guest": guest,
        # Pinned once, here, so a later guest-name fix never moves the URL.
        "slug": episode_slug({"guest": guest, "title": title}),
        # Store the FULL description; card renderers truncate at display time.
        "description": strip_tags(itunes_summary or description) or "Latest episode from the show.",
        "duration": normalize_duration(duration_raw),
        "guestLinkedIn": "",
        "links": {
            "spotify": SHOW_SPOTIFY,
            "apple": SHOW_APPLE,
            "youtube": SHOW_YOUTUBE,
        },
    }
    if guid:
        entry["guid"] = guid
    return entry


def parse_feed_items(feed_xml: str) -> list[dict]:
    """Every episode in the feed, in feed order. Refuses an empty feed."""
    try:
        root = ET.fromstring(feed_xml)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid RSS feed: {exc}") from exc
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("Invalid RSS feed: missing channel")
    items = [parse_feed_item(it) for it in channel.findall("item")]
    if not items:
        raise RuntimeError("RSS feed contains no episodes; refusing to touch episodes.js")
    return items


def fetch_feed_items() -> list[dict]:
    return parse_feed_items(fetch_text(discover_feed_url()))


def _guest_keys(ep: dict) -> set[str]:
    names = (ep.get("guest") or "", extract_guest_name(ep.get("title", "")))
    return {norm_title(n) for n in names if norm_title(n)}


def _find_match(item: dict, existing: list[dict]) -> int | None:
    """Index of the existing entry this feed item already is, if any."""
    guid = item.get("guid")
    if guid:
        for i, ep in enumerate(existing):
            if ep.get("guid") == guid:
                return i
    title = norm_title(item.get("title", ""))
    for i, ep in enumerate(existing):
        if norm_title(ep.get("title", "")) == title:
            return i
    item_guests = _guest_keys(item)
    for i, ep in enumerate(existing):
        if ep.get("date") == item.get("date") and item_guests & _guest_keys(ep):
            return i
    return None


def _with_unique_slug(entry: dict, taken: set[str]) -> dict:
    slug = entry.get("slug") or episode_slug(entry)
    if slug in taken:
        slug = f"{slug}-{entry['date']}"
    return {**entry, "slug": slug}


def _insert_by_date(episodes: list[dict], entry: dict) -> list[dict]:
    """New list with `entry` placed before the first older episode."""
    index = next(
        (i for i, ep in enumerate(episodes) if str(ep.get("date", "")) < entry["date"]),
        len(episodes),
    )
    return episodes[:index] + [entry] + episodes[index:]


def merge_new_episodes(
    existing: list[dict], items: list[dict], max_new: int = MAX_NEW_PER_RUN
) -> tuple[list[dict], list[dict]]:
    """Merge feed items into the episode list without mutating either input.

    Returns (merged list, entries added). Matched entries that lack a guid get
    the feed's guid backfilled so later title edits still match.
    """
    merged = list(existing)
    new_items: list[dict] = []
    for item in items:
        match = _find_match(item, merged)
        if match is None:
            new_items.append(item)
        elif item.get("guid") and not merged[match].get("guid"):
            merged[match] = {**merged[match], "guid": item["guid"]}

    if existing and len(new_items) > 1 and len(new_items) == len(items):
        raise RuntimeError(
            f"{len(new_items)} feed items and none match episodes.js; "
            "refusing to add them (title matching is probably broken)"
        )

    new_items = sorted(new_items, key=lambda e: e["date"])  # oldest first
    if len(new_items) > max_new:
        warn(
            f"{len(new_items)} new feed items; adding the newest {max_new} this run. "
            "The rest follow on later runs. Check the feed if this is unexpected."
        )
        new_items = new_items[-max_new:]

    added: list[dict] = []
    for item in new_items:
        entry = _with_unique_slug(item, {episode_slug(ep) for ep in merged})
        merged = _insert_by_date(merged, entry)
        added.append(entry)
    return merged, added


def run(fetch_items: Callable[[], list[dict]] = fetch_feed_items) -> int:
    """Sync once and return a process exit code. Never writes on failure."""
    try:
        prefix, episodes = load_episodes()
        items = fetch_items()
        merged, added = merge_new_episodes(episodes, items)
    except Exception as exc:  # report clearly, leave episodes.js untouched
        print(f"ERROR: episode sync failed, episodes.js unchanged: {exc}", file=sys.stderr)
        return 1

    if merged == episodes:
        print("No new episode detected. episodes.js unchanged.")
        return 0

    try:
        save_episodes(prefix, merged)
    except Exception as exc:
        print(f"ERROR: could not save episodes.js: {exc}", file=sys.stderr)
        return 1
    for entry in added:
        print(f"Added new episode: {entry['title']}")
    if not added:
        print("Stored feed guids on existing episodes.")
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
