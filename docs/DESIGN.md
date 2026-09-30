# Design

Yoin Symbols follow the visual language of Google's Luminous symbols: a thinner line, more air inside the artboard, containers with continuous curvature, small restrained details and the occasional organic curve. Every path was drawn from scratch as a stroke centre line; no outlines were copied.

The [gallery](https://p2o51.github.io/yoin-symbols/) shows every symbol and the rules below as figures; the Foundations page of the Figma file does the same.

## Measured from the reference

The reference symbols are font outlines on a 960-unit em (960 units = 24 dp, y up).

| Property | Reference | Note |
| --- | --- | --- |
| Stroke | 60 units ≈ 1.5 dp (optical size 24, weight 300) | About 25 % lighter than the 2 dp Material default |
| Caps and joins | All round | No butt caps, no sharp corners |
| Circles | Outer diameter 18.4 dp | A size smaller than Material's 20 dp |
| Square containers | Continuous curvature: in a 17 dp box only about 3 dp of each side is straight | The main difference from a plain rounded rectangle |
| Dots | 1.5 dp, the stroke width | A dot is a zero-length stroke |
| Chevrons | About 9 × 4.5 dp, 45° arms | Small and light |
| Organic curves | S-shaped shoulders, open circles | A little hand-drawn warmth is allowed |

## Rules

### Artboard and keylines

```
24 × 24 artboard
├─ 2 dp margin → 20 × 20 live area
├─ circle: centre line r 8.5 (outer edge 18.5)
├─ square container: centre line 16 × 16 (x, y ∈ [4, 20])
├─ portrait shape: centre line about 11–13 × 18
└─ landscape shape: centre line about 16.5–18.5 × 12.5–14.5
```

### Line

```svg
<path d="…" fill="none" stroke="currentColor"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

- One weight: 1.5. The set also holds together at 1.25 and 1.75 when a whole interface wants a different weight; change only `stroke-width`.
- Paths use `M`, `L`, `C` and `Z` in absolute coordinates. Arcs are converted to cubic curves, which keeps VectorDrawables simple and lets two states interpolate point by point.

### Shapes

| Shape | Helper in `generator/icons/geom.py` | Typical values |
| --- | --- | --- |
| Continuous-curvature container | `squircle(x, y, w, h, r, s)`, the Figma corner-smoothing algorithm | r 3.1–4.0, s 0.6, the bend spreads over 1.6 r |
| Rounded polygon | `rounded_poly(points, radii)`, one radius per corner | Triangle tips 0.85–1.0, roof 2.3 |
| Rounded polyline | `rounded_polyline` | Open shapes: trays, handles |
| Circle, ellipse, arc | `circle`, `ellipse`, `arc` (degrees, 0° = right, 90° = down) | |

### Details

- **Dots:** r 0.95 for information dots (slightly more than half the stroke, so they read as heavy as the line); r 1.4 for the three "more" dots.
- **Chevrons:** 9 × 4.5. Every direction is the same path rotated.
- **Crossings:** where two lines cross, the lower line breaks 1.05 on each side of the upper one (3.6 centre line to centre line). `knock.cut(path, knock.around(over, 1.8))` cuts real Bézier segments, so the gap survives every export (shuffle, visibility_off, cloud_offline, devices).
- **Filled twins:** the same centre line, filled and stroked at the same width, so the outer edge sits exactly on the outline version. Holes use even-odd (error_filled, library_filled).
- **Filled play controls:** play_filled, pause_filled and skip_*_filled are straight-edged polygons whose corners come from the 0.75 round join. Play and pause have the same number of points, so they morph into each other.
- **Right to left:** back, chevron_left, chevron_right and send flip in right-to-left layouts (Android `autoMirror`, Flutter `matchTextDirection`). Media controls keep their direction, as Material recommends.

### Colour

- SVG and web: `currentColor`.
- Compose and VectorDrawables: paths are black and take the tint of the `Icon` (`LocalContentColor`).
- Flutter: the colour of `Icon` / `IconTheme`.
- Figma: the `icon/default` variable, with light and dark modes.

## Animated parts

Symbols with moving parts keep those parts separate: an `id` in the SVG, a group with `android:name` in the VectorDrawable.

| Symbol | Parts |
| --- | --- |
| translate | `wen`, `latin` |
| shuffle | `strand-over`, `strand-under`, `head-over`, `head-under` |
| cast, cast_connected | `screen`, `wave-0` … `wave-2`, `panel` |
| download, download_done | `tray`, `shaft`, `head`, `check` |
| library_add, library_added | `front`, `back`, `plus-v`, `plus-h`, `check` |
| equalizer | `bar-0` … `bar-4` |
| sparkle | `sparkle-main`, `sparkle-mini` |
| repeat_one | `one` |

## Logo

The logo is Yoin's launcher icon translated into this set. Yoin's icon is three fins that run off the edges of the tile; the logo keeps the spine of each fin and draws it the way every symbol here is drawn: one stroke width, round caps, round joins. The strokes sit on the keyline canvas (grid, live area, keyline circle) and, like the Yoin icon, run past the tile so its edge crops them.

| File | Use |
| --- | --- |
| [`logo.svg`](logo.svg) | Default: deep green tile (#00513A), mint lines (#A6F0CD) |
| [`logo-light.svg`](logo-light.svg) | Mint tile, deep green lines |
| [`logo-mono.svg`](logo-mono.svg) | One colour: the tile in `currentColor` with the lines cut out, like Yoin's themed icon |

The logo is generated by `generator/logo.py` along with everything else. Use it whole: keep the crop, the keylines and the two tones together, and use the one-colour file where only one colour is available.

## Checklist for a new symbol

- [ ] 24 × 24, content inside the 20 × 20 live area, optically centred
- [ ] 1.5 stroke, round caps and joins; only `M L C Z`
- [ ] Square containers use `squircle(…, s=0.6)`, not a plain rounded rectangle
- [ ] Crossings cut the lower line with `knock.cut`; lines never simply overlap
- [ ] Dots r 0.95; "more" dots r 1.4
- [ ] If there is a second state (on / off, done / not done), both states use the same parts with the same number of points
- [ ] Parts that will move get an `id` or a group
- [ ] Checked at 1.25, 1.5 and 1.75, in light and dark, in the gallery
