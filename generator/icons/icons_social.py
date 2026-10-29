"""Video & social: reactions, comments, feeds and the video player.

Drawn first for the Paw apps (PiliPaw, WeiPaw, CronPaw) and moved here so every app
reads them from one source.
"""
from geom import *
from icons_music import bubble
from knock import band, cut
from registry import F, FS, S, icon
from shapely.geometry import box

# ---------------------------------------------------------------- reactions


def _thumb_palm(closed=False):
    # the palm and the raised thumb; the cuff sits to its left
    p = parse_d(
        "M7.75 10.6 L10.42 5.02 C10.68 4.48 11.22 4.15 11.82 4.15 C12.8 4.15 13.55 5.03 13.4 6 L12.9 9.25 "
        "L17.45 9.25 C19.05 9.25 20.22 10.76 19.83 12.31 L18.68 17.11 C18.33 18.65 16.95 19.75 15.37 19.75 L7.75 19.75"
    )
    return p + [L(7.75, 10.6), Z] if closed else p


def _thumb_cuff():
    return squircle_box(3.75, 10.6, 7.75, 19.75, 1.7)


@icon("thumb_up", "social", "点赞", replaces=["Icons.Rounded.ThumbUp"])
def _():
    return [S(_thumb_palm()), S(_thumb_cuff())]


@icon("thumb_up_filled", "social", "已点赞", replaces=["Icons.Filled.ThumbUp"])
def _():
    return [FS(_thumb_palm(closed=True)), FS(_thumb_cuff())]


@icon("thumb_down", "social", "点踩", replaces=["Icons.Rounded.ThumbDown"])
def _():
    return [S(rotate(_thumb_palm(), 180)), S(rotate(_thumb_cuff(), 180))]


@icon("thumb_down_filled", "social", "已点踩", replaces=["Icons.Filled.ThumbDown"])
def _():
    return [FS(rotate(_thumb_palm(closed=True), 180)), FS(rotate(_thumb_cuff(), 180))]


@icon("flag", "social", "举报", replaces=["Icons.Rounded.Flag"])
def _():
    pennant = parse_d(
        "M6 4.75 L17.1 4.75 C17.85 4.75 18.3 5.55 17.9 6.2 L15.95 9.4 L17.9 12.6 C18.3 13.25 17.85 14.05 17.1 14.05 L6 14.05"
    )
    return [S(line(6, 20.25, 6, 3.75)), S(pennant)]


@icon("coin", "social", "投币")
def _():
    return [S(circle(12, 12, 8.5)), S(line(8.9, 8.85, 15.1, 8.85)), S(line(12, 8.85, 12, 15.6))]


@icon("coin_filled", "social", "已投币")
def _():
    # the T is a round-capped cut-out, as wide as the outline's stroke
    t = parse_d(
        "M8.9 8.1 L15.1 8.1 A0.75 0.75 0 0 1 15.1 9.6 L12.75 9.6 L12.75 15.6 A0.75 0.75 0 0 1 11.25 15.6 "
        "L11.25 9.6 L8.9 9.6 A0.75 0.75 0 0 1 8.9 8.1 Z"
    )
    return [F(circle(12, 12, 9.25) + t, rule="evenodd")]


def _paw_parts():
    # four toe pads (the outer two tilted out) and a main pad with a soft three-lobed foot
    return [
        ("toe-0", parse_d("M3.943 12.374 A1.65 2.15 -28 1 1 6.857 10.826 A1.65 2.15 -28 1 1 3.943 12.374 Z")),
        ("toe-1", parse_d("M7.326 7.095 A1.7 2.3 -10 1 1 10.674 6.505 A1.7 2.3 -10 1 1 7.326 7.095 Z")),
        ("toe-2", parse_d("M13.326 6.505 A1.7 2.3 10 1 1 16.674 7.095 A1.7 2.3 10 1 1 13.326 6.505 Z")),
        ("toe-3", parse_d("M17.143 10.826 A1.65 2.15 28 1 1 20.057 12.374 A1.65 2.15 28 1 1 17.143 10.826 Z")),
        ("pad", parse_d(
            "M12 12.4 C14.6 12.4 17 15.1 17 17.2 C17 19 15.6 20.1 14.1 19.9 C13.2 19.8 12.7 19.4 12 19.4 "
            "C11.3 19.4 10.8 19.8 9.9 19.9 C8.4 20.1 7 19 7 17.2 C7 15.1 9.4 12.4 12 12.4 Z"
        )),
    ]


