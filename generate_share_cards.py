#!/usr/bin/env python3
"""
Generate branded social share cards for The Making Of Hosted By Jack Pitts.

Reads episodes.js, generates one 1200x630 PNG per episode in ./share-cards/,
and a default 'latest.png' that points at the newest episode. Drop a new
episode into episodes.js and re-run this script to regenerate.

Brand palette and rules match the tmo-podcast skill: cream background,
orange accents, Fraunces serif for headers, Inter for body, no em dashes.
"""

import json
import re
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"
OUT_DIR = ROOT / "share-cards"
OUT_DIR.mkdir(exist_ok=True)

# Brand
CREAM = (243, 232, 207)
CREAM_DEEP = (236, 217, 168)
ORANGE = (216, 122, 44)
ORANGE_DARK = (184, 95, 24)
INK = (20, 19, 15)
INK_SOFT = (58, 53, 43)

W, H = 1200, 630


def load_episodes():
    text = EPISODES_JS.read_text(encoding="utf-8")
    # Strip the "window.EPISODES = " prefix and trailing semicolon
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise RuntimeError("Could not parse episodes.js")
    arr_js = m.group(1)
    return json.loads(arr_js)


def find_font(*candidates, size=48):
    """Try a series of font filenames, fall back to default."""
    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Greedy word-wrap honoring max pixel width."""
    words = text.split()
    lines, cur = [], []
    for word in words:
        trial = " ".join(cur + [word])
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [word]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_waveform(draw, y_top, y_bot, color, opacity=1.0):
    """Decorative orange waveform across the bottom."""
    import math
    steps = 240
    points = []
    span = W
    amp = (y_bot - y_top) / 2
    mid = (y_bot + y_top) / 2
    for i in range(steps + 1):
        x = i * span / steps
        y = mid + amp * math.sin(i / steps * 8 * math.pi)
        points.append((x, y))
    for a, b in zip(points, points[1:]):
        draw.line([a, b], fill=color, width=3)


def render_card(ep, out_path):
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img, "RGBA")

    # Subtle deep-cream band along right side
    draw.rectangle([W - 14, 0, W, H], fill=CREAM_DEEP)

    # Decorative waveform near the bottom edge
    draw_waveform(draw, H - 130, H - 60, (*ORANGE, 110))
    draw_waveform(draw, H - 165, H - 95, (*ORANGE, 60))

    # Top eyebrow: "The Making Of Hosted by Jack Pitts"
    eyebrow_font = find_font(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        size=22,
    )
    eyebrow = "THE MAKING OF / HOSTED BY JACK PITTS"
    draw.text((72, 60), eyebrow, fill=ORANGE_DARK, font=eyebrow_font)

    # Episode tag chip "LATEST EPISODE" or "EPISODE NO. XX"
    chip_font = find_font(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        size=18,
    )
    chip_label = ep.get("dateLabel", "").upper()
    if chip_label:
        bbox = draw.textbbox((0, 0), chip_label, font=chip_font)
        chip_w = bbox[2] - bbox[0] + 28
        chip_h = bbox[3] - bbox[1] + 16
        chip_x, chip_y = 72, 105
        draw.rounded_rectangle(
            [chip_x, chip_y, chip_x + chip_w, chip_y + chip_h],
            radius=chip_h // 2,
            fill=INK,
        )
        draw.text((chip_x + 14, chip_y + 6), chip_label, fill=CREAM, font=chip_font)

    # Big serif headline: guest + (short title fragment)
    guest = ep.get("guest", "").strip()
    title = ep.get("title", "").strip()

    headline_font = find_font(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "DejaVuSerif-Bold.ttf",
        size=72,
    )
    subhead_font = find_font(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "DejaVuSerif.ttf",
        size=34,
    )

    # Headline = "The Making Of {Guest}" if it's a regular ep, otherwise the title
    if guest and ("Making Of" in title or "Making of" in title):
        headline = f"The Making Of {guest}"
    elif guest and "In The Making Of" in title:
        headline = f"In The Making Of: {guest}"
    elif guest:
        headline = guest
    else:
        headline = title

    max_text_width = W - 144
    lines = wrap_text(draw, headline, headline_font, max_text_width)
    y = 200
    for line in lines[:3]:
        draw.text((72, y), line, fill=INK, font=headline_font)
        bbox = draw.textbbox((0, 0), line, font=headline_font)
        y += (bbox[3] - bbox[1]) + 14

    # Subhead: the descriptive part of the title after the colon, if any
    subhead = ""
    if ":" in title:
        subhead = title.split(":", 1)[1].strip()
    elif title and guest and title != headline:
        subhead = title
    if subhead:
        y += 12
        sub_lines = wrap_text(draw, subhead, subhead_font, max_text_width)
        for line in sub_lines[:2]:
            draw.text((72, y), line, fill=INK_SOFT, font=subhead_font)
            bbox = draw.textbbox((0, 0), line, font=subhead_font)
            y += (bbox[3] - bbox[1]) + 8

    # Footer: platforms + duration
    footer_font = find_font(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        size=22,
    )
    dur = ep.get("duration", "")
    footer_left = "LISTEN ON SPOTIFY, APPLE PODCASTS, YOUTUBE"
    draw.text((72, H - 50), footer_left, fill=INK_SOFT, font=footer_font)
    if dur:
        bbox = draw.textbbox((0, 0), dur, font=footer_font)
        draw.text(
            (W - 72 - (bbox[2] - bbox[0]), H - 50),
            dur,
            fill=ORANGE_DARK,
            font=footer_font,
        )

    img.save(out_path, "PNG", optimize=True)
    return out_path


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "-", name.lower()).strip("-")
    return s or "episode"


def main():
    episodes = load_episodes()
    print(f"Loaded {len(episodes)} episodes")

    for ep in episodes:
        slug = slugify(ep.get("guest", "") or ep.get("title", ""))
        out = OUT_DIR / f"{slug}.png"
        render_card(ep, out)
        print(f"Wrote {out.name}")

    # Default: latest
    if episodes:
        render_card(episodes[0], OUT_DIR / "latest.png")
        print("Wrote latest.png")


if __name__ == "__main__":
    main()
