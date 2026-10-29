#!/usr/bin/env python3
"""
Generate the link-preview share cards for The Making Of Hosted By Jack Pitts.

Reads episodes.js and writes 1200x630 PNGs to ./share-cards/:
  <episode slug>.png  one per episode (og:image on its episode page)
  latest.png          the newest episode
  show.png            a stable show-level card (og:image on every other page)

Type matches the site: Newsreader for the guest name and topic, Libre Franklin
for labels. card_type.py loads the vendored fonts (fonts/, SIL OFL, licence
files alongside) and sets each line with real pair kerning, so a Mac and the
ubuntu CI runner draw identical, properly kerned cards. Missing fonts are a
hard error: a silent fallback is how the old cards ended up in DejaVu.

Layout is a masthead: label, orange rule, meta row, then the name always
starts at the same height, so cards line up when they sit side by side.

House rules: show name exactly "The Making Of Hosted By Jack Pitts", no em
dashes, and every line of copy comes from episodes.js or seo_titles.py.
"""

import html
import json
import re
from functools import lru_cache
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from card_type import FONT_DIR, FONT_FILES, MissingFontError, check_fonts, face  # noqa: F401 (re-exported)
from seo_titles import SEO_TITLES
from seo_urls import episode_slug

ROOT = Path(__file__).parent
EPISODES_JS = ROOT / "episodes.js"
OUT_DIR = ROOT / "share-cards"
LOGO = ROOT / "logo.png"

SHOW_NAME = "The Making Of Hosted By Jack Pitts"
SITE_HOST = "themakingofhostedbyjackpitts.com"
LISTEN_LINE = "Listen on Spotify, Apple Podcasts, and YouTube"
SHOW_KICKER = "An entrepreneurship podcast"
SHOW_DECK = (
    "Founders, operators, and family-business owners on how they got "
    "started and how they grew."
)

# Palette (site tokens)
CREAM = (243, 232, 207)
CREAM_EDGE = (234, 220, 189)
ORANGE = (216, 122, 44)
BROWN = (138, 82, 31)
INK = (20, 19, 15)
INK_SOFT = (74, 66, 52)

# Geometry: one grid for every card
W, H = 1200, 630
MARGIN = 72
BAND_H = 72
BAND_TOP = H - BAND_H
EYEBROW_BASE = MARGIN + 18         # baseline of the top label
RULE_Y = EYEBROW_BASE + 22         # orange rule; the logo tile's top edge
META_BASE = RULE_Y + 40            # baseline of the episode meta row
NAME_TOP = META_BASE + 60          # cap-top of the guest name on every card
SHOW_NAME_TOP = RULE_Y + 60        # show card has no meta row
ART = 312                          # logo tile edge
ART_X = W - MARGIN - ART
ART_Y = RULE_Y
COL_W = ART_X - MARGIN - 64        # name column width
TOPIC_W = COL_W - 48               # wrapped italic lines stop short of the art gutter
ONE_LINE_TOPIC_W = COL_W - 16      # a topic that fits this wide stays on one line
TEXT_BOTTOM = BAND_TOP - 64        # lowest baseline the headline block may reach

NAME_MAX, NAME_MAX_TWO_LINES, NAME_MIN_ONE_LINE, NAME_MIN = 104, 84, 76, 52
TOPIC_SIZE = 36
SHOW_DECK_SIZE = 31
SHOW_DECK_LINES = 3                # the deck is never cut off with an ellipsis
EYEBROW_SIZE, EYEBROW_TRACKING = 19, 2.4
META_SIZE, META_TRACKING = 18, 1.6
LABEL_WORD_SPACE = 3
BAND_SIZE = 20
DOT_RADIUS, DOT_GAP = 2, 14
COLON_HEAD_MIN = 0.45              # colon break only if head >= 45% of tail
# Line-break rules for two-line topics, in px of "badness" on top of the
# longer line's width: never end a line on a small word ("Building a /"), and
# prefer breaking before one ("/ and Getting Into YC") or after a comma.
SMALL_WORDS = frozenset("a an the and or of to at in on for from with into through by as & vs".split())
END_ON_SMALL_WORD_PENALTY = 200
NATURAL_BREAK_BONUS = 60
LOGO_CROP = (176, 176, 848, 848)   # the orange-framed square in logo.png


# ---------------------------------------------------------------- data

def load_episodes():
    text = EPISODES_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.EPISODES\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise RuntimeError("Could not parse episodes.js")
    return json.loads(m.group(1))


