#!/usr/bin/env python3
"""
Export each vendored font's GPOS pair kerning to fonts/kerning.json.

generate_share_cards.py lays text out with Pillow's BASIC engine so a Mac and
the CI runner draw identical cards. BASIC never reads GPOS, where these Google
Fonts builds keep their kerning, and in Pillow 11.3 it scales legacy 'kern'
table values down by 64 (a 5px pair moves 0.08px), so a baked kern table does
not help. The generator instead places each character itself and applies the
pairs exported here.

One-off maintenance script (needs fontTools; CI does not run it). Re-run it if
the fonts change. Pairs are keyed by the two characters, values are in font
units, and only Latin text characters are included.

Run: python3 fonts/bake_kern.py
"""

import json

from pathlib import Path

from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent
FONTS = [
    FONT_DIR / "newsreader" / "Newsreader-DisplaySemiBold.ttf",
    FONT_DIR / "newsreader" / "Newsreader-DisplayMediumItalic.ttf",
    FONT_DIR / "librefranklin" / "LibreFranklin-Medium.ttf",
    FONT_DIR / "librefranklin" / "LibreFranklin-SemiBold.ttf",
]
OUT = FONT_DIR / "kerning.json"
# Printable ASCII and Latin-1 letters, plus the punctuation the cards use.
CODEPOINTS = (
    list(range(0x20, 0x7F)) + list(range(0xC0, 0x100))
    + [0x00B7, 0x2013, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0xFB01, 0xFB02]
)


def kern_lookups(gpos):
    indices = []
    for rec in gpos.FeatureList.FeatureRecord:
        if rec.FeatureTag == "kern":
            indices.extend(i for i in rec.Feature.LookupListIndex if i not in indices)
    return [gpos.LookupList.Lookup[i] for i in indices]


def subtables(lookup):
    for st in lookup.SubTable:
        yield st.ExtSubTable if lookup.LookupType == 9 else st


def x_advance(value):
    return (getattr(value, "XAdvance", 0) or 0) if value is not None else 0


def pair_value(st, left, right):
    """XAdvance for (left, right) from one PairPos subtable, or None if it does not apply."""
    if left not in st.Coverage.glyphs:
        return None
    if st.Format == 1:
        pset = st.PairSet[st.Coverage.glyphs.index(left)]
        for rec in pset.PairValueRecord:
            if rec.SecondGlyph == right:
                return x_advance(rec.Value1)
        return None
    c1 = st.ClassDef1.classDefs.get(left, 0)
    c2 = st.ClassDef2.classDefs.get(right, 0)
    return x_advance(st.Class1Record[c1].Class2Record[c2].Value1)


def collect_pairs(font):
    """{'Ta': -103, ...} for every kerned pair of characters in CODEPOINTS."""
    cmap = font.getBestCmap()
    chars = [chr(c) for c in CODEPOINTS if c in cmap]
    lookups = [lk for lk in kern_lookups(font["GPOS"].table) if lk.LookupType in (2, 9)]
    pairs = {}
    for left in chars:
        for right in chars:
            total = 0
            for lookup in lookups:
                for st in subtables(lookup):
                    value = pair_value(st, cmap[ord(left)], cmap[ord(right)])
                    if value is not None:
                        total += value
                        break  # the first applicable subtable wins within a lookup
            if total:
                pairs[left + right] = total
    return pairs


def strip_kern_table(font, path):
    """Earlier runs baked a 'kern' table into the fonts; keep them as shipped."""
    if "kern" in font:
        del font["kern"]
        font.save(path)


def main():
    data = {}
    for path in FONTS:
        font = TTFont(path)
        strip_kern_table(font, path)
        pairs = collect_pairs(font)
        data[path.name] = {"unitsPerEm": font["head"].unitsPerEm, "pairs": pairs}
        print(f"{path.name}: {len(pairs)} pairs")
    OUT.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
                   encoding="utf-8")
    print(f"Wrote {OUT.name}")


if __name__ == "__main__":
    main()
