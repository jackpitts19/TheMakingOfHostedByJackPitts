#!/usr/bin/env python3
"""
Validate the site's indexable surface. Read-only; exits non-zero on failure.

This is the guard rail for the whole SEO setup. It fails the build when any of
the following is true, because each one costs real Search Console coverage:

  * a sitemap URL has no file behind it (would 404 for Googlebot)
  * a sitemap URL keeps a `.html` suffix (Cloudflare Pages 307-redirects those,
    and Search Console reports "Page with redirect -- not indexed")
  * a public page is missing from the sitemap
  * a page is missing a title, meta description, or canonical tag
  * a canonical does not point at the page's own canonical URL
  * two pages share a title or a description (duplicate-content signal)
  * a page carries noindex or nofollow
  * an internal link points at a missing file or at a redirecting `.html` URL
  * robots.txt does not allow crawling or does not advertise the sitemap

Run: python3 validate_seo.py
"""

from __future__ import annotations

import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from generate_sitemap import load_episodes
from seo_urls import BASE_URL, ROOT, public_paths, source_file_for, to_url

SITEMAP_XML = ROOT / "sitemap.xml"
ROBOTS_TXT = ROOT / "robots.txt"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Non-HTML files that internal links may legitimately point at.
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico", ".xml", ".txt", ".pdf"}

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"', re.S | re.I)
ROBOTS_META_RE = re.compile(r'<meta\s+name="robots"\s+content="(.*?)"', re.I)
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="(.*?)"', re.I)
HREF_RE = re.compile(r'href="([^"]+)"')

# The homepage's client-side renderer builds hrefs by string concatenation
# (`'<a href="' + pageHref + '">'`). Those are code, not markup, so they are
# stripped before link checking -- otherwise every JS template reads as a
# broken link. The no-JS fallback markup they mirror is still checked.
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sitemap_locs() -> list[str]:
    root = ET.parse(SITEMAP_XML).getroot()
    return [el.text.strip() for el in root.findall("sm:url/sm:loc", SITEMAP_NS) if el.text]


def check_sitemap(errors: list[str], expected_paths: list[str]) -> None:
    if not SITEMAP_XML.is_file():
        errors.append("sitemap.xml is missing")
        return

    try:
        locs = sitemap_locs()
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml is not valid XML: {exc}")
        return

    if not locs:
        errors.append("sitemap.xml contains no <loc> entries")
        return

    seen: set[str] = set()
    for loc in locs:
        if loc in seen:
            errors.append(f"sitemap: duplicate URL {loc}")
        seen.add(loc)

        if not loc.startswith(BASE_URL + "/"):
            errors.append(f"sitemap: URL is not on the canonical domain: {loc}")
            continue
        if loc.endswith(".html"):
            errors.append(f"sitemap: `.html` URL 307-redirects, use extensionless: {loc}")
        if "#" in loc:
            errors.append(f"sitemap: fragment URLs are not distinct pages: {loc}")

        path = loc[len(BASE_URL):]
        if not source_file_for(path).is_file():
            errors.append(f"sitemap: no file on disk for {loc} (would 404)")

    expected_urls = {to_url(p) for p in expected_paths}
    for missing in sorted(expected_urls - seen):
        errors.append(f"sitemap: public page missing from sitemap: {missing}")


def check_robots(errors: list[str]) -> None:
    if not ROBOTS_TXT.is_file():
        errors.append("robots.txt is missing")
        return

    text = read(ROBOTS_TXT)
    if not re.search(r"^User-agent:\s*\*", text, re.M | re.I):
        errors.append("robots.txt: no `User-agent: *` group")
    if not re.search(r"^Allow:\s*/\s*$", text, re.M | re.I):
        errors.append("robots.txt: no `Allow: /`")
    if re.search(r"^Disallow:\s*/\s*$", text, re.M | re.I):
        errors.append("robots.txt: `Disallow: /` blocks the whole site")
    if f"Sitemap: {BASE_URL}/sitemap.xml" not in text:
        errors.append(f"robots.txt: missing `Sitemap: {BASE_URL}/sitemap.xml`")


