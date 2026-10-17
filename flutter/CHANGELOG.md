# Changelog

## Unreleased

- New symbol `undo` (navigation & actions, replaces `Icons.AutoMirrored.Rounded.Undo`): a hook arrow that turns back on itself, with a 9 × 4.5 chevron head. It flips in right-to-left layouts, like `back`.
- New symbol `copy` (content & notes, replaces `Icons.Rounded.ContentCopy`): a sheet in front of the one it copies, the back sheet cut a gap clear of the front — the `library` sleeve-on-stack grammar.
- New symbols `open_in_full` and `close_fullscreen` (navigation & actions, replace `Icons.Rounded.OpenInFull` / `Icons.Rounded.CloseFullscreen`): two diagonals with `launch`'s square corner head, pointing out to the corners or in to the centre.
- New symbol `light_mode` (content & notes, replaces `Icons.Rounded.LightMode`): a disc and eight short rays on one radius. Yoin uses it for keeping the screen on in Now Playing.

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
