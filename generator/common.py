"""Shared helpers for the Yoin Symbols generators."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "generator"
sys.path.insert(0, str(GEN / "icons"))

from geom import to_d  # noqa: E402
from registry import ORDER, REGISTRY, svg_markup  # noqa: E402

for _m in ("icons_nav", "icons_music", "icons_devices", "icons_content"):
    importlib.import_module(_m)

GROUP_EN = {"nav": "Navigation & actions", "music": "Playback & music", "content": "Content & notes", "device": "Devices & services"}
GROUP_ZH = {"nav": "导航与通用", "music": "播放与音乐", "content": "内容与笔记", "device": "设备与服务"}

REPO_URL = "https://github.com/p2o51/yoin-symbols"
MAVEN_GROUP = "io.github.p2o51"
MAVEN_ARTIFACT = "yoin-symbols"
KOTLIN_PACKAGE = "com.gpo.yoin.symbols"
RES_PREFIX = "ic_yoin_"
# Directional symbols that flip in right-to-left layouts
# (Android autoMirror, Flutter matchTextDirection). Media controls do not flip.
MIRRORED = frozenset({"back", "chevron_left", "chevron_right", "send"})
NPM_NAME = "yoin-symbols"
PUB_NAME = "yoin_symbols"
FONT_FAMILY = "YoinSymbols"
FONT_DISPLAY = "Yoin Symbols"


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def names() -> list[str]:
    return [n for n in ORDER if REGISTRY[n].group != "lab"]


def pascal(name: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in name.split("_"))


def camel(name: str) -> str:
    p = pascal(name)
    return p[:1].lower() + p[1:]


def codepoints() -> dict[str, int]:
    """Stable private-use code points. New icons append; existing ones never move."""
    path = GEN / "codepoints.json"
    cps: dict[str, int] = json.loads(path.read_text()) if path.exists() else {}
    nxt = max(cps.values(), default=0xE000 - 1) + 1
    for n in names():
        if n not in cps:
            cps[n] = nxt
            nxt += 1
    path.write_text(json.dumps(cps, indent=1) + "\n")
    return cps


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def meta() -> list[dict]:
    cps = codepoints()
    out = []
    for n in names():
        ic = REGISTRY[n]
        out.append(
            dict(
                name=n,
                zh=ic.zh,
                group=ic.group,
                codepoint=f"{cps[n]:04X}",
                material=list(dict.fromkeys(r.split(".")[-1] for r in ic.replaces)),
            )
        )
    return out