def clean_text(text):
    """Decode entities, collapse whitespace, and set typographic quotes."""
    text = re.sub(r"\s+", " ", html.unescape(text or "")).strip()
    text = re.sub(r"(?<=\w)'(?=\w)", "\u2019", text)
    text = re.sub(r'(^|[\s(\[])"', "\\1\u201c", text)
    text = text.replace('"', "\u201d")
    text = re.sub(r"(^|[\s(\[])'", "\\1\u2018", text)
    return text.replace("'", "\u2019")


def _strip_guest(text, guest):
    """'Nishank Gite of Nirvana Robotics: X' -> 'Nirvana Robotics: X'."""
    if guest and text.lower().startswith(guest.lower()):
        text = text[len(guest):]
        text = re.sub(r"^\s*(?:of\b|,|:)\s*", "", text)
    return text[:1].upper() + text[1:] if text else ""


def _names_person(text, guest):
    """True if text spells out a guest's first and last name (not 'Taylor's Candy')."""
    for person in re.split(r"\s*&\s*|\s+and\s+", guest):
        words = person.split()
        if len(words) >= 2 and all(re.search(rf"\b{re.escape(w)}\b", text) for w in (words[0], words[-1])):
            return True
    return False


def _title_topic(title, guest):
    """The topic part of an episode title, or "" if the title is just the name."""
    if " | " in title:
        return title.split(" | ", 1)[0].strip()
    if ":" in title:
        head, tail = (p.strip() for p in title.split(":", 1))
        is_show_head = re.match(r"^(in\s+)?the\s+making\s+of\b", head, re.I)
        if is_show_head or head.lower() == guest.lower():
            return tail
        if guest and guest.lower() in head.lower():
            return _strip_guest(title, guest)  # "X of Company: Topic" keeps the company
        return title
    if title and title != guest:
        return re.sub(rf"\s+with\s+{re.escape(guest)}$", "", title) if guest else title
    return ""


def card_topic(ep):
    """The italic line under the guest name, derived from published copy only.

    "Topic | Guest" gives the topic; "The Making Of X: Topic" gives the part
    after the colon; a brand ahead of the colon that is not the guest stays
    ("Concentrate AI: The LLM Gateway ..."). A leading "The Making Of" is
    dropped because the show name is already on the card. If what is left is
    just the guest's name, the hand-checked search title in seo_titles.py is
    used, and failing that a quoted phrase from the title.
    """
    title = clean_text(ep.get("title"))
    guest = clean_text(ep.get("guest"))
    topic = re.sub(r"^the\s+making\s+of\s+", "", _title_topic(title, guest), flags=re.I)
    if topic and topic.lower() != guest.lower() and not _names_person(topic, guest):
        return topic
    seo = clean_text(ep.get("seoTitle") or SEO_TITLES.get(episode_slug(ep), ""))
    if seo:
        return _strip_guest(seo, guest)
    quoted = re.search(r"\u201c([^\u201d]+)\u201d", title)
    return f"\u201c{quoted.group(1)}\u201d" if quoted else ""


def card_meta(issue_no, ep):
    """'EPISODE 19 · OCTOBER 8, 2026 · 1 HR 9 MIN'."""
    bits = [f"Episode {issue_no:02d}"]
    if ep.get("dateLabel"):
        bits.append(clean_text(ep["dateLabel"]))
    dur = (ep.get("duration") or "").strip()
    m = re.fullmatch(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m(?:in)?)?", dur, re.I)
    if dur and m and (m.group(1) or m.group(2)):
        parts = [f"{m.group(1)} hr" if m.group(1) else "", f"{m.group(2)} min" if m.group(2) else ""]
        bits.append(" ".join(p for p in parts if p))
    return "  \u00b7  ".join(bits).upper()


# ---------------------------------------------------------------- text helpers

