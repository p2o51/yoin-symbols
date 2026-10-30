# yoin-symbols

Light, rounded line icons with continuous-curvature containers: 170 symbols on a 24 × 24 grid with a 1.5 stroke, round caps and round joins. SVG strings, React components, an SVG sprite and an icon font, all from one source.

[Gallery](https://p2o51.github.io/yoin-symbols/) · [GitHub](https://github.com/p2o51/yoin-symbols) · MIT

```sh
npm i yoin-symbols
```

## SVG strings

Every symbol is a named export, so bundlers keep only what you import.

```js
import { Translate, toSvg } from 'yoin-symbols'

button.innerHTML = Translate                       // 24 × 24, currentColor
button.innerHTML = toSvg('translate', { size: 20, strokeWidth: 1.25, title: 'Translate' })
```

`toSvg(name, options)` takes `size`, `strokeWidth`, `className` and `title`. Without a title the SVG is `aria-hidden`.

## React

```jsx
import { Translate, HomeFilled } from 'yoin-symbols/react'

<Translate size={20} />
<HomeFilled className="nav-icon" title="Home" />
```

Components forward refs and pass other props to the `<svg>`. Every component also has an `…Icon` alias (`TranslateIcon`), handy for names that shadow globals such as `Error`, `Storage` or `Gamepad`.

## Sprite

```html
<svg width="24" height="24"><use href="/assets/sprite.svg#translate" /></svg>
```

Copy `node_modules/yoin-symbols/dist/sprite.svg` into your static assets. Symbol ids are the canonical snake_case names.

## Icon font

```js
import 'yoin-symbols/font/yoin-symbols.css'
```

```html
<i class="ys ys-translate"></i>
```

Code points live in the Private Use Area from U+E000 and never move between versions.

## Files

- `svg/<name>.svg`: one file per symbol
- `dist/meta.json`: names, Chinese names, groups, code points and the Material symbol each one replaces

## Names

One snake_case name per symbol on every platform: `home_filled` is `HomeFilled` in JavaScript and Kotlin, `homeFilled` in Dart, `.ys-home-filled` in CSS and `#home_filled` in the sprite.
