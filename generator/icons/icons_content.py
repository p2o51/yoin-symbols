"""Notes, memories, stats and list utilities."""
import math

from geom import *
from icons_music import bubble
from icons_nav import _pencil
from knock import around, band, cut, fill_region
from registry import F, FS, S, icon
from shapely.geometry import box
from shapely.ops import unary_union


def note_page():
    pts = [(4.25, 4.25), (19.75, 4.25), (19.75, 14.35), (14.35, 19.75), (4.25, 19.75)]
    return rounded_poly(pts, [3.0, 3.0, 0.9, 0.9, 3.0])


@icon("note", "content", "笔记", replaces=["Icons.AutoMirrored.Rounded.StickyNote2"])
def _():
    fold = rounded_polyline([(14.35, 19.75), (14.35, 14.35), (19.75, 14.35)], [0, 1.9, 0])
    return [S(note_page()), S(fold), S(line(8.1, 9.0, 15.9, 9.0)), S(line(8.1, 12.55, 12.4, 12.55))]


@icon("edit_note", "content", "编辑笔记", replaces=["Icons.Rounded.EditNote"])
def _():
    body, er = _pencil(tip=(11.95, 20.1), length=12.2, width=3.45, cone=3.0, eraser=2.55)
    return [
        S(line(4.0, 6.25, 16.0, 6.25)),
        S(line(4.0, 10.75, 13.0, 10.75)),
        S(line(4.0, 15.25, 8.6, 15.25)),
        S(body),
        S(er),
    ]


@icon("reviews", "content", "乐评 / 评论", replaces=["Icons.Rounded.Reviews"])
def _():
    # two lines of text, the second trailing off into a dot; a star this small closes up
    return [S(bubble()), S(line(7.9, 8.6, 16.1, 8.6)), S(line(7.9, 12.15, 12.0, 12.15)), F(dot_path(15.6, 12.15, 0.95))]


@icon("insights", "content", "统计 / 洞察", replaces=["Icons.Outlined.Insights"])
def _():
    chart = rounded_polyline([(3.75, 18.0), (8.7, 12.6), (12.7, 15.6), (20.25, 7.4)], [0, 1.3, 1.3, 0])
    from icons_music import sparkle_path

    return [S(chart), S(sparkle_path(7.1, 6.6, 2.75))]


@icon("explicit", "content", "Explicit 标记")
def _():
    return [
        S(squircle(4, 4, 16, 16, r=4.0, s=0.6)),
        S(polyline([(14.2, 8.1), (9.8, 8.1), (9.8, 15.9), (14.2, 15.9)])),
        S(line(9.8, 12.0, 13.6, 12.0)),
    ]


@icon("sort", "content", "排序")
def _():
    return [S(line(4.5, 7, 19.5, 7)), S(line(4.5, 12, 15, 12)), S(line(4.5, 17, 10.5, 17))]


@icon("filter", "content", "筛选")
def _():
    return [S(line(4.25, 7, 19.75, 7)), S(line(7.25, 12, 16.75, 12)), S(line(10.25, 17, 13.75, 17))]


def crescent(c1=(12.0, 12.0), r1=8.3, c2=(16.3, 7.7), r2=6.9):
    (x1, y1), (x2, y2) = c1, c2
    d = math.hypot(x2 - x1, y2 - y1)
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)
    xm = x1 + a * (x2 - x1) / d
    ym = y1 + a * (y2 - y1) / d
    p1 = (xm + h * (y2 - y1) / d, ym - h * (x2 - x1) / d)
    p2 = (xm - h * (y2 - y1) / d, ym + h * (x2 - x1) / d)
    ang = lambda c, p: math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    # outer arc of circle 1 (the long way round, away from circle 2)
    a1s, a1e = ang(c1, p1), ang(c1, p2)
    # choose sweep that avoids c2 direction
    mid_dir = ang(c1, c2)
    sweep = (a1e - a1s) % 360
    if sweep == 0:
        sweep = 360
    # test whether the clockwise sweep passes the direction of c2
    def passes(start, sw, target):
        t = (target - start) % 360
        return t < sw
    if passes(a1s, sweep, mid_dir):
        sweep = sweep - 360
    out = arc(x1, y1, r1, a1s, a1s + sweep)
    # inner arc of circle 2 back to p1 (inside circle 1)
    a2s, a2e = ang(c2, p2), ang(c2, p1)
    sw2 = (a2e - a2s) % 360
    # the inner arc must pass through the point of circle 2 closest to c1
    towards = ang(c2, c1)
    if not passes(a2s, sw2, towards):
        sw2 = sw2 - 360
    out += arc_cmds(x2, y2, r2, a2s, a2s + sw2, move=False)
    out += [Z]
    return out