def wrap(text, measure, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if measure(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def balance(lines, measure, max_w):
    """Re-break wrapped lines so they are even and end in natural places.

    For two lines a colon is the preferred break, but only when the part
    before it is a real line (at least COLON_HEAD_MIN of the part after it);
    a lone brand word over a long line reads as ragged.
    """
    text = " ".join(lines)
    if len(lines) == 2 and ": " in text:
        head, tail = text.split(": ", 1)
        head_w, tail_w = measure(head + ":"), measure(tail)
        if head_w <= max_w and tail_w <= max_w and head_w >= COLON_HEAD_MIN * tail_w:
            return [head + ":", tail]
    words = text.split()
    best, best_score = lines, None
    for cuts in combinations(range(1, len(words)), len(lines) - 1):
        bounds = (0, *cuts, len(words))
        candidate = [" ".join(words[i:j]) for i, j in zip(bounds, bounds[1:])]
        widths = [measure(line) for line in candidate]
        if max(widths) > max_w:
            continue
        score = max(widths) + sum(break_badness(a, b) for a, b in zip(candidate, candidate[1:]))
        if best_score is None or score < best_score:
            best, best_score = candidate, score
    return best


def break_badness(first, second):
    """Penalty for breaking between two lines (negative is a good place)."""
    last_word = first.rsplit(" ", 1)[-1]
    badness = 0
    if last_word.lower() in SMALL_WORDS:
        badness += END_ON_SMALL_WORD_PENALTY
    if second.split(" ", 1)[0].lower() in SMALL_WORDS or last_word.endswith((",", ":", ";")):
        badness -= NATURAL_BREAK_BONUS
    return badness


def clamp_lines(text, measure, max_w, max_lines):
    """Wrap to at most max_lines, ending the last line with an ellipsis if cut."""
    lines = wrap(text, measure, max_w)
    if 2 <= len(lines) <= min(max_lines, 3):
        return balance(lines, measure, max_w)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    last = kept[-1]
    while last and measure(last + "\u2026") > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    kept[-1] = last.rstrip(" ,;:.") + "\u2026"
    return kept


def split_name(name):
    """Two-line break for a long name, at '&' for duos, else most balanced."""
    if " & " in name:
        a, b = name.split(" & ", 1)
        return [f"{a} &", b]
    words = name.split()
    if len(words) < 2:
        return [name]
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def name_runs(line, size):
    """(face, text, fill) runs for one name line; a closing '&' is italic and brown."""
    if line.endswith(" &"):
        return [(face("display", size), line[:-1], INK), (face("italic", size), "&", BROWN)]
    return [(face("display", size), line, INK)]


def runs_length(runs):
    return sum(f.length(text) for f, text, _ in runs)


def draw_runs(draw, xy, runs):
    x, y = xy
    for f, text, fill in runs:
        x = f.draw(draw, (x, y), text, fill)
    return x


def fit_name(name, max_w, max_size=NAME_MAX):
    """Largest size that fits: one line down to NAME_MIN_ONE_LINE, then two lines."""
    for size in range(max_size, NAME_MIN_ONE_LINE - 1, -2):
        if runs_length(name_runs(name, size)) <= max_w:
            return [name], size
    lines = split_name(name)
    for size in range(min(max_size, NAME_MAX_TWO_LINES), NAME_MIN - 1, -2):
        if all(runs_length(name_runs(line, size)) <= max_w for line in lines):
            return lines, size
    return lines, NAME_MIN


# ---------------------------------------------------------------- artwork

@lru_cache(maxsize=1)
def background():
    """Cream with a faint warm edge, like uncoated stock."""
    mask = Image.radial_gradient("L").resize((W, W)).crop((0, (W - H) // 2, W, (W + H) // 2))
    mask = mask.point(lambda v: max(0, v - 120) * 255 // 135)
    return Image.composite(Image.new("RGB", (W, H), CREAM_EDGE), Image.new("RGB", (W, H), CREAM), mask)


def paste_with_shadow(canvas, tile, xy, blur=10, offset=4, alpha=36):
    """A hairline lift under the tile, not a floating card."""
    x, y = xy
    w, h = tile.size
    pad = blur * 3
    shadow = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(shadow).rectangle([pad, pad, pad + w - 1, pad + h - 1], fill=alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(INK, (x - pad, y - pad + offset), shadow)
    canvas.paste(tile, (x, y))


@lru_cache(maxsize=None)
def logo_tile(size):
    return Image.open(LOGO).convert("RGB").crop(LOGO_CROP).resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- card chrome

def draw_label(draw, xy, text, fnt, fill):
    """Tracked capitals; each middle dot becomes a small centred disc."""
    x, y = xy
    parts = [p.strip() for p in text.split("\u00b7")]
    dot_y = y - fnt.cap_height() / 2
    for i, part in enumerate(parts):
        if i:
            cx = x + DOT_GAP + DOT_RADIUS
            draw.ellipse([cx - DOT_RADIUS, dot_y - DOT_RADIUS, cx + DOT_RADIUS, dot_y + DOT_RADIUS], fill=fill)
            x = cx + DOT_RADIUS + DOT_GAP
        x = fnt.draw(draw, (x, y), part, fill)
    return x


def draw_header(draw, eyebrow, meta=None):
    label = face("label", EYEBROW_SIZE, EYEBROW_TRACKING, LABEL_WORD_SPACE)
    draw_label(draw, (MARGIN, EYEBROW_BASE), eyebrow.upper(), label, BROWN)
    draw.rectangle([MARGIN, RULE_Y, MARGIN + COL_W, RULE_Y + 1], fill=ORANGE)
    if meta:
        ui = face("ui", META_SIZE, META_TRACKING, LABEL_WORD_SPACE)
        draw_label(draw, (MARGIN, META_BASE), meta, ui, INK_SOFT)


def draw_band(draw):
    draw.rectangle([0, BAND_TOP, W, H], fill=INK)
    ui = face("ui", BAND_SIZE)
    base = round(BAND_TOP + (BAND_H + ui.cap_height()) / 2)
    ui.draw(draw, (MARGIN, base), LISTEN_LINE, CREAM)
    ui.draw(draw, (W - MARGIN - ui.length(SITE_HOST), base), SITE_HOST, CREAM)


def headline_layout(name_lines, name_size, topic_lines, topic_size, top=NAME_TOP):
    """Baselines for each name and topic line; the name's cap-top sits at `top`."""
    name_lead = round(name_size * (0.98 if len(name_lines) > 1 else 1.02))
    topic_lead = round(topic_size * 1.28)
    gap = round(topic_size * 0.9)
    y = top + round(name_size * 0.70)
    name_ys = [y + i * name_lead for i in range(len(name_lines))]
    first_topic = name_ys[-1] + gap + topic_lead
    topic_ys = [first_topic + i * topic_lead for i in range(len(topic_lines))]
    return name_ys, topic_ys


def draw_headline(draw, name_lines, name_size, topic_lines, topic_size, top=NAME_TOP):
    name_ys, topic_ys = headline_layout(name_lines, name_size, topic_lines, topic_size, top)
    for line, y in zip(name_lines, name_ys):
        draw_runs(draw, (MARGIN - 2, y), name_runs(line, name_size))
    italic = face("italic", topic_size)
    for line, y in zip(topic_lines, topic_ys):
        italic.draw(draw, (MARGIN, y), line, INK_SOFT)


def new_canvas():
    canvas = background().copy()
    return canvas, ImageDraw.Draw(canvas, "RGBA")


def save(canvas, out_path):
    # A dithered 256-colour palette halves the file (about 220 KB -> 110 KB)
    # with no visible banding, keeping cards well under the ~300 KB size some
    # apps (WhatsApp) skip for link previews.
    paletted = canvas.convert("RGB").quantize(
        colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG
    )
    paletted.save(out_path, "PNG", optimize=True)
    return out_path


# ---------------------------------------------------------------- cards

def topic_lines_for(text, size, max_w=TOPIC_W, max_lines=2):
    """One line if it fits (never break 'Private / Equity'), else balanced lines."""
    if not text:
        return []
    italic = face("italic", size)
    if italic.length(text) <= ONE_LINE_TOPIC_W:
        return [text]
    return clamp_lines(text, italic.length, max_w, max_lines)


def render_card(ep, issue_no, out_path):
    canvas, draw = new_canvas()
    draw_header(draw, SHOW_NAME, card_meta(issue_no, ep))
    name = clean_text(ep.get("guest")) or clean_text(ep.get("title"))
    name_lines, name_size = fit_name(name, COL_W)
    topic_lines = topic_lines_for(card_topic(ep), TOPIC_SIZE)
    draw_headline(draw, name_lines, name_size, topic_lines, TOPIC_SIZE)
    paste_with_shadow(canvas, logo_tile(ART), (ART_X, ART_Y))
    draw_band(draw)
    return save(canvas, out_path)


def render_show_card(out_path):
    canvas, draw = new_canvas()
    draw_header(draw, SHOW_KICKER)
    name_lines, name_size = fit_name(SHOW_NAME, COL_W, max_size=NAME_MAX_TWO_LINES)
    topic_lines = topic_lines_for(SHOW_DECK, SHOW_DECK_SIZE, max_w=COL_W, max_lines=SHOW_DECK_LINES)
    draw_headline(draw, name_lines, name_size, topic_lines, SHOW_DECK_SIZE, top=SHOW_NAME_TOP)
    paste_with_shadow(canvas, logo_tile(ART), (ART_X, ART_Y))
    draw_band(draw)
    return save(canvas, out_path)


def main():
    check_fonts()
    OUT_DIR.mkdir(exist_ok=True)
    episodes = load_episodes()
    total = len(episodes)
    print(f"Loaded {total} episodes")

    for idx, ep in enumerate(episodes):
        # Must be seo_urls.episode_slug so the file always matches the page's
        # og:image; issue numbers follow generate_episode_pages (newest = total).
        out = OUT_DIR / f"{episode_slug(ep)}.png"
        render_card(ep, total - idx, out)
        print(f"Wrote {out.name}")

    if episodes:
        render_card(episodes[0], total, OUT_DIR / "latest.png")
        print("Wrote latest.png")
    render_show_card(OUT_DIR / "show.png")
    print("Wrote show.png")


if __name__ == "__main__":
    main()
