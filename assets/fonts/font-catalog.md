# 随包字体资源

学术论坛字体使用按[该类别最新强制规则](../../references/activity-types/academic-forum.md)执行，覆盖本页的通用可选建议：中文H1只选演示夏行楷或VonwaonBitmap之一；英文H1强制[Playball-Regular.ttf](playball/Playball-Regular.ttf)。两版标题字族不相同，非H1（含完整会议名、日期）统一HarmonyOS Sans SC。Playball文件来自用户提供；授权范围未随文件说明，当前用于用户请求的测试，正式发布须确认授权。

使用时从Skill根目录解析资源路径，无需全局安装，不依赖用户下载目录。以下为候选资源，依据活动学科、研究对象、表达方向及字形覆盖选择；不强制所有海报使用。

| 资源 | 核验家族／样式 | 适合角色 | 使用限制 |
|---|---|---|---|
| [VonwaonBitmap-16px.ttf](vonwaon-bitmap/VonwaonBitmap-16px.ttf) | VonwaonBitmap 16px／Regular，Version 1.00 | 数字人文、数字媒介与技术主题中的短标题、数字 | 像素是媒介气质，不自动代表所有科学研究；不用于密集嘉宾、机构、议程与细则 |
| [VonwaonBitmap-16pxLite.ttf](vonwaon-bitmap/VonwaonBitmap-16pxLite.ttf) | VonwaonBitmap 16pxLite／Regular | 已核验字符的短标题、日期、标签 | Lite为较小字库版本，不等于更细字重；缺字时选择有覆盖的完整版或另一合适字体 |
| [演示夏行楷.ttf](slide-xiaxing/演示夏行楷.ttf) | Slidexiaxing／Regular，Version 1.000 | 文化遗产、历史、艺术等相关主题的大标题或有限强调文字 | 不用于密集正文；自然科学、医学、工程等活动不得因“学术论坛”身份直接套用 |
| [思源宋体CN](source-han-serif-cn/font-config.md) | Regular／Medium／Bold | 需要宋体结构和正式出版气质的标题、信息与正文 | 字重、覆盖及许可按该配置文件核对 |

## 覆盖与排版核验

- 本次检查记录：16px完整版映射7542个字符，Lite映射4040个字符，演示夏行楷映射6973个字符；字库数量不等于任何未来文案都能排印。
- 本轮数字人文论坛实际标题字符及ASCII英文、数字均有覆盖。每次使用仍须核验新文案中的姓名、机构、学科术语和标点，禁止静默替换成方框或错误字符。
- 像素字体以原生16px网格的整数倍作为优先试排尺寸，检查导出和手机缩略图的网格与笔画；可读性优先，不以整数倍为不可调整的硬约束。
- 中英文可使用不同字体体现对应的信息角色；英文无需照搬中文行楷。正文使用有覆盖、许可适用且容易阅读的黑体、宋体、衬线或无衬线字体。

## 来源与许可记录

三份TTF由用户提供，加入时保持原始二进制内容。字体内版权字段分别为Haoyu Qiu（2021）和keynoteart（2020）。

像素字体随下载包附带的[license.txt](vonwaon-bitmap/license.txt)声明“Vonwaon Bitmap Font Lite (1.0)”适用CC0，并允许个人、教育和商业项目使用。原文随包保存；该文件标题明确为Lite，16px完整版与该声明的对应关系尚未单独核验，不扩大解释为全部文件许可已确认。

演示夏行楷下载包未附可核验的许可文本；字体内版权声明不是授权条款。保留其用户提供、用于本轮本地设计测试的来源记录，商业用途和对外分发范围标为待确认。不要据下载站广告或文件名自行认定“免费商用”，也不要生成不存在的许可证。

## 成员强制模板字体

六套成员模板保留完整资源与原加载路径，字体无需全局安装。艺术街区、工作坊及体育赛事必须按 [类别模板路由](../../references/category-template-routing.md) 使用指定文件，不能从本索引自由挑选替代模板字体。

| 模板 | 实际字体目录与角色 |
|---|---|
| 艺术街区中文 | [字体目录](../category-templates/art-district/zh-CN/assets/fonts/)：澹雅明体DYmingB.ttf 用于标题；Harmony Regular／Medium／Bold 用于信息与数字 |
| 艺术街区英文 | [字体目录](../category-templates/art-district/en/assets/fonts/)：Trajan Bold 标题非数字；Futura Std Book／Medium／Bold 信息；Harmony Regular／Medium／Bold 数字 |
| 工作坊中文 | [字体目录](../category-templates/workshop/zh-CN/fonts/)：HarmonyOS Sans SC 六份 TTF，实际角色依模板 |
| 工作坊英文 | [字体目录](../category-templates/workshop/en/fonts/)：同系列六份 TTF，字母、数字、标点均依模板 |

