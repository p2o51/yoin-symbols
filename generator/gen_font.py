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
# simplification tolerance, half a font unit, as the fraction (num, den) of its square
SIMPLIFY_TOL2 = (1, 4)


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
    return unary_union([layer_geometry(l) for l in REGISTRY[name].layers])


def _polys(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, MultiPolygon):
        return list(g.geoms)
    return [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]


def _dp(pts, tol2, keep):
    """Douglas-Peucker on integer points. Exact integer maths, ties go to the lowest index."""
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy
    best, at = -1, None
    for i in range(1, len(pts) - 1):
        p = pts[i]
        cross = (p[0] - a[0]) * dy - (p[1] - a[1]) * dx
        if cross * cross > best:
            best, at = cross * cross, i
    # distance^2 > tol^2  <=>  cross^2 > tol^2 * |ab|^2  (tol^2 kept as a fraction)
    if at is not None and best * tol2[1] > tol2[0] * l2:
        _dp(pts[: at + 1], tol2, keep)
        keep.append(pts[at])
        _dp(pts[at:], tol2, keep)


def _ring(coords):
    """Font-unit integer ring: rounded, simplified and started at its smallest point.

    Simplifying after rounding, in integer arithmetic, keeps the result independent of the
    last-bit float noise that differs between platforms (libm, GEOS builds): run on float
    coordinates, near-ties on round caps resolved differently on macOS and Linux.
    """
    pts = [(round(x * SCALE), round((24 - y) * SCALE)) for x, y in coords[:-1]]
    pts = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts.pop()
    if len(pts) < 3:
        return None
    s = pts.index(min(pts))
    pts = pts[s:] + pts[:s]
    # split at the start (a hull vertex) and the point farthest from it; both always stay
    far = max(range(len(pts)), key=lambda i: ((pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2, -i))
    keep = [pts[0]]
    _dp(pts[: far + 1], SIMPLIFY_TOL2, keep)
    keep.append(pts[far])
    _dp(pts[far:] + [pts[0]], SIMPLIFY_TOL2, keep)
    return keep if len(keep) >= 3 else None


def glyph_for(name):
    rings = []
    for poly in _polys(icon_geometry(name)):
        poly = orient(poly, sign=1.0)  # CCW in y-down space -> clockwise once y is flipped
        outer = _ring(list(poly.exterior.coords))
        if outer is None:
            continue
        holes = sorted(r for r in (_ring(list(h.coords)) for h in poly.interiors) if r)
        rings.append((outer, holes))
    pen = TTGlyphPen(None)
    for outer, holes in sorted(rings):
        for ring in [outer] + holes:
            pen.moveTo(ring[0])
            for p in ring[1:]:
                pen.lineTo(p)
            pen.closePath()
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
