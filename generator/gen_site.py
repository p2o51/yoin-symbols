#!/usr/bin/env python3
"""Build the gallery site (GitHub Pages) from the same sources as the packages.

    python3 generator/gen_site.py                 # writes docs/index.html
    python3 generator/gen_site.py --body out.html # also writes a body-only copy
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote

import common as C
from common import REGISTRY, svg_markup
from geom import to_d, polyline, circle  # noqa: E402

import icons_music as MU  # noqa: E402
import icons_nav as NV  # noqa: E402
import icons_devices as DV  # noqa: E402
import icons_content as CT  # noqa: E402
import logo as LOGO  # noqa: E402


def d(cmds):
    return to_d(cmds)


def layers_d(name, mode=None):
    return [to_d(l["d"]) for l in REGISTRY[name].layers if mode is None or l["mode"] == mode]


def geom():
    g = {}
    g["translate"] = dict(
        wen=[d(p) for p in MU.wen_parts()],
        latin=[d(p) for p in MU.a_parts()],
        wenC=list(MU.WEN_C),
        latinC=list(MU.A_C),
    )
    front, back, (cx, cy) = CT._library_front_back()
    g["libraryAdd"] = dict(front=d(front), back=d(back), c=[cx, cy], half=3.1,
                           check=[[cx - 3.05, cy + 0.1], [cx - 0.85, cy + 2.3], [cx + 3.2, cy - 1.75]])
    g["sparkle"] = dict(main=d(MU.sparkle_path(10.6, 13.4, 7.25)), mini=d(MU.sparkle_path(18.1, 5.9, 2.35)),
                        mainC=[10.6, 13.4], miniC=[18.1, 5.9])
    ox, oy = DV.CAST_O
    ox_dot = ox + 0.55
    g["cast"] = dict(screen=d(DV.cast_screen()), dot=d(circle(ox + 0.55, oy - 0.55, 1.1)),
                     w1=layers_d("cast")[2], w2=layers_d("cast")[3], panel=d(DV.cast_panel()), o=[ox, oy])
    g["search"] = dict(layers=layers_d("search"))
    g["refresh"] = dict(layers=layers_d("refresh"), c=[NV.REFRESH["cx"], NV.REFRESH["cy"]])
    g["download"] = dict(tray=d(DV.tray()), shaft=[[12, 3.9], [12, 14.4]],
                         head=[[7.9, 10.3], [12, 14.4], [16.1, 10.3]], check=[[7.35, 10.1], [10.6, 13.35], [16.85, 7.1]])
    g["eq"] = dict(xs=[4.5, 8.25, 12.0, 15.75, 19.5], hs=[4.6, 10.6, 15.8, 8.6, 4.0])
    l, r = MU.play_halves()
    pl, pr = MU.pause_quads()
    g["playPause"] = dict(play=[l, r], pause=[pl, pr])
    g["heart"] = d(MU.heart())
    g["shuffle"] = dict(
        crossA=[[3.8, 17.2], [10.6, 17.2], [13.2, 6.8], [20.0, 6.8]],
        crossB=[[3.8, 6.8], [10.6, 6.8], [13.2, 17.2], [20.0, 17.2]],
        parA=[[3.8, 17.2], [10.6, 17.2], [13.2, 17.2], [20.0, 17.2]],
        parB=[[3.8, 6.8], [10.6, 6.8], [13.2, 6.8], [20.0, 6.8]],
        head=3.3,
    )
    g["repeat"] = dict(loop=d(MU._repeat_loop()), headA=d(MU._head(17.9, 6.75, 1, 0, size=3.1)),
                       headB=d(MU._head(6.1, 17.25, -1, 0, size=3.1)),
                       one=d(polyline([(10.95, 10.55), (12.35, 9.8), (12.35, 14.35)])))
    pm = MU.play_mode_geometry()
    g["playMode"] = dict(
        loopA=MU.chain_floats(pm["loop_a"]), loopB=MU.chain_floats(pm["loop_b"]),
        crossA=MU.chain_floats(pm["cross_a"]), crossB=MU.chain_floats(pm["cross_b_mirror"]),
        headLoopA=pm["head_loop_a"], headLoopB=pm["head_loop_b"],
        headCrossA=pm["head_cross_a"], headCrossB=pm["head_cross_b_mirror"],
        one=pm["one"], oneC=list(pm["one_c"]), gap=pm["gap_half"],
    )
    g["chevron"] = dict(down=[[7.5, 9.9], [12, 14.4], [16.5, 9.9]], up=[[7.5, 14.1], [12, 9.6], [16.5, 14.1]])
    g["home"] = d(NV._home_path())
    g["library"] = dict(outline=layers_d("library"), filled=[
        dict(d=to_d(l["d"]), mode=l["mode"], rule=l.get("rule", "nonzero")) for l in REGISTRY["library_filled"].layers])
    g["back"] = dict(shaft=[[19.5, 12], [4.75, 12]], head=[[10.6, 6.15], [4.75, 12], [10.6, 17.85]])
    t, b = MU.skip_next_parts()
    g["skip"] = dict(tri=d(t), bar=d(b))
    g["visibility"] = dict(eye=d(NV._eye()), pupil=d(circle(12, 12, 3.1)), slash=[[4.6, 3.9], [19.4, 20.1]])
    g["recenter"] = dict(layers=layers_d("recenter"))
    g["error"] = dict(layers=layers_d("error"))
    g["send"] = dict(layers=layers_d("send"))
    g["memory"] = dict(cookie=d(CT.cookie()), heart=layers_d("memory")[1])
    g["settings"] = dict(layers=layers_d("settings"))
    # figures for the design-language section
    from geom import squircle, rrect
    from knock import around
    gap = around(MU.SHUF_A, 0.75 + 1.05)
    ring = list(gap.exterior.coords)
    gap_d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in ring) + " Z"
    shuf_inner = svg_markup(REGISTRY["shuffle"], title=False, ids=False)
    shuf_inner = shuf_inner[shuf_inner.index(">") + 1: -len("</svg>")]
    g["lang"] = dict(
        squircle=d(squircle(0.5, 0.5, 23, 23, r=7.0, s=0.6)),
        rrect=d(rrect(0.5, 0.5, 23, 23, 7.0)),
        squircleIcon=d(squircle(4, 4, 16, 16, r=4.0, s=0.6)),
        shuffleIcon=shuf_inner,
        shufA=d(MU.SHUF_A),
        shufB=d(MU.SHUF_B),
        shufGap=gap_d,
    )
    return g


def icons_meta():
    out = []
    for m in C.meta():
        ic = REGISTRY[m["name"]]
        out.append(dict(m, svg=svg_markup(ic, size=24, title=False, ids=False)))
    return out


def favicon() -> str:
    return "data:image/svg+xml," + quote(LOGO.svg("dark", prefix="fav"))


def render() -> str:
    tpl = (C.GEN / "site_template.html").read_text(encoding="utf-8")
    data = json.dumps(dict(version=C.version(), icons=icons_meta(), geom=geom()),
                      ensure_ascii=False, separators=(",", ":"))
    brand = f'<img class="logo" src="data:image/svg+xml,{quote(LOGO.svg("dark", prefix="brand"))}" width="30" height="30" alt="">'
    return tpl.replace("/*__DATA__*/null", data).replace("<!--LOGO-->", brand)


def main(argv):
    body = render()
    head, rest = body.split("<!--BODY-->", 1)
    desc = "Light, rounded line icons for Jetpack Compose, Web, Flutter and Figma."
    full = (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<link rel="icon" href="{favicon()}">\n'
        '<meta property="og:title" content="Yoin Symbols">\n'
        f'<meta property="og:description" content="{desc}">\n'
        '<meta property="og:image" content="https://p2o51.github.io/yoin-symbols/og.png">\n'
        + head + "</head>\n<body>\n" + rest + "\n</body>\n</html>\n"
    )
    C.write(C.ROOT / "docs" / "index.html", full)
    if "--body" in argv:
        out = Path(argv[argv.index("--body") + 1])
        C.write(out, body.replace("<!--BODY-->\n", ""))
    print(f"  site      docs/index.html ({len(full) // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1:])