@icon("paw", "social", "赞（爪印）")
def _():
    return [S(d, group=g) for g, d in _paw_parts()]


@icon("paw_filled", "social", "已赞（爪印）")
def _():
    return [FS(d, group=g) for g, d in _paw_parts()]


# ---------------------------------------------------------------- talking


@icon("comment", "social", "评论", replaces=["Icons.AutoMirrored.Rounded.Comment"])
def _():
    return [S(bubble()), S(line(8.1, 8.9, 15.9, 8.9)), S(line(8.1, 12.1, 12.6, 12.1))]


def _tailed_bubble(x, y, w, h, tail_x, tail_y):
    """A short bubble whose bottom-left corner runs out into a tail ending at (x, tail_y)."""
    out = []
    for c in squircle(x, y, w, h, r=3.5 / 1.6, s=0.6, corners=(True, True, False, True)):
        if c[0] == "L" and abs(c[1] - x) < 1e-6 and abs(c[2] - (y + h)) < 1e-6:
            out += [L(tail_x, y + h), L(x, tail_y)]
            continue
        out.append(c)
    return out


@icon("dialogue", "social", "对话", replaces=["Icons.Rounded.Forum"])
def _():
    # two bubbles, one each side, their tails pointing out; the lower tail is a little
    # shorter so the pair fits the live area
    upper = _tailed_bubble(3.75, 2.75, 10.5, 7, 6.9, 12.25)
    lower = mirror_x(_tailed_bubble(3.75, 12.25, 10.5, 7, 6.9, 21.25))
    return [S(upper), S(lower)]


@icon("reply", "social", "回复", replaces=["Icons.AutoMirrored.Rounded.Reply"])
def _():
    return [
        S(polyline([(9.5, 6.5), (4.5, 11.5), (9.5, 16.5)])),
        S(parse_d("M4.5 11.5 L14 11.5 C17 11.5 19.5 14 19.5 17 L19.5 18")),
    ]


@icon("forward", "social", "转发", replaces=["Icons.AutoMirrored.Rounded.Forward"])
def _():
    return [S(parse_d(
        "M13.25 5.95 C13.25 5.29 14.04 4.95 14.52 5.4 L19.42 10.02 C19.97 10.54 19.97 11.41 19.42 11.93 L14.52 16.55 "
        "C14.04 17 13.25 16.66 13.25 16 L13.25 14.25 C8.85 14.25 6.05 15.45 4.4 18.55 C4.7 13.35 7.7 9.75 13.25 9.3 Z"
    ))]


@icon("at", "social", "@ 提及", replaces=["Icons.Rounded.AlternateEmail"])
def _():
    return [
        S(circle(12, 12, 3.4)),
        S(parse_d(
            "M15.4 8.9 L15.4 13.4 C15.4 14.75 16.25 15.75 17.55 15.75 C19.05 15.75 20.25 14.35 20.25 12 "
            "C20.25 7.444 16.556 3.75 12 3.75 C7.444 3.75 3.75 7.444 3.75 12 C3.75 16.556 7.444 20.25 12 20.25 "
            "C13.65 20.25 15.15 19.8 16.4 19"
        )),
    ]


@icon("topic", "social", "话题 / #", replaces=["Icons.Rounded.Tag"])
def _():
    # a slanted hash; its strokes cross like add's, without a knockout
    return [
        S(line(10, 4.25, 8.25, 19.75)),
        S(line(15.75, 4.25, 14, 19.75)),
        S(line(5, 9.25, 19.5, 9.25)),
        S(line(4.5, 14.75, 19, 14.75)),
    ]


@icon("emoji", "social", "表情", replaces=["Icons.Rounded.EmojiEmotions"])
def _():
    return [
        S(circle(12, 12, 8.5)),
        S(parse_d("M8.6 14.1 C9.35 15.45 10.6 16.25 12 16.25 C13.4 16.25 14.65 15.45 15.4 14.1")),
        S(line(9.25, 9.6, 9.25, 10.4)),
        S(line(14.75, 9.6, 14.75, 10.4)),
    ]


