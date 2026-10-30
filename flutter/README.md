# yoin_symbols

Light, rounded line icons with continuous-curvature containers for Flutter: 170 symbols on a 24 × 24 grid with a 1.5 stroke, shipped as an icon font for the `Icon` widget.

[Gallery](https://p2o51.github.io/yoin-symbols/) · [GitHub](https://github.com/p2o51/yoin-symbols) · MIT

## Install

```sh
flutter pub add yoin_symbols
```

## Use

```dart
import 'package:yoin_symbols/yoin_symbols.dart';

Icon(YoinSymbols.translate)
Icon(YoinSymbols.homeFilled, size: 28, color: Theme.of(context).colorScheme.primary)
```

Size and colour come from `Icon` and `IconTheme`, like any other icon font. Release builds tree-shake the font, so only the symbols you use ship with your app.

`YoinSymbols.all` maps every canonical name to its `IconData`, for galleries and pickers. Referencing it keeps the whole font.

## Names

One snake_case name per symbol on every platform: `home_filled` is `YoinSymbols.homeFilled` here, `YoinSymbols.HomeFilled` in Jetpack Compose and `HomeFilled` in JavaScript.

## Example

`example/` is a searchable gallery of every symbol:

```sh
cd example
flutter create --platforms=android,ios,web .
flutter run
```