按字体文件哈希去重共 19 份新字体资源；多个模板中的相同文件保留各自路径，以免破坏原脚本。Futura Maxi、Trajan Regular 和其他附带字重保留，只有模板允许或用户明确指定时使用，不自动替换当前角色。每次新文案仍须核对字形覆盖、实际注册、字重与测量。

来源为用户提供的小组成员包，复制时保持二进制不变。未随包提供独立完整许可证或购买授权凭据。Futura Maxi 内置条款明确限制复制与分发；澹雅明体内置字段为 IPA Open Font License v1.0；其余字体的文件名、版权字段或许可网址不构成完整授权核验。当前记录为课程本地合并；对外发布字体包时须按实际许可证确认，不能把它们标为全部免费商用。逐文件元数据及哈希见 [字体记录](member-template-fonts.json)。

## 体育赛事成员字体

[中文字体目录](../category-templates/sports/zh-CN/fonts/) 与 [英文字体目录](../category-templates/sports/en/fonts/) 各保留江城律动黑.ttf 和 HarmonyOS Sans SC 六字重。主标题实际加载江城律动黑，其余文字按模板使用 Harmony；不能静默替换。文件字节数与 SHA256 见各包 references/font-assets.json，来源为用户小组成员包，二进制保持原样。未据文件名新增免费商用或对外分发授权结论。


## 传统文化、节庆及艺术展览成员字体

以下三个类别固定使用本次成员包内的字体，完整 TTF 与对应 OFL 文本保留在各语言 `assets/fonts`，无需全局安装。中文和英文各有独立完整副本，不改变原脚本资源路径。

| 类别 | 字体目录与角色 |
|---|---|
| 传统文化／文物／考古 | [中文](../category-templates/traditional-cultural-exhibition/zh-CN/assets/fonts/)／[英文](../category-templates/traditional-cultural-exhibition/en/assets/fonts/)：Ma Shan Zheng 中文艺术标题，Noto Serif SC 中文展讯，Bodoni Moda 英文标题，Inter 英文辅助 |
| 节庆／春节／国庆 | [中文](../category-templates/festival-lantern/zh-CN/assets/fonts/)／[英文](../category-templates/festival-lantern/en/assets/fonts/)：Bodoni Moda 英文大标题，Noto Serif SC 中文，Inter 辅助信息 |
| 数字艺术／绘画／摄影 | [中文](../category-templates/digital-art-exhibition/zh-CN/assets/fonts/)／[英文](../category-templates/digital-art-exhibition/en/assets/fonts/)：Noto Sans SC 中文，Inter 英文与数字，标题和正文使用明确字重差 |

上述五种字体均随包保留成员提供的 SIL Open Font License 文本。字体文件按字节复制，逐份哈希、原路径和许可证见 [本次资源来源清单](member-template-additions-2026-10-12.json)。这些是成员复现所用的开源字体；不能宣称已识别原参考图全部原版字体。字形覆盖与字号仍须按每次真实文案核验。


## 品牌快闪、红色主题与非遗文创共享字体

本轮字体按实际 SHA256 去重到 [共享资源目录](member-modules/)，中英文模块的 `references/font-manifest.json` 记录正确路径、许可、哈希与可用状态，不安装到系统字体目录。字体二进制与成员记录保持一致；志莽行书和红色模块马善政已由用户补交原版并接入。

品牌固定模板V2：中文标题默认寒蝉全圆ChillRoundF，中文元信息／正文思源黑体SC Regular／Bold；英文标题Nunito Bold，元信息／正文Nunito Regular／Bold。思源Heavy与小赖日文字形版保留备选，短标题用小赖时需核对简体字形；得意黑未提供，不得选用。实际字体仍由对应语言manifest绑定共享路径。

红色主题：九份哈希一致资源已补齐，分别为思源宋体 Regular／Bold、思源黑体 Regular／Bold、霞鹜文楷、Nunito Regular／Bold、马善政和志莽行书。**两份书法字现为bundled可用**，来自用户补交文件且完全匹配原成员hash；实体分别为 [马善政](member-modules/ma-shan-zheng/MaShanZheng-Regular.ttf) 与 [志莽行书](member-modules/zhi-mang-xing/ZhiMangXing-Regular.ttf)，随包 [马善政OFL](member-modules/ma-shan-zheng/OFL.txt)／[志莽行书OFL](member-modules/zhi-mang-xing/OFL.txt) 已保存。两版字体策略和 `scripts/resolve_font.py` 将提示计划及排版绑定到真实路径，书法仅用于审核后的短标题。其他类别独立版本保持原样。

