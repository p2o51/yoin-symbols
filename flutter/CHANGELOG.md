# Changelog

## Unreleased

- New symbol `undo` (navigation & actions, replaces `Icons.AutoMirrored.Rounded.Undo`): a hook arrow that turns back on itself, with a 9 × 4.5 chevron head. It flips in right-to-left layouts, like `back`.

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
