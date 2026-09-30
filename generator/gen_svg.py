"""svg/<name>.svg — the canonical, editable files (stroke-based, currentColor)."""
from common import REGISTRY, ROOT, names, svg_markup, write


def build() -> int:
    out = ROOT / "svg"
    out.mkdir(exist_ok=True)
    keep = set()
    for n in names():
        write(out / f"{n}.svg", svg_markup(REGISTRY[n], size=24, title=False) + "\n")
        keep.add(f"{n}.svg")
    for stale in out.glob("*.svg"):
        if stale.name not in keep:
            stale.unlink()
    return len(keep)