@icon("sleep", "content", "睡眠定时")
def _():
    return [S(crescent())]


def _sun(cx=12.0, cy=12.0):
    # a sun: the disc and eight short rays on one radius, so the diagonals
    # read the same length as the straight ones
    rays = [S(line(*pt_on(cx, cy, 6.35, a), *pt_on(cx, cy, 8.35, a))) for a in range(0, 360, 45)]
    return [S(circle(cx, cy, 3.55))] + rays


@icon("light_mode", "content", "屏幕常亮 / 浅色", replaces=["Icons.Rounded.LightMode"])
def _():
    return _sun()


@icon("speed", "content", "播放速度")
def _():
    cx, cy, r = 12.0, 13.2, 8.2
    return [S(arc(cx, cy, r, 148, 392)), S(line(cx, cy, 15.95, 9.25)), F(circle(cx, cy, 1.45))]


def cookie(cx=12.0, cy=12.0, rm=7.85, amp=0.62, lobes=9, n=10):
    pts = []
    for i in range(lobes * n):
        th = 2 * math.pi * i / (lobes * n) - math.pi / 2
        r = rm + amp * math.cos(lobes * th)
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return smooth_closed(pts)


@icon("memory", "content", "记忆（印章）", note="收藏成为记忆时的印章态")
def _():
    from icons_music import heart

    h = scale(heart(), 0.36, cx=12, cy=12.2)
    return [S(cookie()), S(h)]


def _library_front_back():
    from icons_nav import FRONT, _library_back

    x, y, w, h = FRONT
    return squircle(x, y, w, h, r=3.3, s=0.6), _library_back(), (x + w / 2, y + h / 2)


@icon("library_add", "content", "加入资料库", note="+ → 确认中 → ✓")
def _():
    front, back, (cx, cy) = _library_front_back()
    return [S(front, id="front"), S(back, id="back"), S(line(cx, cy - 3.1, cx, cy + 3.1), id="plus-v"), S(line(cx - 3.1, cy, cx + 3.1, cy), id="plus-h")]


@icon("library_added", "content", "已加入资料库")
def _():
    front, back, (cx, cy) = _library_front_back()
    return [S(front, id="front"), S(back, id="back"), S(polyline([(cx - 3.05, cy + 0.1), (cx - 0.85, cy + 2.3), (cx + 3.2, cy - 1.75)]), id="check")]


# ---------------------------------------------------------------- copy (a sheet in front of the one it copies)

COPY_FRONT = (8.75, 8.25, 11.0, 12.5)


@icon("copy", "content", "复制", replaces=["Icons.Rounded.ContentCopy"])
def _():
    # the library's sleeve-on-stack grammar: the front sheet whole, the back
    # one only where it shows — cut a gap's width clear of the front
    x, y, w, h = COPY_FRONT
    back = squircle(4.25, 3.75, w, h, r=2.9, s=0.6)
    back = cut(back, unary_union([box(x - 1.9, y - 1.9, 30, 30)]))
    return [S(squircle(x, y, w, h, r=2.9, s=0.6)), S(back)]


# ---------------------------------------------------------------- from the Paw apps


@icon("brightness", "content", "亮度", replaces=["Icons.Rounded.BrightnessMedium"])
def _():
    # light_mode's sun with its left half filled
    half = [M(12, 8.45)] + arc_cmds(12, 12, 3.55, -90, -270, move=False) + [Z]
    return _sun() + [F(half)]


