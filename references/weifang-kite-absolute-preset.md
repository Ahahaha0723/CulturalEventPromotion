# 风筝数字艺术展：已验收固定绝对参数

这是D26要求保存的本案固定版式：原始验收输出T2_v11/I13由S01/R13生成，S03把其实际参数、图像资产和执行器封装。指定同款时按此执行，其他活动不自动继承本案事实或参数。

## 文件与执行

- [通用画布/图层/图像/字体](../assets/layout-presets/weifang-kite-digital-v1/canvas.json)
- [中文完整文字和坐标](../assets/layout-presets/weifang-kite-digital-v1/zh-CN.json)
- [英文完整文字和坐标](../assets/layout-presets/weifang-kite-digital-v1/en.json)
- [来源及哈希](../assets/layout-presets/weifang-kite-digital-v1/origin-and-sources.json)
- [独立执行器](../scripts/render_weifang_absolute_preset.py)，使用Pillow，无需原项目目录或图像生成。

在安装Pillow的Python中运行：`python scripts/render_weifang_absolute_preset.py --output <新的输出目录> --language both`。输出已存在时拒绝覆盖。源课程文案、字体文件与已派生12个图像资产都在包内；复制资产不算新增生成候选。替换文案需确认新母本与适配；原配置保留，不把示例事实带入新活动。

## 坐标及字体解释

画布3840×2160，左上原点(0,0)，x向右、y向下，单位px。`draw_xy`是Pillow `anchor=lt`的实际绘制点，`bbox`是按真实字体测出的可见文字框，两者不可混淆。中文与英文的全部行文字分别保存，包括课程标记；行间距由各行y坐标决定，没有额外字距处理。

中文NotoSansSC使用wght轴；中文文化说明第二行NotoSerifSC固定wght700；中文标题/工艺MaShanZheng是固定Regular，历史参数900/650只代表requested_weight，实际无字重轴。英文标题/工艺BodoniModa轴为[wght650,opsz72]；英文其余Inter轴按[opsz32,每行wght]。不能把中文固定字体称作900粗体。字体路径、哈希、实际轴与字号都在JSON中。

## 画布、图片与图层绝对参数

纸纹全画布3840×2160；背景K02已裁出主体上三分之一，放置[0,609,3840,2160]，20%不透明度。中央柔化区[1150,350,2690,1060]，mask alpha130/255，Gaussian blur90。顶部装饰[0,0,3840,270]，20%不透明度，与Logo下沿270齐平；其原主体裁切[34,211,2152,524]、裁边阈值8仅用于求边界，已非等比适配3840×270。

Logo框[140,70,340,270]，200×200。右上橙条[3260,124,3640,137]。四条工艺橙线中心x=405/945/2895/3435，框[x−95,1650,x+95,1661]；Pillow矩形包含末端像素。标题/文化说明参考中心x1920，右侧信息与类别右缘3640。虚线/方形端点、标题白板及票务橙板均关闭。

前景8素材位置如下；槽位对称，不同作品不镜像。所有sprite路径/尺寸/实际放置框及hash见canvas.json。

| 素材 | 槽位[l,t,r,b] | 实际粘贴框[l,t,r,b] |
|---|---|---|
| K03 | [180, 380, 630, 920] | [220, 405, 590, 895] |
| K05 | [720, 380, 1170, 920] | [754, 410, 1136, 891] |
| K06 | [2670, 380, 3120, 920] | [2686, 402, 3103, 898] |
| K07 | [3210, 380, 3660, 920] | [3252, 420, 3618, 881] |
| K10 | [180, 990, 630, 1530] | [210, 1037, 600, 1483] |
| K12 | [720, 990, 1170, 1530] | [742, 1015, 1148, 1505] |
| K13 | [2670, 990, 3120, 1530] | [2703, 1031, 3087, 1489] |
| K15 | [3210, 990, 3660, 1530] | [3246, 1027, 3624, 1493] |

## 中文逐行绝对文字参数

| 字段/文字 | 实际字体/轴 | 字号px | draw_xy | 实际bbox | 对齐 |
|---|---|---|---|---|---|
| C01：城市文化中心 | NotoSansSC.ttf / [550] | 48 | [370, 146] | [370, 146, 658, 192] | left |
| category：数字艺术展 | NotoSansSC.ttf / [550] | 42 | [3430, 177] | [3430, 177, 3640, 218] | right |
| C02：风起鸢成 | MaShanZheng-Regular.ttf / 固定Regular | 330 | [1260, 560] | [1260, 560, 2580, 868] | center |
| C02：潍坊风筝制作技艺 | NotoSansSC.ttf / [800] | 84 | [1584, 1010] | [1584, 1010, 2256, 1093] | center |
| C02：数字艺术展 | NotoSansSC.ttf / [800] | 92 | [1690, 1130] | [1690, 1130, 2150, 1220] | center |
| C03：国家级非物质文化遗产代表性项目： | NotoSansSC.ttf / [550] | 60 | [1440, 1350] | [1440, 1350, 2400, 1408] | center |
| C03：风筝制作技艺（潍坊风筝） | NotoSerifSC.ttf / [700] | 65 | [1530, 1440] | [1530, 1440, 2310, 1503] | center |
| C04：扎 | MaShanZheng-Regular.ttf / 固定Regular | 84 | [363, 1560] | [363, 1560, 447, 1628] | center |
| C04：绘 | MaShanZheng-Regular.ttf / 固定Regular | 84 | [903, 1560] | [903, 1560, 987, 1632] | center |
| C04：糊 | MaShanZheng-Regular.ttf / 固定Regular | 84 | [2853, 1560] | [2853, 1560, 2937, 1628] | center |
| C04：放 | MaShanZheng-Regular.ttf / 固定Regular | 84 | [3393, 1560] | [3393, 1560, 3477, 1631] | center |
| C05：2026.12.12 — 2027.03.14 | NotoSansSC.ttf / [800] | 105 | [180, 1790] | [180, 1790, 1471, 1872] | left |
| C07：免费参观 · 须提前预约 | NotoSansSC.ttf / [550] | 60 | [180, 1950] | [180, 1950, 808, 2008] | left |
| C06：周二至周日 10:00–20:00 | NotoSansSC.ttf / [550] | 60 | [2977, 1790] | [2977, 1790, 3640, 1844] | right |
| C06：19:00停止入场 | NotoSansSC.ttf / [550] | 60 | [3242, 1870] | [3242, 1870, 3640, 1928] | right |
| C06：周一闭馆 | NotoSansSC.ttf / [550] | 60 | [3400, 1950] | [3400, 1950, 3640, 2008] | right |
| course-note：课程测试 · 非真实机构主办 | NotoSansSC.ttf / [400] | 31 | [180, 2090] | [180, 2090, 566, 2120] | left |

