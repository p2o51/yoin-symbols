"""The Yoin Symbols logo.

Yoin's launcher icon is three fins that run off the edges of the tile. The Symbols logo
keeps their spines and redraws them in the language of the set: one stroke width, round
caps and round joins, on the 24-unit keyline canvas (grid, live area, keyline circle).
Like the Yoin icon, the strokes run past the tile and the edge crops them.

Three files are written to docs/:

    logo.svg        deep green tile, mint lines (the default)
    logo-light.svg  mint tile, deep green lines
    logo-mono.svg   one colour: the tile in currentColor with the lines cut out,
                    the way Yoin's themed (monochrome) icon cuts its grooves
"""
from __future__ import annotations

import re

from geom import squircle, to_d

# Spines of the three fins in Yoin's launcher foreground (1024 viewport = 108 dp).
SPINES_108 = [
    # purple fin: a wide V
    "M131.3 89 C253 108.9 354.7 178 426 242.8 C461.7 275.3 489.7 306.6 508.8 329.8 "
    "C518.4 341.4 525.7 351 530.6 357.7 C533.1 361 535 363.6 536.2 365.4 L540 367 L553 360.5 "
    "C560.5 355.4 571.3 348 584.8 339.2 C611.8 321.6 649.6 298.3 692.9 275.8 "
    "C736.2 253.3 784.9 231.5 833.6 216.7 C882.3 201.9 930.9 194.2 974 199.8",
    # pink fin: in from the left, then down
    "M-34 399 C26.08 454.85 288.37 530.2 412 560.9 C362.7 642.9 293.68 741.08 412 860",
    # navy fin: in from the right, then down
    "M1064 319 C1024.75 428.754 711.646 514.356 560 543.437 C607.788 628.239 687.306 832.475 623.08 971",
]

SIZE = 1024                      # the logo's own viewBox: the visible 72 dp of the 108 dp canvas
_VIS = 1024 * 72 / 108
_OFF = (1024 - _VIS) / 2
_K = SIZE / _VIS                 # 1.5
UNIT = SIZE / 24                 # one keyline unit
STROKE = round(1.5 * UNIT * 1.28)  # 82: the set's 1.5 stroke, a touch heavier for a tile
DEEP, MINT = "#00513A", "#A6F0CD"


def _map(d: str) -> str:
    nums = iter(float(n) for n in re.findall(r"-?\d*\.?\d+", d))
    out, toks = [], re.findall(r"[MLC]|-?\d*\.?\d+", d)
    xy = 0
    for t in toks:
        if t in "MLC":
            out.append(t)
            continue
        v = next(nums)
        v = (v - _OFF) * _K
        out.append(f"{v:.1f}".rstrip("0").rstrip("."))
        xy ^= 1
    s = " ".join(out)
    return re.sub(r"([MLC]) ", r"\1", s)


SPINES = [_map(d) for d in SPINES_108]
TILE = to_d(squircle(0, 0, SIZE, SIZE, r=0.2 * SIZE, s=0.6))


def _keylines(ink: str) -> str:
    u = UNIT
    grid = "".join(f"M{i * u:.2f} 0V{SIZE}M0 {i * u:.2f}H{SIZE}" for i in range(1, 24))
    return (
        f'<path d="{grid}" stroke="{ink}" stroke-opacity=".13" stroke-width="3"/>'
        f'<rect x="{2 * u:.2f}" y="{2 * u:.2f}" width="{20 * u:.2f}" height="{20 * u:.2f}" '
        f'stroke="{ink}" stroke-opacity=".5" stroke-width="6" stroke-dasharray="21 15"/>'
        f'<circle cx="{SIZE / 2:g}" cy="{SIZE / 2:g}" r="{8.5 * u:.2f}" '
        f'stroke="{ink}" stroke-opacity=".75" stroke-width="6.75" stroke-dasharray="27 18"/>'
    )


def _marks(ink: str) -> str:
    return (
        f'<g stroke="{ink}" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round">'
        + "".join(f'<path d="{d}"/>' for d in SPINES)
        + "</g>"
    )


def svg(variant: str = "dark", size: int | None = None, prefix: str = "ys-logo") -> str:
    """variant: dark | light | mono. prefix keeps ids unique when several logos share a page."""
    wh = f' width="{size}" height="{size}"' if size else ""
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}"{wh} fill="none">'
    if variant == "mono":
        return (
            head
            + f'<defs><mask id="{prefix}-cut" maskUnits="userSpaceOnUse" x="0" y="0" width="{SIZE}" height="{SIZE}">'
            + f'<path d="{TILE}" fill="#fff"/>{_keylines("#000")}{_marks("#000")}</mask></defs>'
            + f'<path d="{TILE}" fill="currentColor" mask="url(#{prefix}-cut)"/></svg>'
        )
    bg, ink = (DEEP, MINT) if variant == "dark" else (MINT, DEEP)
    return (
        head
        + f'<defs><clipPath id="{prefix}-tile"><path d="{TILE}"/></clipPath></defs>'
        + f'<g clip-path="url(#{prefix}-tile)"><path d="{TILE}" fill="{bg}"/>{_keylines(ink)}{_marks(ink)}</g></svg>'
    )


def build(write) -> int:
    from common import ROOT
    files = {"logo.svg": "dark", "logo-light.svg": "light", "logo-mono.svg": "mono"}
    for name, variant in files.items():
        write(ROOT / "docs" / name, svg(variant) + "\n")
    return len(files)