@icon("dark_mode", "content", "深色模式", replaces=["Icons.Rounded.DarkMode"])
def _():
    moon = parse_d(
        "M10.594 3.82 C6.435 4.535 3.474 8.257 3.713 12.471 C3.953 16.684 7.316 20.047 11.529 20.287 "
        "C15.743 20.526 19.465 17.565 20.18 13.406 C17.441 15.269 13.764 14.922 11.421 12.579 "
        "C9.078 10.236 8.731 6.559 10.594 3.82 Z"
    )
    star = parse_d(
        "M17.6 3.95 C17.704 5.43 18.17 5.896 19.65 6 C18.17 6.104 17.704 6.57 17.6 8.05 "
        "C17.496 6.57 17.03 6.104 15.55 6 C17.03 5.896 17.496 5.43 17.6 3.95 Z"
    )
    return [S(moon), S(star)]


@icon("palette", "content", "主题色", replaces=["Icons.Rounded.Palette"])
def _():
    board = parse_d(
        "M12 3.75 C7.444 3.75 3.75 7.444 3.75 12 C3.75 16.556 7.444 20.25 12 20.25 C13.05 20.25 13.75 19.5 13.75 18.6 "
        "C13.75 18.15 13.6 17.8 13.35 17.5 C13.1 17.2 12.95 16.85 12.95 16.45 C12.95 15.55 13.65 14.85 14.55 14.85 "
        "L16.4 14.85 C18.526 14.85 20.25 13.126 20.25 11 C20.25 6.994 16.556 3.75 12 3.75 Z"
    )
    dots = [(7.6, 12.2), (9.1, 8.4), (12.9, 7.1), (16.4, 8.9)]
    return [S(board), F(join(*(circle(x, y, 0.95) for x, y in dots)))]


@icon("image", "content", "图片", replaces=["Icons.Rounded.Image"])
def _():
    return [
        S(squircle_box(3.75, 3.75, 20.25, 20.25, 5.6)),
        S(parse_d("M4.4 16.6 L8.56 12.44 C9.146 11.854 10.096 11.854 10.682 12.44 L14.2 15.95")),
        S(parse_d("M12.85 14.6 L14.31 13.14 C14.896 12.554 15.846 12.554 16.432 13.14 L19.75 16.45")),
        S(circle(15.3, 8.6, 1.55)),
    ]


@icon("camera", "content", "截图 / 相机", replaces=["Icons.Rounded.PhotoCamera"])
def _():
    # a landscape container whose top edge rises into the viewfinder bump
    body = cut(squircle_box(3.75, 6.25, 20.25, 19.75, 4.4), box(8.6, 0, 15.4, 7))
    bump = parse_d("M8.6 6.25 L9.55 4.6 C9.8 4.17 10.25 3.9 10.75 3.9 L13.25 3.9 C13.75 3.9 14.2 4.17 14.45 4.6 L15.4 6.25")
    return [S(body + bump[1:]), S(circle(12, 12.75, 3.25))]


@icon("article", "content", "专栏 / 文章", replaces=["Icons.AutoMirrored.Rounded.Article"])
def _():
    return [
        S(squircle_box(5, 3.75, 19, 20.25, 4.8)),
        S(line(8.6, 8.6, 15.4, 8.6)),
        S(line(8.6, 12, 15.4, 12)),
        S(line(8.6, 15.4, 12.4, 15.4)),
    ]


@icon("calendar", "content", "日历", replaces=["Icons.Rounded.CalendarToday"])
def _():
    return [
        S(squircle_box(4.5, 5.5, 19.5, 19.5, 3.4)),
        S(line(4.5, 9.5, 19.5, 9.5)),
        S(line(8.5, 3.5, 8.5, 6.5)),
        S(line(15.5, 3.5, 15.5, 6.5)),
    ]


@icon("place", "content", "地点", replaces=["Icons.Rounded.Place"])
def _():
    pin = parse_d(
        "M12 20.5 C12 20.5 18.5 14.8 18.5 10 C18.5 6.41 15.59 3.5 12 3.5 C8.41 3.5 5.5 6.41 5.5 10 "
        "C5.5 14.8 12 20.5 12 20.5 Z"
    )
    return [S(pin), S(circle(12, 10, 2.25))]


@icon("waves", "content", "滚动边缘（潮线）", replaces=["Icons.Rounded.Waves"])
def _():
    wave = "c1.5 0 1.5 -1.5 3 -1.5s1.5 1.5 3 1.5s1.5 -1.5 3 -1.5s1.5 1.5 3 1.5s1.5 -1.5 3 -1.5s1.5 1.5 3 1.5"
    return [S(parse_d("M3 9.5" + wave)), S(parse_d("M3 15.5" + wave))]