## 英文逐行绝对文字参数

| 字段/文字 | 实际字体/轴 | 字号px | draw_xy | 实际bbox | 对齐 |
|---|---|---|---|---|---|
| C01：City Cultural Center | Inter.ttf / [32, 550] | 48 | [370, 146] | [370, 146, 805, 190] | left |
| category：DIGITAL ART | Inter.ttf / [32, 550] | 42 | [3388, 177] | [3388, 177, 3640, 207] | right |
| C02：Where Wind | BodoniModa.ttf / [650, 72] | 215 | [1266, 470] | [1266, 470, 2574, 636] | center |
| C02：Takes Form | BodoniModa.ttf / [650, 72] | 215 | [1319, 745] | [1319, 745, 2521, 909] | center |
| C02：A Digital Art Exhibition of | Inter.ttf / [32, 750] | 66 | [1530, 1100] | [1529, 1100, 2311, 1162] | center |
| C02：Weifang Kite-Making Craft | Inter.ttf / [32, 750] | 66 | [1500, 1200] | [1500, 1200, 2341, 1262] | center |
| C03：National-level Intangible Cultural Heritage: | Inter.ttf / [32, 550] | 60 | [1356, 1390] | [1356, 1390, 2485, 1446] | center |
| C03：Weifang Kite-Making Craft | Inter.ttf / [32, 650] | 65 | [1520, 1475] | [1520, 1475, 2319, 1535] | center |
| C04：frame, | BodoniModa.ttf / [650, 72] | 60 | [312, 1570] | [312, 1570, 497, 1625] | center |
| C04：paint, | BodoniModa.ttf / [650, 72] | 60 | [864, 1570] | [864, 1570, 1027, 1631] | center |
| C04：paste and | BodoniModa.ttf / [650, 72] | 60 | [2758, 1570] | [2758, 1570, 3032, 1630] | center |
| C04：fly | BodoniModa.ttf / [650, 72] | 60 | [3395, 1570] | [3395, 1570, 3475, 1632] | center |
| C05：12 DEC 2026 — 14 MAR 2027 | Inter.ttf / [32, 800] | 89 | [180, 1790] | [180, 1790, 1389, 1858] | left |
| C07：Free admission with advance reservation | Inter.ttf / [32, 550] | 60 | [180, 1950] | [180, 1950, 1276, 1995] | left |
| C06：Tuesday–Sunday 10:00–20:00 | Inter.ttf / [32, 550] | 60 | [2816, 1790] | [2816, 1790, 3640, 1846] | right |
| C06：Last entry 19:00 · Closed Mondays | Inter.ttf / [32, 550] | 60 | [2714, 1939] | [2714, 1939, 3640, 1995] | right |
| course-note：Course test · Institution is fictional | Inter.ttf / [32, 400] | 31 | [180, 2090] | [180, 2090, 643, 2112] | left |

## 固定关系和复查

C06与C07均为60px、实际wght550；同语言相同字体。英文C06为两行，其首行y1790与C05顶对齐，末行实际y1939、下缘1995与C07下缘齐平。中文C06三行y1790/1870/1950。主标题拆为两部分时无冒号；C03文化说明中的冒号仍保留。

执行器检查每行bbox、每个素材放置框和原验收图RGB像素哈希，环境相同可核实逐像素复现；不同Pillow/FreeType环境出现不一致时记录实际结果，不能静默称完全复现。复现验证不是新活动/独立前向测试，不增加设计候选或海报迭代轮次。E23图集边缘与E33装饰内部纸色色区仍保留，封装不代表修复；官方quick_validate依赖限制另记录。

## S04：新材料自动进入八素材版式

无需用户再提出“使用同款”。识别为风筝数字艺术展后，按[自动路由](weifang-kite-auto-route.md)展示编号并请选8图。任务接口：`python scripts/render_weifang_absolute_preset.py --job <项目任务JSON> --output <新目录> --language both`；任务JSON由[输入模板](../assets/layout-presets/weifang-kite-digital-v1/selected-job-template.json)派生。八图确认/母本文案/当前Logo必须来自本任务；背景默认来自当前素材包02号上三分之一，用户可以自由指定其他有效编号，不要求背景在八前景集合中；默认02由本固定规则授权，用户覆盖另记录真实回复。脚本重算新图尺寸和文字框，保留固定槽位/字号/字体/对齐锚点；新文案超出画布时报告而不静默缩字或删字段。没有--job的旧接口保留同案像素复现校验。
