#!/usr/bin/env python3
"""
Fail loudly if search or AI crawlers stop getting the real site.

The site can be perfect and still invisible: one Cloudflare toggle ("Block AI
bots", "AI Labyrinth", a bot-fight mode, or a managed robots.txt that appends
Disallow rules) silently shuts out ChatGPT, Claude, Perplexity, or even
Google. None of that lives in this repo, so no other check would notice.

This requests a few live pages as each crawler and checks that it gets HTTP
200 with the real page (its <h1>), not a challenge page, and that the live
robots.txt does not disallow it. CI runs it after every sync; a failure makes
the workflow red and GitHub emails the owner.

Run: python3 check_crawler_access.py   (stdlib only; needs network)
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request

from seo_urls import BASE_URL

CRAWLERS = {
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "GPTBot": "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)",
    "OAI-SearchBot": "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)",
    "ClaudeBot": "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
    "PerplexityBot": "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
}

# One page of each kind the crawlers need: the homepage and the two archives.
# Archives, not a single article, so the check never depends on one URL.
# Kept small so the check stays fast and polite.
PATHS = ("/", "/episodes", "/articles")

# Markers of a bot challenge or block page served instead of the real page.
CHALLENGE_MARKERS = ("cf-chl", "challenge-platform", "Just a moment...", "Attention Required!")

TIMEOUT_SECONDS = 20


def fetch(url: str, user_agent: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        return err.code, ""
    except (urllib.error.URLError, TimeoutError) as err:
        return 0, str(err)


def page_problem(status: int, body: str) -> str | None:
    """Why a crawler's response is not the real page, or None if it is."""
    if status != 200:
        return f"HTTP {status}"
    if any(marker in body for marker in CHALLENGE_MARKERS):
        return "got a bot challenge page"
    if "<h1" not in body:
        return "page has no <h1>, so it is not the real page"
    return None


def disallowed_agents(robots_txt: str) -> list[str]:
    """Crawlers from CRAWLERS that robots.txt blocks from the whole site."""
    blocked: set[str] = set()
    groups = re.split(r"\n\s*\n", robots_txt.replace("\r\n", "\n"))
    for group in groups:
        agents = [a.strip().lower() for a in re.findall(r"(?im)^\s*user-agent:\s*(.+)$", group)]
        if not re.search(r"(?im)^\s*disallow:\s*/\s*$", group):
            continue
        for name in CRAWLERS:
            if name.lower() in agents or "*" in agents:
                blocked.add(name)
    return sorted(blocked)


def main() -> int:
    failures: list[str] = []
    status, robots = fetch(f"{BASE_URL}/robots.txt", "Mozilla/5.0")
    if status != 200:
        failures.append(f"robots.txt: HTTP {status}")
    else:
        failures.extend(f"robots.txt disallows {name} from the whole site" for name in disallowed_agents(robots))

    for name, user_agent in CRAWLERS.items():
        for path in PATHS:
            problem = page_problem(*fetch(BASE_URL + path, user_agent))
            if problem:
                failures.append(f"{name} {path}: {problem}")

    if failures:
        print("Crawler access check FAILED. Check the Cloudflare bot settings:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"Crawler access OK: {len(CRAWLERS)} crawlers x {len(PATHS)} pages, robots.txt allows all.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
