# 红色主题字体选择与中英文排版策略

## 核心原则
活动类别仅缩小候选集，具体字体根据历史叙事类型、展览语气和信息功能选择。书法字≠红色文化默认字体。

## 已内置字体及职责
- `source-han-serif`（思源宋体 SC）：历史档案、文物证据、正式文化回顾展的标题/引言。内置 Regular/Bold。
- `source-han-sans`（思源黑体 SC）：现代主题展的标题及**所有长正文、日期、地点、参观信息的首选**。内置 Regular/Bold。
- `lxgw-wenkai`（霞鹜文楷）：书信、人物故事、引言等人文表达；只在字形、字重、字号可读时使用。
- `zhi-mang-xing`（钟齐志莽行书）：精神主题的短标题/视觉强调，强调笔势；禁止用于历史事实小字。
- `ma-shan-zheng`（马善政毛笔楷书）：纪念性短标题/重点词；禁止用于历史事实小字。
- `nunito`：英文信息/辅助英文字体（Regular/Bold），正式文献场景亦可按实际字体组合选择思源宋体拉丁字符。

## 自动选择映射（非模板）
- 档案/文献/文物：思源宋体 Bold H1，思源黑体 Regular H3-正文。
- 革命人物/书信：思源宋体 H1，霞鹜文楷用于引言，思源黑体用于活动信息。
- 精神主题：志莽行书或马善政用于**经审核的简短 H1**，思源黑体用于 H2-H5。
- 现代专题/年轻化展览：思源黑体 Bold H1，Regular H2-H5，必要时局部书法字点缀。

## 中英双版本
- 共享已核对的历史事实、证据链接、展览主视觉与色彩系统；必须独立处理标题长度、断行、行距、模块宽度、信息优先级。英文需检查译名、准确性、日期格式；不得凭译文修改事实。
- 字体角色保持一致即可，禁止照搬中文行数/位置当作英文版式适配。

## 实际加载规则
- `references/font-manifest.json` 相对本语言模块 `SKILL.md` 所在根目录解析；读取每个条目的 `file` 和 `license_file`，它们指向总包共享目录 `../../../fonts/member-modules/`，不要拼接旧 `fonts/<family>/...` 路径。两份用户补交书法字及随包OFL已按原成员哈希接入，九份红色主题字体均可用。
- 不应依靠提示词“使用 XX 字体”来宣称成图已用包内字体。正式海报应在 HTML/CSS/SVG 或 Pillow 等可加载本地字体的工具中进行文字排版。
- 字体用前要检查文件存在、manifest sha256、TTF/OTF 可读、所需中文字符字形覆盖、字号清晰度、缺字和文本溢出。
- 在笔触较强字体中，政治人物、历史名称、日期等绝不能为了风格牺牲字形准确性。品牌/机构 Logo 不允许用普通字体自绘冒充官方标志。


## 提示计划与排版文件的实际路径绑定

以下路径以本语言模块根目录为基准；中文、英文包均解析同一共享实体，部署后无需用户原始微信文件夹。

|字体ID|实际文件 `file`|随包许可 `license_file`|允许角色|
|---|---|---|---|
|`ma-shan-zheng` / `display`|`../../../fonts/member-modules/ma-shan-zheng/MaShanZheng-Regular.ttf`|`../../../fonts/member-modules/ma-shan-zheng/OFL.txt`|审核后的短H1／重点词|
|`zhi-mang-xing` / `display`|`../../../fonts/member-modules/zhi-mang-xing/ZhiMangXing-Regular.ttf`|`../../../fonts/member-modules/zhi-mang-xing/OFL.txt`|审核后的短H1／视觉强调|

在本次 `prompt-plan` 的文字与字体部分记录 `family`、`weight`、实际绝对 `font_file`、`sha256`、`license_file` 和适用文字。运行本模块的 `scripts/resolve_font.py` 得到绑定，不从中文源包硬编码部署路径，也不只写字体名称：

```sh
python <本语言模块绝对路径>/scripts/resolve_font.py --family ma-shan-zheng --weight display --text-file <工作区已锁定标题.txt> --output <工作区font-binding-ma.json>
python <本语言模块绝对路径>/scripts/resolve_font.py --family zhi-mang-xing --weight display --text-file <工作区已锁定标题.txt> --output <工作区font-binding-zhi.json>
```

输出路径属于项目工作区。字体绑定器自动按自身目录读取清单、验证字体和许可哈希、检查实际标题完整字形；缺字或未知ID时报错，不自动换字。排版器读取返回的 `font_file` 真正加载；HTML/CSS用实际文件的 `@font-face src`，Pillow用 `ImageFont.truetype(font_file, size)`，不要把“提示词写了路径”当成图片模型已经应用字体。

无正式文字主视觉的图像提示继续只规划主题与文字预留；文字绑定作用于提示计划中的可控排版阶段。书法字不用于密集历史事实、日期地点或正文，英文信息仍按本语言策略采用Nunito／实际适合的拉丁字体并独立排版。每份新活动题名重新核验字形、尺寸和背景对比。
