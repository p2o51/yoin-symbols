#!/usr/bin/env python3
"""Regenerate every Yoin Symbols artifact from the icon sources.

    pip install -r generator/requirements.txt
    python3 generator/build.py

Sources live in generator/icons/ (one Python function per symbol, stroke centre-lines on
a 24 x 24 grid). Outputs:

    svg/                                   canonical SVG files
    android/yoin-symbols/src/main/         VectorDrawables, YoinSymbols.kt, SymbolGeometry.kt
    web/                                   npm package (dist/, svg/, font/, package.json)
    flutter/                               pub package (lib/, fonts/, pubspec.yaml)
    docs/index.html                        gallery site (GitHub Pages)
    docs/logo*.svg                         the Yoin Symbols logo (dark, light, one colour)
    generator/codepoints.json              stable font code points (append-only)

The single version number lives in VERSION.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_android  # noqa: E402
import gen_flutter  # noqa: E402
import gen_font  # noqa: E402
import gen_site  # noqa: E402
import gen_svg  # noqa: E402
import gen_web  # noqa: E402
import logo  # noqa: E402
from common import ROOT, names, version, write  # noqa: E402


def sync_versions() -> None:
    v = version()
    props = ROOT / "android" / "gradle.properties"
    text = props.read_text(encoding="utf-8")
    props.write_text(re.sub(r"(?m)^VERSION_NAME=.*$", f"VERSION_NAME={v}", text), encoding="utf-8")


def main() -> None:
    print(f"Yoin Symbols {version()} · {len(names())} symbols")
    print(f"  svg       {gen_svg.build()} files")
    with tempfile.TemporaryDirectory() as tmp:
        ttf = Path(tmp) / "YoinSymbols.ttf"
        woff2 = Path(tmp) / "YoinSymbols.woff2"
        print(f"  font      {gen_font.build(ttf, woff2)} glyphs")
        print(f"  android   {gen_android.build()} drawables + YoinSymbols.kt")
        print(f"  web       {gen_web.build(ttf, woff2)} symbols")
        print(f"  flutter   {gen_flutter.build(ttf)} IconData")
    print(f"  logo      {logo.build(write)} files in docs/")
    gen_site.main([])
    sync_versions()


if __name__ == "__main__":
    main()