def check_error_page(errors: list[str]) -> None:
    """The 404 must exist, be noindex, and stay out of the sitemap.

    Cloudflare Pages serves /404.html for unmatched routes. If it were
    indexable it would land in Search Console as a soft 404; if it were listed
    in the sitemap it would be a URL that never returns 200.
    """
    file = ROOT / "404.html"
    if not file.is_file():
        errors.append("404.html is missing (Cloudflare Pages serves it for unmatched routes)")
        return

    html = read(file)
    robots = ROBOTS_META_RE.search(html)
    if not robots or "noindex" not in robots.group(1).lower():
        errors.append("404.html: must be noindex, or it becomes a soft 404 in Search Console")
    if SITEMAP_XML.is_file() and "/404" in read(SITEMAP_XML):
        errors.append("404.html must not be listed in sitemap.xml")


def resolve_link(href: str, from_path: str) -> str | None:
    """Site-root-relative target of an internal link, or None if external."""
    href = href.split("#", 1)[0].strip()
    if not href:
        return None
    if href.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    if href.startswith("//"):
        return None
    if href.startswith("http"):
        if not href.startswith(BASE_URL):
            return None
        href = href[len(BASE_URL):] or "/"
    if href.startswith("/"):
        return posixpath.normpath(href)
    # Relative: resolve against the linking page's directory.
    return posixpath.normpath(posixpath.join(posixpath.dirname(from_path) or "/", href))


def check_page(errors: list[str], path: str, titles: dict, descs: dict) -> None:
    file = source_file_for(path)
    html = read(file)
    rel = file.relative_to(ROOT)

    title_m = TITLE_RE.search(html)
    title = title_m.group(1).strip() if title_m else ""
    if not title:
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(title, []).append(path)

    desc_m = DESC_RE.search(html)
    desc = desc_m.group(1).strip() if desc_m else ""
    if not desc:
        errors.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(desc, []).append(path)

    robots_m = ROBOTS_META_RE.search(html)
    if robots_m:
        directives = robots_m.group(1).lower()
        if "noindex" in directives:
            errors.append(f"{rel}: page is noindex")
        if "nofollow" in directives:
            errors.append(f"{rel}: page is nofollow")

    canon_m = CANONICAL_RE.search(html)
    if not canon_m:
        errors.append(f"{rel}: missing canonical tag")
    elif canon_m.group(1).strip() != to_url(path):
        errors.append(
            f"{rel}: canonical is {canon_m.group(1).strip()}, expected {to_url(path)}"
        )

    for href in HREF_RE.findall(SCRIPT_STYLE_RE.sub("", html)):
        target = resolve_link(href, path)
        if target is None:
            continue
        if target.endswith(".html"):
            errors.append(f"{rel}: internal link 307-redirects (drop `.html`): {href}")
            continue
        suffix = posixpath.splitext(target)[1].lower()
        exists = (
            (ROOT / target.lstrip("/")).is_file()
            if suffix in ASSET_SUFFIXES
            else source_file_for(target).is_file()
        )
        if not exists:
            errors.append(f"{rel}: broken internal link {href} -> {target}")


def check_duplicates(errors: list[str], titles: dict, descs: dict) -> None:
    for title, paths in titles.items():
        if len(paths) > 1:
            errors.append(f"duplicate <title> on {', '.join(paths)}: {title[:60]!r}")
    for desc, paths in descs.items():
        if len(paths) > 1:
            errors.append(f"duplicate description on {', '.join(paths)}: {desc[:60]!r}")


def run_checks() -> list[str]:
    """Every problem found, as human-readable strings. Empty means healthy."""
    errors: list[str] = []
    paths = public_paths(load_episodes())

    check_robots(errors)
    check_sitemap(errors, paths)
    check_error_page(errors)

    titles: dict[str, list[str]] = {}
    descs: dict[str, list[str]] = {}
    for path in paths:
        if not source_file_for(path).is_file():
            errors.append(f"{path}: no source file at {source_file_for(path).name}")
            continue
        check_page(errors, path, titles, descs)
    check_duplicates(errors, titles, descs)

    return errors


def main() -> int:
    errors = run_checks()
    if errors:
        print(f"SEO validation FAILED with {len(errors)} problem(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"SEO validation passed: {len(public_paths(load_episodes()))} public URLs, all checks green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
