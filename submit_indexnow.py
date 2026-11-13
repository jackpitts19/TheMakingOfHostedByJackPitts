#!/usr/bin/env python3
"""
Tell Bing and the other IndexNow engines that pages are new or changed.

Without this, a new page waits for an organic crawl, which is slow for pages
nothing links to (the unlisted podcast lists). With it, Bing, Yandex, Naver,
Seznam and Yep hear about them within seconds. Bing's index also feeds
ChatGPT search and Copilot. Google does not take part in IndexNow; submit the
sitemap in Search Console for Google.

Run from the repo root AFTER a deploy is live (the engines verify ownership by
fetching <key>.txt from the live site):

    python3 submit_indexnow.py --dry-run          # show what would be sent
    python3 submit_indexnow.py                    # every sitemap URL
    python3 submit_indexnow.py /articles/x /y     # just these paths

Stdlib only. A trimmed port of Salt Creek Advisory's tools/submit_indexnow.py.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

from seo_urls import BASE_URL, ROOT

ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_PATTERN = re.compile(r"^[0-9a-f]{8,128}$")
TIMEOUT_SECONDS = 30


def find_key() -> str:
    """The key from the one <key>.txt at the repo root whose content is its own name."""
    keys = [p for p in ROOT.glob("*.txt") if KEY_PATTERN.match(p.stem)]
    if len(keys) != 1:
        raise SystemExit(f"expected exactly one IndexNow key file at the repo root, found {len(keys)}")
    key = keys[0].stem
    if keys[0].read_text(encoding="utf-8").strip() != key:
        raise SystemExit(f"{keys[0].name} must contain exactly '{key}'")
    return key


def sitemap_urls() -> list[str]:
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return [u.strip() for u in re.findall(r"<loc>(.*?)</loc>", text, re.S)]


def urls_for(paths: list[str]) -> list[str]:
    if not paths:
        return sitemap_urls()
    known = set(sitemap_urls())
    urls = [BASE_URL + (p if p.startswith("/") else "/" + p) for p in paths]
    unknown = [u for u in urls if u not in known]
    if unknown:
        raise SystemExit(f"not in sitemap.xml (typo, or regenerate it first): {unknown}")
    return urls


def payload(key: str, urls: list[str]) -> dict:
    return {
        "host": urlparse(BASE_URL).hostname,
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": urls,
    }


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    paths = [a for a in argv if not a.startswith("--")]
    body = payload(find_key(), urls_for(paths))
    if dry_run:
        print(json.dumps(body, indent=2))
        return 0
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            print(f"IndexNow accepted {len(body['urlList'])} URLs (HTTP {response.status}).")
            return 0
    except urllib.error.HTTPError as err:
        # 403: key file not live yet or wrong; 422: URLs do not match the host.
        print(f"IndexNow rejected the submission: HTTP {err.code} {err.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
