# 设计

Yoin Symbols 沿用 Google Luminous 符号的视觉语言：更细的线、更大的留白、连续曲率的容器、克制的小细节，偶尔带一点手写感的曲线。所有路径都按描边中线从零绘制，没有复用任何轮廓。

[图库](https://p2o51.github.io/yoin-symbols/)里有全部符号和下面这些规则的示意图，Figma 文件的 Foundations 页也有同样的内容。

## 从参考里量到的数字

参考符号是字体轮廓，960 单位 = 24 dp，y 轴向上。

| 项目 | 参考 | 说明 |
| --- | --- | --- |
| 描边 | 60 单位 ≈ 1.5 dp（opsz 24 · wght 300） | 比 Material 默认的 2 dp 轻约 25 % |
| 端点 / 转角 | 全部圆头、圆角 | 没有平头和尖角 |
| 圆 | 外沿直径 18.4 dp | 比 Material 的 20 dp 小一圈 |
| 方形容器 | 连续曲率：17 dp 的方框每边直线只剩约 3 dp | 和普通圆角矩形最大的区别 |
| 小圆点 | 1.5 dp，等于描边宽 | 点是长度为零的描边 |
| V 形箭头 | 约 9 × 4.5 dp，45° 臂 | 小而轻 |
| 有机曲线 | S 形肩线、开口的圆 | 允许一点手写感 |

## 规则

### 画板与关键线

```
24 × 24 画板
├─ 2 dp 边距 → 20 × 20 关键区
├─ 圆：中线 r 8.5（外沿 18.5）
├─ 方形容器：中线 16 × 16（x, y ∈ [4, 20]）
├─ 竖长形：中线约 11–13 × 18
└─ 横长形：中线约 16.5–18.5 × 12.5–14.5
```

### 线

```svg
<path d="…" fill="none" stroke="currentColor"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

- 描边统一 1.5。整个界面想更轻或更重时只改 `stroke-width`，1.25 和 1.75 都成立。
- 路径只用绝对坐标的 `M`、`L`、`C`、`Z`。圆弧转成三次贝塞尔，VectorDrawable 更简单，两个状态也能逐点插值。

### 形状

| 形状 | `generator/icons/geom.py` 里的函数 | 常用参数 |
| --- | --- | --- |
| 连续曲率容器 | `squircle(x, y, w, h, r, s)`，即 Figma 的圆角平滑算法 | r 3.1–4.0，s 0.6，弯曲延伸到 1.6 r |
| 圆角多边形 | `rounded_poly(points, radii)`，每个角单独给半径 | 三角形顶点 0.85–1.0，房顶 2.3 |
| 圆角折线 | `rounded_polyline` | 开口形状：托盘、把手 |
| 圆、椭圆、弧 | `circle`、`ellipse`、`arc`（角度制，0° 向右，90° 向下） | |

### 细节

- **小圆点**：信息点 r 0.95（比描边一半略大，光学上才和线一样重）；“更多”的三个点 r 1.4。
- **V 形箭头**：9 × 4.5，所有方向是同一条路径旋转。
- **交叉**：两条线交叉时，下层线条在上层两侧各断开 1.05（中线到中线 3.6）。`knock.cut(path, knock.around(over, 1.8))` 切出来的是真正的贝塞尔线段，任何导出都保留缝隙（shuffle、visibility_off、cloud_offline、devices）。
- **实心版**：同一条中线，填充再加同宽描边，外沿与线框版完全重合。镂空用 even-odd（error_filled、library_filled）。
- **实心播放控件**：play_filled、pause_filled、skip_*_filled 是直边多边形，角由 0.75 的圆角连接自然形成。播放和暂停点数相同，可以互相变形。
- **从右到左**：back、chevron_left、chevron_right、send、undo 在从右到左的布局里会镜像（Android 用 `autoMirror`，Flutter 用 `matchTextDirection`）。播放控件不镜像，和 Material 的建议一致。

### 颜色

- SVG 和 Web：`currentColor`。
- Compose 和 VectorDrawable：路径是黑色，由 `Icon` 的 tint（`LocalContentColor`）上色。
- Flutter：跟随 `Icon` / `IconTheme` 的颜色。
- Figma：`icon/default` 变量，有浅色和深色两个模式。

## 动画部件

有动画部件的符号把部件分开：SVG 里有 `id`，VectorDrawable 里是带 `android:name` 的分组。

| 符号 | 部件 |
| --- | --- |
| translate | `wen`、`latin` |
| shuffle | `strand-over`、`strand-under`、`head-over`、`head-under` |
| cast、cast_connected | `screen`、`wave-0` … `wave-2`、`panel` |
| download、download_done | `tray`、`shaft`、`head`、`check` |
| library_add、library_added | `front`、`back`、`plus-v`、`plus-h`、`check` |
| equalizer | `bar-0` … `bar-4` |
| sparkle | `sparkle-main`、`sparkle-stick`、`sparkle-dot-0`、`sparkle-dot-1` |
| repeat_one | `one` |

## 标志

标志是把 Yoin 的启动器图标翻译成这套图标的语言。Yoin 的图标是三片伸出画面边缘的鳍；标志保留每片鳍的脊线，用这里每个符号都用的画法重画：同一种描边宽度、圆端点、圆转角。线条放在关键线画布上（网格、有效区、关键线圆），并像 Yoin 图标一样超出方块，被边缘裁切。

| 文件 | 用途 |
| --- | --- |
| [`logo.svg`](../logo.svg) | 默认：深绿方块（#00513A），薄荷绿线条（#A6F0CD） |
| [`logo-light.svg`](../logo-light.svg) | 薄荷绿方块，深绿线条 |
| [`logo-mono.svg`](../logo-mono.svg) | 单色：方块用 `currentColor`，线条镂空，和 Yoin 的主题图标做法一样 |

标志和其他文件一样由 `generator/logo.py` 生成。请整体使用：裁切、关键线和两种色调保持在一起；只能用一种颜色的地方用单色文件。

## 新增符号检查清单

- [ ] 24 × 24，内容在 20 × 20 关键区内，光学居中
- [ ] 描边 1.5，圆端点、圆转角；只用 `M L C Z`
- [ ] 方形容器用 `squircle(…, s=0.6)`，不用普通圆角矩形
- [ ] 交叉处用 `knock.cut` 让下层断开，不直接叠画
- [ ] 小圆点 r 0.95；“更多”r 1.4
- [ ] 有第二状态（开 / 关、完成 / 未完成）时，两态用同一组部件、同样的点数
- [ ] 要动的部件给 `id` 或分组
- [ ] 在图库里切 1.25 / 1.5 / 1.75 描边、浅色和深色都看一遍
