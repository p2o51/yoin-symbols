# Yoin Symbols

![Yoin Symbols](docs/cover.png)

Light, rounded line icons with continuous-curvature containers. 91 symbols drawn for the music player Yoin, packaged for Jetpack Compose, the web, Flutter and Figma from a single source.

[Gallery](https://p2o51.github.io/yoin-symbols/) · [Figma](https://www.figma.com/design/g0H4CfkagF8p1N4vuPYxQA) · [npm](https://www.npmjs.com/package/yoin-symbols) · [pub.dev](https://pub.dev/packages/yoin_symbols) · [Maven Central](https://central.sonatype.com/artifact/io.github.p2o51/yoin-symbols) · [中文](README.zh-CN.md)

| Platform | Package | Install |
| --- | --- | --- |
| Jetpack Compose, Android views | `io.github.p2o51:yoin-symbols` | `implementation("io.github.p2o51:yoin-symbols:0.1.0")` |
| Web, React | `yoin-symbols` | `npm i yoin-symbols` |
| Flutter | `yoin_symbols` | `flutter pub add yoin_symbols` |
| Figma | Yoin Symbols library | Duplicate the file, or enable the published library |
| Anything else | [`svg/`](svg) | Copy the files |

- 24 × 24 grid, 1.5 stroke, round caps and round joins
- Continuous-curvature containers (corner smoothing 60 %)
- Crossing lines leave a real gap in the path, not a mask
- Ten symbols have a filled twin with the same outer edge
- Seven symbols animate in Compose, on Material 3 Expressive springs

## Jetpack Compose

```kotlin
dependencies {
    implementation("io.github.p2o51:yoin-symbols:0.1.0")
}
```

```kotlin
import com.gpo.yoin.symbols.YoinSymbols

Icon(YoinSymbols.Translate, contentDescription = "Translate")
Icon(YoinSymbols.HomeFilled, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
```

Every symbol is an `ImageVector`, built lazily on first use. `YoinSymbolCatalog.all` maps every name to a function that returns its symbol, for pickers and galleries. Outside Compose, the same symbols are VectorDrawables: `com.gpo.yoin.symbols.R.drawable.ic_yoin_translate`.

### Animated symbols

These return a `Painter`, so they drop into any `Icon` and take its tint.

| Function | What moves |
| --- | --- |
| `rememberTranslateSymbolPainter(translating)` | 文 and A orbit and swap places while waiting, and always come to rest as 文A |
| `rememberPlayPauseSymbolPainter(playing)` | The triangle splits into the two pause bars |
| `rememberFavoriteSymbolPainter(favorite)` | One heartbeat, then the fill grows from the centre |
| `rememberExpandSymbolPainter(expanded)` | The chevron flattens and folds over like a hinge |
| `rememberEqualizerSymbolPainter(playing)` | Bars follow random levels, then sink into dots on a slow spring |
| `rememberSparkleSymbolPainter(generating, filled)` | The star turns a quarter at a time, the small star blinks off-beat |
| `rememberPlayModeSymbolPainter(mode)` | One play-mode button: repeat all → shuffle → repeat one. The loop is cut open and its lower half turns over into the crossing strand; the 1 pops in for repeat one |

```kotlin
Icon(
    painter = rememberTranslateSymbolPainter(translating = uiState.isTranslating),
    contentDescription = if (uiState.isTranslating) "Translating" else "Translate",
)
```

Loops finish their current beat before they stop, so a symbol never freezes halfway. When the system animator scale is 0, they stay still. To follow a reduced-motion setting of your own, provide the reduced springs:

```kotlin
CompositionLocalProvider(LocalSymbolMotion provides SymbolMotion.Reduced) {
    // loops become an opacity breath, morphs lose their overshoot
}
```

For the play-mode button, `SymbolPlayMode.next()` gives the mode after a tap. With Media3 the three modes map to `REPEAT_MODE_ALL`, `REPEAT_MODE_ALL` with `shuffleModeEnabled`, and `REPEAT_MODE_ONE`:

```kotlin
var mode by rememberSaveable { mutableStateOf(SymbolPlayMode.RepeatAll) }
IconButton(onClick = { mode = mode.next() }) {
    Icon(rememberPlayModeSymbolPainter(mode), contentDescription = "Play mode")
}
```

`SymbolMotion` holds every spring, so an app with its own motion scheme can pass its own values: `SymbolMotion.Default.copy(spatial = mySpring)`.

## Web

```js
import { Translate, toSvg } from 'yoin-symbols'           // SVG strings, tree-shakeable
el.innerHTML = toSvg('translate', { size: 20, title: 'Translate' })

import { Translate } from 'yoin-symbols/react'           // React components
<Translate size={20} strokeWidth={1.25} />

import 'yoin-symbols/font/yoin-symbols.css'               // icon font
<i class="ys ys-translate"></i>
```

There is also an SVG sprite (`yoin-symbols/sprite.svg`, ids are the snake_case names) and `meta.json` with every name, group and code point. See [web/README.md](web/README.md).

## Flutter

```dart
import 'package:yoin_symbols/yoin_symbols.dart';

Icon(YoinSymbols.translate)
```

An icon font, so size and colour follow `Icon` and `IconTheme`, and release builds keep only the glyphs you use. See [flutter/README.md](flutter/README.md).

## Figma

The [Figma file](https://www.figma.com/design/g0H4CfkagF8p1N4vuPYxQA) has every symbol as a component with real 1.5 strokes bound to an `icon/default` colour variable (light and dark modes). Filled twins are one component with a `Style = Outline / Filled` property. Duplicate it, or publish it as a team library. The Foundations page documents the grid and rules.

## Names

Each symbol has one snake_case name. Every platform derives its own form from it:

| Canonical | Compose | Android resource | JavaScript, React | Flutter | CSS |
| --- | --- | --- | --- | --- | --- |
| `home_filled` | `YoinSymbols.HomeFilled` | `ic_yoin_home_filled` | `HomeFilled` | `YoinSymbols.homeFilled` | `.ys-home-filled` |

Font code points start at U+E000 and are append-only: a symbol keeps its code point forever. `web/dist/meta.json` lists the Material symbol each one replaces, which helps when migrating from Material icons.

## Using a local checkout

Before a release is on Maven Central, or while you are changing symbols, point your apps at a clone.

**Android, any version of AGP.** Publish to your local Maven repository:

```sh
cd android && ./gradlew :yoin-symbols:publishToMavenLocal
```

```kotlin
// settings.gradle.kts of the app
dependencyResolutionManagement {
    repositories {
        mavenLocal { content { includeGroup("io.github.p2o51") } }
        google()
        mavenCentral()
    }
}
```

**Android, live edits.** A composite build swaps the dependency for the source. It works best when the app and this project use the same Android Gradle Plugin version (9.1 here):

```kotlin
// settings.gradle.kts of the app
val yoinSymbols = file("../yoin-symbols/android")
if (yoinSymbols.exists()) includeBuild(yoinSymbols)
```

**Web.** `npm i ../yoin-symbols/web`

**Flutter.**

```yaml
dependencies:
  yoin_symbols:
    path: ../yoin-symbols/flutter
```

## Repository

```
generator/          source of truth: one Python function per symbol, plus the generators
  icons/            geometry kit and the symbols (icons_nav.py, icons_music.py, …)
  build.py          regenerates everything below
svg/                canonical SVG files
android/            Compose library: generated ImageVectors and drawables, hand-written motion
web/                npm package
flutter/            pub package and example gallery
docs/               gallery site (GitHub Pages), design and motion notes
```

```sh
pip install -r generator/requirements.txt
python3 generator/build.py
```

Generated files are committed; CI fails if they drift from the source. See [CONTRIBUTING.md](CONTRIBUTING.md) to add a symbol and [RELEASING.md](RELEASING.md) to publish.

Design notes: [docs/DESIGN.md](docs/DESIGN.md) · [docs/MOTION.md](docs/MOTION.md)

## License

MIT. The symbols are original drawings. Their design language was studied from Google's Luminous symbols; no outlines were copied.