@icon("mail", "social", "私信", replaces=["Icons.Rounded.Mail"])
def _():
    return [
        S(squircle_box(3.75, 5.25, 20.25, 18.75, 5.0)),
        S(parse_d("M7.4 9.2 L10.95 12.05 C11.564 12.543 12.436 12.543 13.05 12.05 L16.6 9.2")),
    ]


# ---------------------------------------------------------------- people & feeds


def _person_side():
    # person's head and shoulders, moved left to make room for a badge
    return [ellipse(10.2, 8.1, 3.3, 3.55), parse_d("M3.8 19.9 C3.8 16.7 6.6 14.9 10.2 14.9 C11.35 14.9 12.45 15.1 13.4 15.45")]


@icon("person_add", "social", "关注", replaces=["Icons.Rounded.PersonAdd"])
def _():
    head, shoulders = _person_side()
    return [S(head), S(shoulders), S(line(18.25, 13.75, 18.25, 19.75)), S(line(15.25, 16.75, 21.25, 16.75))]


@icon("person_check", "social", "已关注")
def _():
    head, shoulders = _person_side()
    return [S(head), S(shoulders), S(polyline([(15.1, 16.95), (16.95, 18.8), (20.75, 15)]))]


def _quiet_lids():
    # a lowered eye: the almond sits high, three short lashes fall from its lower lid
    return parse_d(
        "M3.75 10.6 C5.9 7.55 8.7 6 12 6 C15.3 6 18.1 7.55 20.25 10.6 C18.1 13.65 15.3 15.2 12 15.2 "
        "C8.7 15.2 5.9 13.65 3.75 10.6 Z"
    )


def _quiet_lashes():
    return [S(line(7.9, 16.9, 7.1, 18.6)), S(line(12, 17.6, 12, 19.4)), S(line(16.1, 16.9, 16.9, 18.6))]


@icon("quiet_eye", "social", "悄悄关注")
def _():
    return [S(_quiet_lids()), S(circle(12, 10.6, 2.5))] + _quiet_lashes()


@icon("quiet_eye_filled", "social", "悄悄关注中")
def _():
    return [S(_quiet_lids()), FS(circle(12, 10.6, 2.5))] + _quiet_lashes()


@icon("channel", "social", "频道")
def _():
    # three stacked streams merging into one
    return [
        S(line(4.75, 6.75, 13.25, 6.75)),
        S(line(4.75, 12, 11.25, 12)),
        S(line(4.75, 17.25, 13.25, 17.25)),
        S(parse_d("M16.25 6.75 C18.6 6.75 19.25 8.4 19.25 12 C19.25 15.6 18.6 17.25 16.25 17.25")),
        S(line(14.25, 12, 19.25, 12)),
    ]


@icon("dynamic", "social", "动态", replaces=["Icons.Rounded.Explore"])
def _():
    return [S(circle(12, 12, 8.5)), S(polyline([(15.6, 8.4), (13.55, 13.55), (8.4, 15.6), (10.45, 10.45)], closed=True))]


@icon("dynamic_filled", "social", "动态（选中）", replaces=["Icons.Filled.Explore"])
def _():
    needle = polyline([(16.25, 7.75), (10.05, 10.05), (7.75, 16.25), (13.95, 13.95)], closed=True)
    return [F(circle(12, 12, 9.25) + needle, rule="evenodd")]


FLAME = (
    "M12 20.5 C8.41 20.5 5.75 17.93 5.75 14.6 C5.75 11.6 7.7 9.6 9.25 7.75 C10.25 6.55 10.85 5.2 10.95 3.75 "
    "C13.9 5.35 15.95 8.1 16.2 11.05 C16.75 10.5 17.1 9.8 17.25 9.05 C18.2 10.4 18.25 12.5 18.25 14.6 "
    "C18.25 17.93 15.59 20.5 12 20.5 Z"
)


