"""Icon font (TTF + WOFF2) for Flutter's Icon widget and CSS icon-font use.

Fonts cannot stroke, so every layer is outlined with shapely at the 1.5 stroke width
(round caps / joins) and merged. 24 px = 960 font units; ascent 960, descent 0,
so a glyph fills exactly the em box — the same metrics convention as Material Icons.
"""
from __future__ import annotations

import math
import os

from fontTools.fontBuilder import FontBuilder
from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from common import FONT_DISPLAY, FONT_FAMILY, REGISTRY, codepoints, names, version
from knock import _point, _segments

UPM = 960
FONT_EPOCH = 1790726400  # 2026-09-30T00:00:00Z; override with SOURCE_DATE_EPOCH
SCALE = UPM / 24.0
HALF = 0.75  # half stroke width


def _sample(sub, n_curve=48):
    pts = [sub[0][1]]
    for seg in sub:
        steps = 1 if seg[0] == "L" else n_curve
        for i in range(1, steps + 1):
            pts.append(_point(seg, i / steps))
    return pts


def _closed(pts):
    return math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1e-6


def layer_geometry(layer):
    subs = _segments(layer["d"])
    mode = layer["mode"]
    strokes, fills = [], []
    for sub in subs:
        pts = _sample(sub)
        if mode in ("stroke", "fillstroke"):
            if len(pts) == 1 or (len(pts) == 2 and pts[0] == pts[1]):
                strokes.append(LineString([pts[0], (pts[0][0] + 1e-4, pts[0][1])]).buffer(HALF, quad_segs=16))
            else:
                strokes.append(LineString(pts).buffer(HALF, cap_style="round", join_style="round", quad_segs=16))
        if mode in ("fill", "fillstroke") and len(pts) >= 3:
            fills.append(Polygon(pts).buffer(0))
    geo = []
    if fills:
        if layer.get("rule") == "evenodd":
            acc = fills[0]
            for f in fills[1:]:
                acc = acc.symmetric_difference(f)
            geo.append(acc)
        else:
            geo.append(unary_union(fills))
    if strokes:
        geo.append(unary_union(strokes))
    return unary_union(geo) if geo else Polygon()


def icon_geometry(name):
    g = unary_union([layer_geometry(l) for l in REGISTRY[name].layers])
    return g.simplify(0.004, preserve_topology=True)


def _polys(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, MultiPolygon):
        return list(g.geoms)
    return [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]


def _draw_ring(pen, coords):
    pts = [(round(x * SCALE), round((24 - y) * SCALE)) for x, y in coords[:-1]]
    dedup = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
    if len(dedup) > 1 and dedup[0] == dedup[-1]:
        dedup.pop()
    if len(dedup) < 3:
        return
    pen.moveTo(dedup[0])
    for p in dedup[1:]:
        pen.lineTo(p)
    pen.closePath()


def glyph_for(name):
    pen = TTGlyphPen(None)
    for poly in _polys(icon_geometry(name)):
        poly = orient(poly, sign=1.0)  # CCW in y-down space -> clockwise once y is flipped
        _draw_ring(pen, list(poly.exterior.coords))
        for hole in poly.interiors:
            _draw_ring(pen, list(hole.coords))
    return pen.glyph()


def build(out_ttf, out_woff2=None):
    cps = codepoints()
    order = [".notdef", "space"] + names()
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {0x20: "space"}
    cmap.update({cps[n]: n for n in names()})
    fb.setupCharacterMap(cmap)
    glyphs = {".notdef": TTGlyphPen(None).glyph(), "space": TTGlyphPen(None).glyph()}
    for n in names():
        glyphs[n] = glyph_for(n)
    fb.setupGlyf(glyphs)
    glyf = fb.font["glyf"]
    fb.setupHorizontalMetrics({gn: (UPM, getattr(glyf[gn], "xMin", 0)) for gn in order})
    fb.setupHorizontalHeader(ascent=UPM, descent=0, lineGap=0)
    v = version()
    fb.setupNameTable(
        {
            "familyName": FONT_DISPLAY,
            "styleName": "Regular",
            "uniqueFontIdentifier": f"{FONT_FAMILY}-Regular-{v}",
            "fullName": f"{FONT_DISPLAY} Regular",
            "psName": f"{FONT_FAMILY}-Regular",
            "version": f"Version {v}",
            "licenseDescription": "MIT License",
            "licenseInfoURL": "https://opensource.org/licenses/MIT",
        }
    )
    fb.setupOS2(
        sTypoAscender=UPM, sTypoDescender=0, sTypoLineGap=0,
        usWinAscent=UPM, usWinDescent=0, achVendID="YOIN", fsType=0,
        sxHeight=UPM // 2, sCapHeight=UPM,
    )
    fb.setupPost(isFixedPitch=1)
    head = fb.font["head"]
    head.fontRevision = float(".".join(v.split(".")[:2]))
    # Fixed timestamps keep the font byte-for-byte reproducible (CI checks for drift).
    head.created = head.modified = timestampSinceEpoch(int(os.environ.get("SOURCE_DATE_EPOCH", FONT_EPOCH)))
    fb.save(str(out_ttf))
    if out_woff2:
        f = TTFont(str(out_ttf), recalcTimestamp=False)
        f.flavor = "woff2"
        f.save(str(out_woff2))
    return len(names())
