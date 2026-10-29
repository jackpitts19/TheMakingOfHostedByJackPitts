"""
Type setting for the share cards: vendored fonts, pair kerning, and ligatures.

Pillow's BASIC layout engine is used on purpose (Raqm is present on some
installs and not others and would shift glyphs between a Mac and CI), but BASIC
ignores GPOS kerning and, in Pillow 11.3, scales legacy 'kern' values down by
64. So each character is placed here instead, using the pair kerning exported
from the fonts' GPOS tables to fonts/kerning.json by fonts/bake_kern.py.
"""

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).parent
FONT_DIR = ROOT / "fonts"
KERNING_FILE = FONT_DIR / "kerning.json"

FONT_FILES = {
    "display": FONT_DIR / "newsreader" / "Newsreader-DisplaySemiBold.ttf",
    "italic": FONT_DIR / "newsreader" / "Newsreader-DisplayMediumItalic.ttf",
    "label": FONT_DIR / "librefranklin" / "LibreFranklin-SemiBold.ttf",
    "ui": FONT_DIR / "librefranklin" / "LibreFranklin-Medium.ttf",
}
LIGATURES = (("fi", "ﬁ"), ("fl", "ﬂ"))


class MissingFontError(RuntimeError):
    pass


def check_fonts():
    required = [*FONT_FILES.values(), KERNING_FILE]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        raise MissingFontError(
            "Share-card fonts are missing: " + ", ".join(missing)
            + ". They are vendored in fonts/ (Newsreader and Libre Franklin, SIL OFL). "
            "Restore them from git rather than letting the cards fall back to a system font."
        )


@lru_cache(maxsize=None)
def font(role, size):
    check_fonts()
    return ImageFont.truetype(str(FONT_FILES[role]), size=size, layout_engine=ImageFont.Layout.BASIC)


@lru_cache(maxsize=1)
def _kerning():
    return json.loads(KERNING_FILE.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _pairs(role):
    entry = _kerning().get(FONT_FILES[role].name)
    if entry is None:
        raise MissingFontError(f"No kerning for {FONT_FILES[role].name}; re-run fonts/bake_kern.py")
    return entry["pairs"], entry["unitsPerEm"]


@dataclass(frozen=True)
class Face:
    """One font at one size, optionally letterspaced (tracking in px).

    word_space adds extra px after each space, which tracked capitals need so
    words do not close up. Ligatures are only used on untracked text.
    """

    role: str
    size: int
    tracking: float = 0
    word_space: float = 0

    @property
    def pil(self):
        return font(self.role, self.size)

    def _prepare(self, text):
        if self.tracking == 0:
            for seq, lig in LIGATURES:
                text = text.replace(seq, lig)
        return text

    def _advances(self, text):
        """(char, x offset) for each character, plus the total advance."""
        pairs, upm = _pairs(self.role)
        scale = self.size / upm
        fnt, x, prev, placed = self.pil, 0.0, None, []
        for ch in self._prepare(text):
            if prev is not None:
                x += pairs.get(prev + ch, 0) * scale + self.tracking
                if prev == " ":
                    x += self.word_space
            placed.append((ch, x))
            x += fnt.getlength(ch)
            prev = ch
        return placed, x

    def length(self, text):
        return self._advances(text)[1]

    def cap_height(self):
        return -self.pil.getbbox("H", anchor="ls")[1]

    def draw(self, draw, xy, text, fill):
        """Draw on a baseline at xy; returns the end x."""
        x0, y = xy
        placed, total = self._advances(text)
        for ch, dx in placed:
            if ch != " ":
                draw.text((x0 + dx, y), ch, font=self.pil, fill=fill, anchor="ls")
        return x0 + total


def face(role, size, tracking=0, word_space=0):
    return Face(role, size, tracking, word_space)
