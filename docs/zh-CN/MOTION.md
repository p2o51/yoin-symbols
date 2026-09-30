# 动效

下面每个动效都能在[图库](https://p2o51.github.io/yoin-symbols/#motion)里点着试，可以慢放，也可以切到减弱动效的版本。其中 7 个已经在 Compose 库里；其余的在这里写成规格、在图库里有原型，任何平台都可以照着实现。

## 原则

1. **状态是同一组线条的变形。** 三角变成暂停条、箭头变成对勾、平行线变成交叉，都是点对点插值，不在两张图之间淡入淡出。
2. **等待时让符号自己干活。** 翻译、搜索、连接、生成这类等待，按钮尺寸不变，符号做和含义相关的动作，而不是换成转圈。
3. **循环要有停顿。** 每一拍是一次 spring 加 0.2–0.4 s 的静止，只在静止时检查“完成了吗”。符号总停在整齐的姿态，不会半路刹住。
4. **位移走空间 spring，颜色走效果 spring。** 符号级的位移（1–3 dp）用 fast spatial；透明度、填充、颜色用 effects，永不过冲。
5. **余韵收尾。** 暂停、断开、取消都以低刚度的临界阻尼衰减结束，不做硬切。Yoin 取自日语的“余韵”，指声音停止后留下的回响，这也是整套动效的签名。

## Spring 参数

数值来自 Material 3 Expressive 的 MotionScheme，Compose 库里由 `SymbolMotion` 持有。

| 名称 | `SymbolMotion` | 阻尼比 / 刚度 |
| --- | --- | --- |
| Expressive fast spatial | `fastSpatial` | 0.6 / 800 |
| Expressive default spatial | `spatial` | 0.8 / 380 |
| Standard fast spatial | `control` | 0.9 / 1400 |
| Standard default spatial | | 0.9 / 700 |
| fast / default / slow effects | `effects` = default，`slowEffects` = slow | 1.0 / 3800 · 1600 · 800 |
| 余韵衰减（Yoin） | `resonance` | 1.0 / 60 |
| 抖动（Yoin，失败反馈） | | 0.28 / 900 |

## 翻译等待：文 / A 轨道交换

**进行中。** 文 和 A 各自保持直立，沿同一个圆（半径约 5.3，圆心在符号中心）各走半圈、互换位置。走到半路时，从右上经过的字放大到 1.08，从左下经过的缩到 0.86、透明度降到约 0.6，像两张牌一前一后交错，不会撞在一起。每次交换用 Expressive default spatial，落位后停 0.32 s。

**结束。** 走完当前这半圈再判断；如果停在交换后的位置（A 在左上），再补半圈。静止姿态永远是 文A。

**失败（原型）。** 回到 文A 后用抖动 spring 左右摇两下。

**减弱动效。** 字形不动，只在 42 % 和 100 % 透明度之间用 slow effects 呼吸，结束时停在 100 %。

建议：翻译进行中让翻译按钮本身保持满强调，只把旁边的按钮设为不可用，否则 disabled 的透明度会把动画压暗。

## 播放模式：一个按钮

随机和循环放在同一个按钮上，和 Spotoolfy 一样：每点一下 列表循环 → 随机 → 单曲循环 → 列表循环（列表循环在 Spotoolfy 里叫 sequential，即“顺序”）。循环图标的两半和随机图标的两股都画成同样的 7 段三次贝塞尔链，所以切换是同一组线条在动：环的上半股把尾巴甩下去，变成上升的一股；下半股绕中线水平翻转，变成下降的一股，落定时在上升那股下面让出缝。回到环时，单曲循环的「1」比线条晚 140 ms 弹出，落进已经合拢的环里。

## 动效清单

| # | 动效 | 适用场景 | 动作 | Spring | 减弱动效 | Compose |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 翻译等待 | 翻译按钮 | 见上 | E default + 0.32 s 停顿 | 透明度呼吸 | `rememberTranslateSymbolPainter` |
| 2 | 加入资料库 · 等待确认 | 资料库「+」，服务端稍后确认 | 竖线收起、横线缩成圆点，卡片里一段弧转动；确认后圆点展开成对勾并回弹；失败回到「+」并摇两下 | 变形 E fast；弧 fast / slow effects | 弧不转只呼吸；确认直接出对勾 | |
| 3 | AI 生成 | 生成、摘要、推荐 | 大星每次转 90° 后停，小星错拍闪；完成时填实并轻微放大 | 旋转 E default；填充 default effects | 透明度呼吸，完成直接填实 | `rememberSparkleSymbolPainter` |
| 4 | 投屏连接 | 投屏按钮 | 圆点、内弧、外弧依次点亮并外弹；连上后面板从左下长出（cast_connected） | 点亮 default effects；外弹 E fast；面板 E default | 只有透明度 | |
| 5 | 搜索中 | 搜索面板 | 放大镜在三个位置间“张望”，有结果时回原位并放大一下 | E default + 0.16 s | 透明度呼吸 | |
| 6 | 重新扫描 | 刷新 | 每拍转一整圈后停，结束总在整圈 | E default + 0.22 s | 透明度呼吸 | |
| 7 | 下载 → 已下载 | 离线下载 | 下载中箭头点头；完成时箭杆缩回，箭头三点变成对勾 | E fast | 直接切换 | |
| 8 | 正在播放 | 列表当前行、迷你播放器 | 柱子追随随机高度（或真实音频能量）；暂停时从两边到中间依次缩成圆点 | 跳动 E fast；衰减用余韵 | 静止，暂停时降到 45 % 透明度 | `rememberEqualizerSymbolPainter` |
| 9 | 播放 ↔ 暂停 | 播放按钮、迷你播放器 | 三角竖切两半，各变一根暂停条；不旋转 | S fast | 同一变形（位移本来就小） | `rememberPlayPauseSymbolPainter` |
| 10 | 收藏 | 心形按钮、曲目行 | 描边心跳一次（0.8 → 1），实心从中心长出，六个小点散开；取消只收回实心 | E fast；散点 slow effects | 实心淡入淡出 | `rememberFavoriteSymbolPainter`（不含散点） |
| 11 | 播放模式 · 一个按钮 | 播放控制 | 一个按钮循环 列表循环 → 随机 → 单曲循环。列表循环 → 随机：环被剪开，上半股甩成上升的一股，下半股像翻牌一样翻过来、从上面那股底下穿过，落定时让出缝。随机 → 单曲：两股翻回成环，「1」随后弹出。单曲 → 列表：「1」缩回，两个箭头沿各自方向推一下 | 剪开与翻转 E default；「1」与推动 E fast | 淡出、切换、淡入 | `rememberPlayModeSymbolPainter` |
| 12 | 展开 / 收起 | 折叠行、菜单 | 箭头先压平再翻折，像合页，不整体旋转 | E default | S fast spatial | `rememberExpandSymbolPainter` |
| 13 | 导航选中 | 底部导航、Nav Rail | 实心从底部涨满，同时按钮变宽、轻压回弹 | 涨满 S fast；回弹 E fast；变宽 S default | 实心淡入 | |
| 14 | 预测性返回 | 返回箭头 | 手势进度（经返回手势缓动）缩短箭杆、箭头左移；提交时滑出，取消时弹回 | 手势直驱；提交 E fast；取消 S default | 只缩箭杆 | |
| 15 | 上一首 / 下一首 | 播放控制 | 三角朝切歌方向推一下再回弹 | E fast 冲量 | 没有位移 | |
| 16 | 显示 / 隐藏 | 密码、Token 输入框 | 斜线从左上画到右下，眼睛微眯，斜线经过处轮廓断开 | S default | 斜线直接出现 | |
| 17 | 回到当前句 | 歌词 | 两个箭头向中线合拢再弹开，中线闪一下 | E fast 冲量；slow effects | 只闪中线 | |
| 18 | 错误 | 错误徽标、连接失败 | 感叹号摇两下，只在刚失败时 | 抖动 | 只变色 | |
| 19 | 发送 | 发送按钮 | 纸飞机从右上飞出，从左下飞回 | E fast / E default | 淡出淡入 | |
| 20 | 记忆印章 | 收藏成为记忆 | 印章转回正位并盖下，心形随后弹出 | E fast | 直接出现 | |
| 21 | 设置 | 设置入口 | 每次点按转一个齿（45°） | E default | 不转 | |

E = Expressive，S = Standard。

## 实现说明（Compose）

- 每个动效符号是一个返回 `Painter` 的 `@Composable`，内部用 `rememberVectorPainter { Group { Path } }` 构建、`Animatable` 驱动。静态符号仍然是 `ImageVector`。
- 循环放在一个长期运行的 `LaunchedEffect` 里，通过 `rememberUpdatedState` 读最新状态，状态变化不会掐断正在走的半圈。
- 循环会检查 `MotionDurationScale`：系统动画时长缩放为 0 时每个动画都会在下一帧结束，所以循环直接停下，符号保持静止而不是闪烁。
- 两态变形要求两态点数相同。本套里 play_filled 与 pause_filled、download 与 download_done、library_add 与 library_added、各方向的 V 形箭头，以及循环与随机的线条（`SymbolGeometry` 里的 7 段链）都是按这个规则画的。
