# Motion

Every motion below can be tried in the [gallery](https://p2o51.github.io/yoin-symbols/#motion), slowed down or switched to its reduced version. Seven of them ship in the Compose library; the rest are specified here and prototyped in the gallery, ready to be built on any platform.

## Principles

1. **A state change is the same lines moving.** The triangle becomes the pause bars, the arrow becomes a check, parallel lines become a crossing. Points interpolate; two pictures never cross-fade.
2. **While waiting, the symbol does the work.** Translating, searching, connecting, generating: the button keeps its size and the symbol performs an action that fits its meaning, instead of turning into a spinner.
3. **Loops have a rest.** Each beat is one spring followed by 0.2–0.4 s of stillness, and the loop only checks whether it is done during the rest. A symbol always stops in a tidy pose, never halfway.
4. **Movement uses spatial springs, colour uses effects springs.** Symbol-sized movement (1–3 dp) uses the fast spatial spring; opacity, fill and colour use effects springs, which never overshoot.
5. **Resonance at the end.** Pausing, disconnecting and cancelling end on a slow, critically damped decay instead of a cut. Yoin is Japanese for the resonance that lingers after a sound; this is the signature of the set.

## Springs

The values follow the Material 3 Expressive motion scheme. `SymbolMotion` in the Compose library holds them.

| Name | `SymbolMotion` | Damping ratio / stiffness |
| --- | --- | --- |
| Expressive fast spatial | `fastSpatial` | 0.6 / 800 |
| Expressive default spatial | `spatial` | 0.8 / 380 |
| Standard fast spatial | `control` | 0.9 / 1400 |
| Standard default spatial | | 0.9 / 700 |
| Fast / default / slow effects | `effects` = default, `slowEffects` = slow | 1.0 / 3800 · 1600 · 800 |
| Resonance (Yoin) | `resonance` | 1.0 / 60 |
| Shake (Yoin, failure) | | 0.28 / 900 |

## Translate: 文 and A swap places

**While translating.** 文 and A stay upright and each travels half a turn around the same circle (radius about 5.3, centred on the symbol), swapping places. Halfway round, the glyph passing the upper right grows to 1.08 and the one passing the lower left shrinks to 0.86 and fades to about 0.6, like two cards passing in front of each other, so they never collide. Each swap uses the Expressive default spatial spring, then rests for 0.32 s.

**When it finishes.** The current half turn completes. If the glyphs are left swapped (A top-left), they take one more half turn. The symbol always comes to rest as 文A.

**On failure (prototype).** After returning to 文A the symbol shakes twice with the shake spring.

**Reduced motion.** The glyphs stay put and breathe between 42 % and 100 % opacity on the slow effects spring, ending at 100 %.

Tip: keep the translate button fully emphasised while it works and disable only its neighbours, or the disabled opacity dims the animation.

## Play mode: one button

Shuffle and repeat live on one button, as in Spotoolfy: each tap moves repeat all → shuffle → repeat one → repeat all (Spotoolfy calls repeat all "sequential"). The loop halves of repeat and the two strands of shuffle are drawn as matching chains of seven cubic segments, so the change is the same lines moving: the upper half of the loop swings its tail down into the rising strand, the lower half turns over (a horizontal flip about the centre) into the falling strand, and the falling strand's gap opens under the rising one as it lands. Going back to the loop, the 1 of repeat one pops in 140 ms after the strands start, so it lands in a finished loop.

## Catalogue

| # | Motion | Where it fits | What moves | Springs | Reduced motion | Compose |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Translate, waiting | Translate button | See above | E default + 0.32 s rest | Opacity breath | `rememberTranslateSymbolPainter` |
| 2 | Add to library, waiting for confirmation | Library + button, server confirms later | The vertical bar retracts and the horizontal bar shrinks to a dot while an arc turns inside the card; on confirmation the dot unfolds into a check with a small bounce; on failure back to + with a shake | Morph E fast; arc fast / slow effects | Arc breathes instead of turning; check appears directly | |
| 3 | AI generating | Generate, summarise, suggest | The large star turns 90° and rests; the small star blinks off-beat; when done both fill and bloom slightly | Rotation E default; fill default effects | Opacity breath; fill appears directly | `rememberSparkleSymbolPainter` |
| 4 | Casting, connecting | Cast button | The dot, inner arc and outer arc light up in turn and pop outward; once connected the panel grows from the lower left (cast_connected) | Light default effects; pop E fast; panel E default | Opacity only | |
| 5 | Searching | Search panel | The magnifier looks around between three positions; when results arrive it returns and zooms slightly | E default + 0.16 s rest | Opacity breath | |
| 6 | Rescanning | Refresh | One full turn per beat, then a rest; always stops at a full turn | E default + 0.22 s rest | Opacity breath | |
| 7 | Download → downloaded | Offline download | The arrow nods while downloading; when done the shaft retracts and the arrowhead's three points become the check | E fast | Direct swap | |
| 8 | Now playing | Current row, mini player | Bars chase random levels (or real audio levels); when paused they sink into dots from the edges inward | Bars E fast; decay resonance | Still bars, dimmed to 45 % when paused | `rememberEqualizerSymbolPainter` |
| 9 | Play ↔ pause | Play button, mini player | The triangle splits into two halves, each becoming a pause bar; no rotation | S fast | Same (the travel is tiny) | `rememberPlayPauseSymbolPainter` |
| 10 | Favorite | Heart button, track rows | The outline beats once (0.8 → 1), the fill grows from the centre, six dots burst out; unfavoriting only shrinks the fill | E fast; dots slow effects | Fill fades in and out | `rememberFavoriteSymbolPainter` (no dots) |
| 11 | Play mode, one button | Playback controls | One button cycles repeat all → shuffle → repeat one. Repeat all → shuffle: the loop is cut open, the upper half swings into the rising strand and the lower half turns over like a card and passes underneath, its gap opening as it lands. Shuffle → repeat one: the strands turn back into the loop and the 1 pops in after them. Repeat one → repeat all: the 1 shrinks away and both arrows nudge along their direction | Cut and turn E default; 1 and nudge E fast | Fade out, change, fade in | `rememberPlayModeSymbolPainter` |
| 12 | Expand / collapse | Collapsible rows, menus | The chevron flattens and folds over like a hinge instead of rotating | E default | S fast spatial | `rememberExpandSymbolPainter` |
| 13 | Navigation selected | Bottom bar, nav rail | The fill rises from the bottom while the item widens, with a small press and bounce | Fill S fast; bounce E fast; width S default | Fill fades in | |
| 14 | Predictive back | Back arrows | Gesture progress (through the back-gesture easing) shortens the shaft and moves the head left; commit slides it out, cancel springs back | Gesture-driven; commit E fast; cancel S default | Shaft shortens only | |
| 15 | Previous / next | Playback controls | The triangle pushes toward the skip direction and bounces back | E fast impulse | No movement | |
| 16 | Show / hide | Password and token fields | The slash draws from top left to bottom right as the eye narrows; the outline under the slash breaks as it passes | S default | Slash appears directly | |
| 17 | Back to the current line | Lyrics | Both arrows close in on the centre line and spring apart; the line flashes | E fast impulse; slow effects | Line flashes only | |
| 18 | Error | Error badge, failed connection | The exclamation mark shakes twice, only at the moment of failure | Shake | Colour change only | |
| 19 | Send | Send button | The paper plane flies out to the upper right and returns from the lower left | E fast / E default | Fade out and in | |
| 20 | Memory stamp | Saving something as a memory | The stamp turns upright and presses down; the heart pops in after it | E fast | Appears directly | |
| 21 | Settings | Settings entry | Each tap turns the gear one tooth (45°) | E default | No rotation | |

E = Expressive, S = Standard.

## Implementation notes (Compose)

- Each animated symbol is a `@Composable` that returns a `Painter` built with `rememberVectorPainter { Group { Path } }` and driven by `Animatable`. Static symbols stay `ImageVector`s.
- Loops live in one long-running `LaunchedEffect` that reads the latest state through `rememberUpdatedState`, so a state change never cuts a half turn short.
- Loops check `MotionDurationScale`: at an animator scale of 0 every animation would finish on the next frame, so the loop stops and the symbol stays still instead of flickering.
- Two-state morphs need both states to have the same number of points. In this set play_filled and pause_filled, download and download_done, library_add and library_added, the chevrons, and the repeat and shuffle strands (as seven-segment chains in `SymbolGeometry`) are drawn that way.