非遗市集新模板改用各语言fonts目录的真实字体：中文与英文各自加载FontQu Smile（字制区喜脉喜欢体）400，两版各八份NotoSerifSC250–900字重；清单分别见[中文font-assets](../category-templates/heritage-market/zh-CN/references/font-assets.json)和[英文font-assets](../category-templates/heritage-market/en/references/font-assets.json)。两版额外她屿山海仅为备用，不进入当前标题路由。新包未附许可，保留未知，不沿用旧共享字体许可作为新字族授权。旧非遗共享资源和补齐许可仅保留历史记录，不能作为新版字体路由。

实际版本、来源、原包哈希、共享文件与许可记录见 [本轮接入清单](member-modules/integration-manifest.json)。只有实际注册／加载、字形与尺寸核对通过的文件才可记为项目采用字体；Nunito 不作为中文唯一字库。


## 潮流演出、传统表演与动漫游戏成员字体

本批六个包的24份不同字体、13个字族与完整随包OFL文本保留在 [共享资源目录](performance-anime-members/)。同哈希文件只存一份，字体实体未修改；不覆盖既有SC／CN版或同名字族其他版本。各包 `assets/fonts/catalog.json` 用相对成员根目录的实际路径记录哈希、内部名称、字重、官方仓库提交与许可证，`role-profiles.json` 和角色索引给出字段候选序列。

|类别|实际字体清单及主要角色|
|---|---|
|潮流演出|[中文清单](../category-templates/music-festival/zh-CN/assets/fonts/catalog.json)／[英文清单](../category-templates/music-festival/en/assets/fonts/catalog.json)：思源黑体CN、思源宋体CN、Anton、Archivo Black、Barlow／Condensed、Bebas Neue，按场景／阵容／肖像方案调度|
|传统表演|[中文清单](../category-templates/symphony-concert/zh-CN/assets/fonts/catalog.json)／[英文清单](../category-templates/symphony-concert/en/assets/fonts/catalog.json)：思源宋体CN、思源黑体CN、Spectral、Barlow、成员本包Ma Shan Zheng，按戏曲／相声／交响／融合音乐调度|
|动漫游戏|[中文清单](../category-templates/anime-game-expo/zh-CN/assets/fonts/catalog.json)／[英文清单](../category-templates/anime-game-expo/en/assets/fonts/catalog.json)：思源黑体CN、站酷快乐／庆科黄油、Anton、Archivo Black、Barlow／Condensed、Bebas Neue、Rajdhani、Spectral；Noto Sans Thai仅在实际泰文需求及可变字体支持下使用|

调用每包 `scripts/font_engine.py` 检查真实字段并按返回路径加载，逐项记录字形覆盖、回退、尺寸与渲染结果。候选不等于原图字体精确识别；字体哈希与许可通过不证明所有排版器、审美或完整海报已通过。

传统表演包Ma Shan Zheng的二进制及许可服务该模块条件策略，与红色主题新补入的原版是独立文件。红色模块Ma Shan Zheng与Zhi Mang Xing现已由用户补交，按其最新manifest及字体绑定规则使用。既有传统文化展览／传统表演版本不覆盖。

原包文件来源、原始清单、共享资源及成员哈希见 [本批接入清单](performance-anime-members/integration-manifest.json)。字体OFL许可不覆盖参考海报、官方IP、人物、Logo等素材权限。

## 校庆编辑式成员字体

新校庆中文与英文包各完整保留八份NotoSerifSC静态字体与原 `fonts/` 路径：[中文字体清单](../category-templates/university-anniversary/zh-CN/references/font-assets.json)／[英文字体清单](../category-templates/university-anniversary/en/references/font-assets.json)。ExtraLight实际250，Light300、Regular400、Medium500、SemiBold600、Bold700、ExtraBold800、Black900；所有中文、英文字母、数字及标点按对应语言模板注册实际文件，不以旧思源宋体CN替代。

字体文件哈希与成员完全一致，路径相对该语言模块根目录，不依赖下载目录或系统安装。原包没有许可文件，按成员清单记录为未提供，不从字族名自行扩大授权结论。使用前运行该包 `scripts/check_assets.py` 并重新检查本题字符。原始来源与哈希见 [校庆接入清单](anniversary-template-additions-2026-10-12.json)。


动漫严格参考新版新增正常字宽Barlow BoldItalic，SHA256与随包OFL验证后接入performance-anime-members/barlow；新增reference-022／052／053为对照候选，实际项目须先比较原图并锁定字体，显式reference_font_check禁止缺字静默回退。