@icon("fire", "social", "热门", replaces=["Icons.Rounded.LocalFireDepartment"])
def _():
    inner = "M12 20.5 C10.62 20.5 9.55 19.48 9.55 18.15 C9.55 16.62 10.95 15.72 11.55 14.05 C13.35 15.05 14.45 16.5 14.45 18.15 C14.45 19.48 13.38 20.5 12 20.5"
    return [S(parse_d(FLAME)), S(parse_d(inner))]


def _trophy():
    cup = parse_d("M7.25 4.25 L16.75 4.25 L16.75 9.75 C16.75 12.373 14.623 14.5 12 14.5 C9.377 14.5 7.25 12.373 7.25 9.75 Z")
    handles = [
        parse_d("M7.25 6.25 L5.6 6.25 C4.6 6.25 3.9 7.05 4.05 8.05 C4.35 9.95 5.6 11.2 7.55 11.45"),
        parse_d("M16.75 6.25 L18.4 6.25 C19.4 6.25 20.1 7.05 19.95 8.05 C19.65 9.95 18.4 11.2 16.45 11.45"),
    ]
    return cup, handles, line(12, 14.5, 12, 17.25), squircle_box(8.25, 17.25, 15.75, 19.75, 1.25)


@icon("trophy", "social", "排行榜", replaces=["Icons.Rounded.EmojiEvents"])
def _():
    cup, handles, stem, base = _trophy()
    return [S(cup)] + [S(h) for h in handles] + [S(stem), S(base)]


@icon("trophy_filled", "social", "排行榜（选中）", replaces=["Icons.Filled.EmojiEvents"])
def _():
    cup, handles, stem, base = _trophy()
    return [FS(cup)] + [S(h) for h in handles] + [S(stem), FS(base)]


@icon("gift", "social", "礼物 / 充电", replaces=["Icons.Rounded.CardGiftcard"])
def _():
    lid = squircle_box(3.75, 8.25, 20.25, 12, 1.6)
    # the box below the lid: a container whose top edge and corners are cut away
    body = cut(squircle_box(5.25, 4, 18.75, 20.25, 3.6), box(-1, -1, 30, 12))
    bow = parse_d(
        "M12 8.25 C10.4 8.25 8.25 7.65 8.25 6 C8.25 4.95 9 4.25 9.95 4.25 C11.2 4.25 11.8 5.6 12 8.25 "
        "C12.2 5.6 12.8 4.25 14.05 4.25 C15 4.25 15.75 4.95 15.75 6 C15.75 7.65 13.6 8.25 12 8.25 Z"
    )
    return [S(lid), S(body), S(line(12, 8.25, 12, 20.25)), S(bow)]


@icon("poll", "social", "投票", replaces=["Icons.Rounded.Poll"])
def _():
    # three options of different lengths
    return [S(line(5.25, 7, 18.75, 7)), S(line(5.25, 12, 12.75, 12)), S(line(5.25, 17, 15.75, 17))]


# ---------------------------------------------------------------- video


def screen():
    """The landscape frame that danmaku, subtitles, hd and pip share."""
    return squircle_box(3.25, 4.75, 20.75, 19.25, 5.0)


@icon("live", "social", "直播", replaces=["Icons.Rounded.Sensors"])
def _():
    return [
        S(circle(12, 12, 1.75)),
        S(arc(12, 12, 4.6, -45, 45)),
        S(arc(12, 12, 4.6, 225, 135)),
        S(arc(12, 12, 8.25, -45, 45)),
        S(arc(12, 12, 8.25, 225, 135)),
    ]


@icon("views", "social", "播放量")
def _():
    # play_circle's triangle on a screen standing on a short bar
    tri = rounded_poly([(10.05, 7.95), (16.55, 12.0), (10.05, 16.05)], [0.75, 0.85, 0.75])
    return [S(squircle_box(3.25, 4.25, 20.75, 16.75, 4.9)), S(translate(tri, -0.1, -1.5)), S(line(8.75, 20, 15.25, 20))]


@icon("video", "social", "视频", replaces=["Icons.Rounded.Videocam"])
def _():
    lens = parse_d(
        "M15.75 10.35 L19.32 8.27 C19.92 7.92 20.75 8.35 20.75 9.07 L20.75 14.93 C20.75 15.65 19.92 16.08 19.32 15.73 L15.75 13.65"
    )
    return [S(squircle_box(3.25, 6, 15.75, 18, 4.5)), S(lens)]


