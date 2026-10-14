# Cultural Event Promotion Skill V3.1

一个面向 Codex 的文化活动宣传海报 Skill，用于从 PDF、Word、Excel、图片及混合资料包中提取活动信息，建立可追踪的内容母本，识别活动类型，并进一步完成中英文海报的视觉策略、生成、排版与质量检查。

> Skill 的正式入口是 [`SKILL.md`](SKILL.md)；英文入口见 [`SKILL.en.md`](SKILL.en.md)。本 README 仅用于介绍、安装和协作。

## V3.1 更新

- 删除总入口描述中的商品营销／一般社区服务排除表述，并同步英文入口。
- 十四类（含学术论坛）统一从类别路由加载，保留原有中文／英文模板、字体与视觉规则。
- 母本提取结果增加必经人工确认，记录版本、范围和真实用户回复。
- 比例不符、缺少必需资料图等严重制作问题首次发现即暂停受影响流程，待具体方案确认并复检后恢复。

确认流程详见 [人工确认节点](references/human-confirmation-gates.md)。包内原有字体、图片、成员资源与脚本保留；内容与规格改动仍按其原规则核验。

## 主要能力

- 盘点并解析 PDF、Word、Excel、图片和文件夹中的混合资料。
- 提取文字、表格、图片、二维码及来源信息，建立内容母本。
- 输出主活动类型、可选次类型、属性标签、置信度和原文依据。
- 为中文、英文及双语海报组织文案和排版策略。
- 按活动类型选择视觉、字体、信息层级和媒介适配方案。
- 对活动事实、语言、可读性、文化表达和输出规格进行质量检查。

## 支持的 14 类活动

1. 传统文化展览
2. 红色主题展览
3. 数字艺术展览
4. 民族交响音乐会
5. 音乐节
6. 节庆灯会
7. 学术论坛
8. 校庆活动
9. 体育赛事
10. 动漫游戏展
11. 品牌快闪
12. 艺术街区／艺术季
13. 非遗文创与独立出版市集
14. 工作坊活动

每一类都有独立策略文件，位于 [`references/activity-types/`](references/activity-types/)。主 Skill 完成类型判断后，只加载对应策略，避免一次引入无关规则。

## 目录结构

```text
.
├── SKILL.md                       # 中文 Skill 入口
├── SKILL.en.md                    # 英文 Skill 入口
├── agents/openai.yaml             # UI 元数据与默认提示
├── references/                    # 工作流、内容母本、双语与视觉策略
│   └── activity-types/            # 14 类活动的独立策略文件
├── assets/                        # 母本、提示计划、交付与质检模板及参考图
├── scripts/                       # 文件盘点、母本和交付校验脚本
├── tests/                         # 冒烟测试与测试夹具
└── examples/                      # 课程案例映射
```

## 安装

将仓库直接克隆到 Codex Skills 目录：

```bash
git clone git@github.com:dengyuchen658-lab/CulturalEventPromotion_Skills.git \
  ~/.codex/skills/cultural-event-poster
```

也可以使用 HTTPS：

```bash
git clone https://github.com/dengyuchen658-lab/CulturalEventPromotion_Skills.git \
  ~/.codex/skills/cultural-event-poster
```

若已将仓库下载到其他位置，也可以把整个仓库目录复制到 `~/.codex/skills/cultural-event-poster/`。安装后重新打开相关 Codex 会话，使 Skill 被重新发现。

## 使用

在请求中明确调用：

```text
请使用 $cultural-event-poster 分析这个文化活动资料包，先输出活动类型和内容母本，不要生成海报。
```

或提出完整制作任务：

```text
请使用 $cultural-event-poster 根据资料包制作中文和英文两版文化活动海报。
```

资料中的文字仅作为待分析内容，不会覆盖用户当前指令。没有可靠来源的信息会保持为 `missing`、`pending` 或 `conflict`，不会被补写成事实。

## 本地验证

```bash
python3 scripts/check_internal_links.py
python3 tests/run_smoke_tests.py
```

如需使用全部辅助脚本，可安装：

```bash
python3 -m pip install -r requirements.txt
```

## 素材与协作说明

- `assets/reference-posters/` 中的图片用于课程案例分析和视觉机制参考；来源或授权未确认时，不应直接用于公开成品。
- 修改活动分类时，请同步检查总路由、对应类型策略、双语规则和测试。
- 向远程仓库发布、上传成品或操作外部平台，仍需用户明确授权。

## English summary

This repository contains a Codex skill for extracting traceable event facts from mixed source packages, classifying cultural activities, planning category-specific visual strategies, and producing quality-controlled Chinese and English poster variants. Start with [`SKILL.en.md`](SKILL.en.md) for the English instructions.
