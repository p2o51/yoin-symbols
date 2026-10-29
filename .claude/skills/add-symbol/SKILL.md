---
name: add-symbol
description: Add, port or change a Yoin Symbols icon. Use whenever Yoin, PiliPaw, WeiPaw, CronPaw or any other app needs an icon this set does not have, when porting an icon an app drew itself, or when refining a symbol's drawing. Apps never draw icons or copy symbol files; every icon goes through this repository.
---

# Adding a symbol

The only source is `generator/icons/`. Everything else (`svg/`, the Android library, `web/`, `flutter/`, `docs/index.html`, `generator/codepoints.json`) is generated; never edit it by hand.

## Before drawing

1. Search for an existing symbol with the same meaning: the gallery (`docs/index.html`), `web/dist/meta.json` (names, Chinese names, groups, the Material icons each replaces), `grep -n '@icon(' generator/icons/*.py`. Reuse one that means the same thing instead of adding a near-duplicate.
2. Pick the name: snake_case, after what it shows or means (`thumb_up`, `danmaku_off`), never after the screen that uses it. Filled twins end in `_filled`. Kotlin gets `YoinSymbols.PascalCase` automatically.
3. Pick the group and its module: `nav` → `icons_nav.py`, `music` → `icons_music.py`, `content` → `icons_content.py`, `device` → `icons_devices.py`, `social` (video & social) → `icons_social.py`. A new group also needs `GROUP_EN` / `GROUP_ZH` in `generator/common.py` and `GROUPS` in `generator/site_template.html`.

## Drawing

Read `docs/DESIGN.md` and two neighbouring symbols first. A symbol is a function returning layers:

```python
@icon("name", "group", "中文名", replaces=["Icons.Rounded.Material"])
def _():
    return [S(stroke_path), FS(filled_twin_path), F(dot_path)]
```

- 24 × 24; the ink (stroke outer edge) stays inside 2–22 on both axes.
- One 1.5 stroke, round caps and joins; output only `M L C Z` (the helpers guarantee it).
- Containers: `squircle(..., s=0.6)` or `squircle_box(left, top, right, bottom, reach)` (reach = 1.6 r), never a plain rounded rectangle.
- Circles `circle`, arcs `arc` (degrees, 0° right, 90° down), open shapes `rounded_polyline`.
- Free-form outlines may stay as path data via `parse_d("…")` (any SVG path, arcs and relative commands included).
- Something passing behind something else: cut the lower line with `knock.cut(path, knock.band(...))` or `knock.around(over, 1.8)`. Strokes of one object that cross (`add`, `topic`) stay joined.
- Information dots r 0.95 (filled `F(circle(...))`); "more" dots r 1.4.
- Filled twin: the same centre line with `FS`, so its outer edge equals the outline's.
- Parts that animate: give layers a `group="name"` (Kotlin group, VectorDrawable `android:name`, SVG `id`) and add them to the parts table in both DESIGN docs.
- Directional symbols that must flip right-to-left: add the name to `MIRRORED` in `generator/common.py`.
- Helpers are called when the module is imported, so define a helper above the first `@icon` that uses it.

## Porting an app's existing drawing

Export what the app shows now as the reference, not what you think its source says: a temporary JVM unit test in the app that walks each `ImageVector` (`root` → `VectorPath.pathData`) and writes SVG path data. Port it, then overlay the two (buffer strokes by 0.75, compare the ink). Keep them within 0.5 unit unless you are deliberately fixing a rule above, and list every deliberate change in the pull request. Delete the export test; never commit it.

## Build and check

```sh
pip install -r generator/requirements.txt   # Python ≥ 3.10 (shapely 2.1)
python3 generator/build.py
```

- `generator/codepoints.json` only grows; never edit or remove an entry.
- Existing symbols' `svg/*.svg` must not change unless that was the point.
- Look at every new symbol at stroke 1.25, 1.5 and 1.75, light and dark (the gallery's controls, or render the SVGs with the stroke width swapped).
- `cd android && ./gradlew :yoin-symbols:assembleRelease` (needs `android/local.properties` with `sdk.dir`).
- Add one line under `## Unreleased` in `CHANGELOG.md`; update the symbol count in both READMEs when it changes.
- Commit the source and the generated files together; CI fails if they drift.

## Using it in an app

Apps include `../yoin-symbols/android` as a composite build, so the symbol is usable as soon as the sibling checkout has it. After this repository's pull request merges, the app's CI pin (`ref:` of the `p2o51/yoin-symbols` checkout in its workflow) moves to the merged SHA. See `CONTRIBUTING.md` → "Requesting or adding a symbol from an app".

## Never

- Change `VERSION`, tag, or publish to Maven Central, npm, pub.dev or GitHub Releases. Only the owner decides on a release.
- Draw an icon inside an app, or copy `YoinSymbols.kt`, a drawable or an SVG into an app.
