#!/usr/bin/env python3
"""
Produce logo.webp, the web-sized hero logo, from the full-resolution logo.png.

Why: logo.png is 1024x1024 and 1751 KB, and it renders in the homepage hero
above the fold, which makes it the Largest Contentful Paint element. Core Web
Vitals is a ranking factor, so shipping 1.7 MB there is a direct SEO cost.

logo.png is deliberately left untouched at full resolution: the Press Kit
section of index.html offers it as a download ("Show logo (PNG)"), and press
need the high-res file. Only the hero swaps to WebP, via a <picture> element
whose <img> still falls back to logo.png for the ~3% of browsers without WebP.

The hero renders at max-width 440px, so 880px covers 2x retina exactly.

Run: python3 generate_logo_webp.py   (needs Pillow: pip install pillow)
"""

from __future__ import annotations

import sys

from PIL import Image

from seo_urls import ROOT

SOURCE = ROOT / "logo.png"
TARGET = ROOT / "logo.webp"

# The hero is `max-width: 440px`; 2x that is crisp on retina without waste.
HERO_WIDTH_PX = 880
WEBP_QUALITY = 88


def main() -> int:
    if not SOURCE.is_file():
        raise RuntimeError(f"{SOURCE.name} not found")

    with Image.open(SOURCE) as im:
        original_kb = SOURCE.stat().st_size // 1024
        resized = im.convert("RGBA").resize(
            (HERO_WIDTH_PX, HERO_WIDTH_PX), Image.LANCZOS
        )
        resized.save(TARGET, "WEBP", quality=WEBP_QUALITY, method=6)

    new_kb = TARGET.stat().st_size // 1024
    saved = original_kb - new_kb
    print(
        f"Wrote {TARGET.name}: {HERO_WIDTH_PX}px, {new_kb} KB "
        f"(from {original_kb} KB, saved {saved} KB / {saved * 100 // original_kb}%)"
    )
    print(f"{SOURCE.name} left untouched at full resolution for the press kit.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
