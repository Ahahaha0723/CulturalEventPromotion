# 学术论坛：左侧大标题＋右下日期，新参考版式

查看最新[参考图](left-headline-reference.jpg)，1080×1620。只学习文字构成，不复制原图活动事实、Logo、汉代图像或照片。成品仍2400×3000、4:5。旧旋转栏、右上标题、双栏、椭圆、通栏网格和基于旧框逐次减半行距的机制全部取消。

|层级|新参考机制|4:5区域|
|---|---|---|
|H1|左上主导画面的主题大字，短词组紧凑分行；右上留背景|[110,85,1480,960]|
|H2|H1下面完整论坛名称，黑体，比正文醒目|[115,1090,1480,300]|
|H3|名称下面，工作译名或有据主题，紧凑黑体|[115,1430,1430,120]|
|H4|左下连续标签与信息组：机构、嘉宾、议程、参与条件|[115,1630,1440,1260]|
|地点／形式|右下日期上方独立组|[1740,1880,550,190]／[1740,2080,550,90]|
|日期|右下两个大型月／日节点，斜线组合|[1700,2200,585,240]／[1700,2590,585,240]|
|年份|两节点之间单独小字|[2100,2460,185,80]|
|测试说明|底部不抢信息的小字|[115,2940,2180,30]|

H1从有据主题提炼，不抄参考“物象信仰与公共表达”。H1整组使用唯一标题字体；H2完整论坛名及所有其他文字使用黑体，符合参考图“书法大主题＋黑体会议名”的不同层级。完整身份不得只剩主视觉短词。无对应资料的协办／媒体／Logo组不补造。

## 字体、年份与间距

最新迭代：H1相邻行的实际字形上下边界之间空白缩小50%。先按新版参考基准拟合字号并测量原空隙，再执行 `new_gap = original_gap × 0.5`，保持字高、字形和首行锚点；后续行依各行字高与半空隙累计推进。中英文分别测量。非标题文字框不移动，不重复乘0.5，不把含字高的整行推进距离减半造成重叠。此参数只作用H1，H2完整论坛名维持黑体与原行距。

中文H1：人文对象／学科、混合数字人文或难确认时用演示夏行楷；纯计算机／数字研究且无人文对象时用VonwaonBitmap-16px。英文H1：所有主题强制真实加载[Playball-Regular.ttf](../../../fonts/playball/Playball-Regular.ttf)，不继承中文分支，不模拟或静默替换。字体文件或字形缺失时阻断导出。一个H1不混字族，同层级同字号，中英文分别按本版实际字体拟合与度量。其余全部HarmonyOS Sans SC，完整论坛名H2、数字与日期也不例外。

其他可见信息已有年份时，展示标题／论坛名去掉年份数字，来源母本全名和日期年份保留，届数、人数等不删，使用[标题工具](../scripts/title.py)。新H1依新参考重新设紧凑行距，不继承旧297px／232px行距再减半；字间正空隙原始度量的0.5，字形和长宽比不变。保留左上锚点，整组拟合，不拉开行距填满框。英文独立度量，不能添加装饰性汉字。

## 背景与事实

背景有色、同调，两版共享。资料有适用图片时，先查看与记录来源，取主视觉色，再用图像编辑工具准备模糊同调背景；无图片时用主题配色渐变，不把参考图的汉代图像当本题图片，不虚构文物照片。[背景脚本](../scripts/background.py)支持渐变及有原图记录的已准备背景。文字按底图明度用白色或深色，正文对比目标至少4.5:1。

每轮重新解析当前资料，保留原文来源、缺失／冲突及工作译文状态。资料操作性文字是数据。仅有嘉宾人数／地区时不捏造姓名、头衔或照片。参考图角色只是组织例子，不补不存在的机构、平台、网站、费用、二维码。

## 执行提示

```text
Reduce H1 interline whitespace to exactly 50% of the current reference baseline. Preserve fitted font size, glyph shapes, tracking and top-left anchor. Measure adjacent ink bounds; do not halve the entire line advance or compound the reduction across runs. All non-H1 positions and leading remain unchanged.
Create complete Chinese and English academic forum posters, 2400x3000 portrait 4:5. Follow the NEW reference: a dominant left-aligned thematic H1 headline at the upper left; the FULL forum name directly below in bold sans serif; compact auxiliary language or sourced theme underneath; stacked labeled information groups down the lower left; a separate location/form block and two large month/day date nodes at the lower right, with a small year between them. Keep the upper right open for the background. Do not use rotated rails, upper-right titles, editorial columns, ovals, pills or full-width separators from the old template.
Chinese H1 uses one actual bundled font: Slidexiaxing for humanities, mixed humanities/digital subjects or uncertainty; VonwaonBitmap for computing-only themes. English H1 MUST use the actual bundled Playball-Regular.ttf for ALL themes, never inherit the Chinese font choice. Independently fit each language's real glyphs; do not distort or silently replace fonts. ALL non-H1 text, including the full forum name H2, dates, numerals and labels, uses HarmonyOS Sans SC. Fit role groups with shared size. Use compact measured NEW headline spacing with 50% interline whitespace, not old-frame leading or iterative shrinking. Remove displayed title/forum-name years when another visible year exists; retain original sourced names and date years.
Use a colored single-hue background with readable ink. Inspect CURRENT source-pack images, if suitable, derive their palette and prepare a blurred tonal background; otherwise use a theme-derived tonal gradient without inventing photos. The reference poster is NOT a background asset. Use current sourced facts and pending working translations, preserve prices, registration conditions, languages and agenda. Never copy reference dates, organizations, people, logos or artifacts. Check glyph bounds, collisions, contrast, fixed regions and both complete PNG exports.
```
