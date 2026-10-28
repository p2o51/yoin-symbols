# Changelog

## Unreleased

- `sparkle` and `sparkle_filled` are now a short wand with the star at its tip and two specks of light, instead of the large and small star every AI feature uses. `rememberSparkleSymbolPainter` turns the star and blinks the specks; the SVG parts are `sparkle-main`, `sparkle-stick`, `sparkle-dot-0` and `sparkle-dot-1`.
- `star` and `star_filled` are a size larger (outer radius 8.85 → 10.4), as heavy as `favorite`.
- `reviews`: the bubble holds two lines of text and a dot instead of a star that closed up at 24 px.
- `share`, `launch`, `cast` and `cast_connected` share one opening rule: where something leaves the container, one side opens wide past its corner and the other stops one wave spacing (3.95) short. `share` opens on the left, `launch` loses its top edge and top-left corner, and `cast` now leaves the same gap at both ends of the outer wave.

## 0.2.0 · 2026-10-19

- New symbol `undo` (navigation & actions, replaces `Icons.AutoMirrored.Rounded.Undo`): a hook arrow that turns back on itself, with a 9 × 4.5 chevron head. It flips in right-to-left layouts, like `back`.
- New symbol `copy` (content & notes, replaces `Icons.Rounded.ContentCopy`): a sheet in front of the one it copies, the back sheet cut a gap clear of the front — the `library` sleeve-on-stack grammar.
- New symbols `open_in_full` and `close_fullscreen` (navigation & actions, replace `Icons.Rounded.OpenInFull` / `Icons.Rounded.CloseFullscreen`): two diagonals with `launch`'s square corner head, pointing out to the corners or in to the centre.
- New symbol `light_mode` (content & notes, replaces `Icons.Rounded.LightMode`): a disc and eight short rays on one radius. Yoin uses it for keeping the screen on in Now Playing.
- `SymbolPlayMode` has a fourth mode, `ShuffleRepeatOne`, and the order is now repeat all → shuffle → shuffle + repeat one → repeat one (one change per tap); `shuffle` and `repeatOne` read the two parts. In `rememberPlayModeSymbolPainter` the 1 rides with the strands into the open wedge left of the crossing, at 0.72 scale.

## 0.1.0 · 2026-09-30

First release.

- 91 symbols in four groups: navigation & actions, playback & music, content & notes, devices & services.
- 24 × 24 grid, 1.5 stroke, round caps and joins, continuous-curvature containers, knocked-out crossings.
- Android: `YoinSymbols.*` ImageVectors, VectorDrawables (`ic_yoin_*`), and seven spring-animated symbols
  (translate, play / pause, favorite, expand, equalizer, sparkle, and a one-button play mode).
- Web: SVG strings, React components, an SVG sprite and an icon font (`yoin-symbols` on npm).
- Flutter: icon font with `YoinSymbols.*` IconData (`yoin_symbols` on pub.dev).
- Back, chevrons and send flip in right-to-left layouts on Android and Flutter.
- Figma: a component library with every symbol, Outline / Filled variants and an `icon/default` colour variable.
- A logo drawn from Yoin's launcher icon, in dark, light and one-colour versions (`docs/logo*.svg`).