@icon("danmaku", "social", "弹幕")
def _():
    return [
        S(screen()),
        S(line(7.6, 9.6, 12.4, 9.6)),
        S(line(14.6, 9.6, 16.4, 9.6)),
        S(line(7.6, 14.4, 9.4, 14.4)),
        S(line(11.6, 14.4, 16.4, 14.4)),
    ]


@icon("danmaku_off", "social", "弹幕关")
def _():
    # visibility_off's slash and gap
    slash = (4.6, 3.9, 19.4, 20.1)
    gap = band(*slash, 0.75 + 1.1, extend=0.0)
    return [S(cut(screen(), gap)), S(line(12.1, 9.6, 16.4, 9.6)), S(line(7.6, 14.4, 11.4, 14.4)), S(line(*slash))]


@icon("danmaku_top", "social", "顶部弹幕")
def _():
    return [S(screen()), S(line(8.6, 9.4, 15.4, 9.4)), S(line(10.4, 12.6, 13.6, 12.6))]


@icon("danmaku_bottom", "social", "底部弹幕")
def _():
    return [S(screen()), S(line(10.4, 11.4, 13.6, 11.4)), S(line(8.6, 14.6, 15.4, 14.6))]


@icon("danmaku_scroll", "social", "滚动弹幕")
def _():
    return [S(screen()), S(line(10.6, 12, 16.4, 12)), S(polyline([(9.3, 9.9), (7.2, 12), (9.3, 14.1)]))]


@icon("subtitles", "social", "字幕", replaces=["Icons.Rounded.Subtitles"])
def _():
    return [
        S(screen()),
        S(line(7.6, 12.6, 10.2, 12.6)),
        S(line(12.4, 12.6, 16.4, 12.6)),
        S(line(7.6, 15.4, 13.2, 15.4)),
        S(line(15.4, 15.4, 16.4, 15.4)),
    ]


@icon("hd", "social", "画质", replaces=["Icons.Rounded.Hd"])
def _():
    return [
        S(screen()),
        S(line(7.4, 9.3, 7.4, 14.7)),
        S(line(10.6, 9.3, 10.6, 14.7)),
        S(line(7.4, 12, 10.6, 12)),
        S(parse_d("M13.3 9.3 L13.3 14.7 L14.6 14.7 C16.091 14.7 17.1 13.6 17.1 12 C17.1 10.4 16.091 9.3 14.6 9.3 Z")),
    ]


@icon("pip", "social", "画中画", replaces=["Icons.Rounded.PictureInPicture"])
def _():
    return [S(screen()), FS(squircle_box(12.6, 11.9, 16.9, 15.4, 1.3))]


def _bracket(x0, y0, x1, y1, r=2.85):
    """One corner of a frame: from (x0, y0) to the corner, then on to (x1, y1)."""
    return rounded_polyline([(x0, y0), (x0, y1), (x1, y1)], [0, r, 0])


@icon("fullscreen", "social", "全屏", replaces=["Icons.Rounded.Fullscreen"])
def _():
    corner = _bracket(4.75, 9.25, 9.25, 4.75)
    return [S(rotate(corner, a)) for a in (0, 90, 180, 270)]


@icon("fullscreen_exit", "social", "退出全屏", replaces=["Icons.Rounded.FullscreenExit"])
def _():
    corner = _bracket(9.25, 4.75, 4.75, 9.25)
    return [S(rotate(corner, a)) for a in (0, 90, 180, 270)]


@icon("replay", "social", "重播", replaces=["Icons.Rounded.Replay"])
def _():
    loop = arc(12, 12.5, 6.75, 180, -90) + [L(8.6, 5.75)]
    return [S(loop), S(polyline([(11, 3.35), (8.6, 5.75), (11, 8.15)]))]


@icon("watch_later", "social", "稍后再看", replaces=["Icons.Rounded.WatchLater"])
def _():
    return [S(circle(12, 12, 8.5)), S(polyline([(12, 7.6), (12, 12), (14.9, 13.8)]))]
