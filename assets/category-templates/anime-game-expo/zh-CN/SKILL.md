---
name: cultural-anime-game-poster
description: "为动漫与游戏展览整理资料、制定中英文海报策略、调用随包字体、执行生成前确认与图面迭代。按具体小类与真实内容决策；不用于商品营销。"
---

# 动漫与游戏展览海报补充

这是可独立运行、也可接入 cultural-event-poster 的专题补充。先读内容与证据，再确定表达和字体。字体下载记录不等于案例原字体确认，原始评分不等于传播效果。

- [接收资料与建立母本](references/intake-and-facts.md)
- [活动与子类策略](references/category-strategy.md)
- [生成前五项确认](references/pre-generation-approval.md)
- [中文海报](references/zh-poster-strategy.md)
- [英文海报](references/en-poster-strategy.md)
- [字体使用与调度](references/font-routing.md)
- [字体识别与替代](references/font-identification.md)
- [案例证据与缺项](references/case-evidence.md)
- [制作与QA](references/production-and-qa.md)


- [优秀案例分析与设计转化](references/reference-learning.md)：收到优秀案例或要求贴近参考时，在概念、字体和提示前读取；实际看图并落实到生产。
## 按小类调用

- [anime-convention](references/subtypes/anime-convention.md)
- [game-expo](references/subtypes/game-expo.md)
- [ip-experience](references/subtypes/ip-experience.md)
- [artist-alley](references/subtypes/artist-alley.md)

## 执行顺序

资料盘点 → 事实母本与冲突检查 → 主类型与小类 → 文化／主题命题与方向 → 字体样张和五项确认 → 无正式文字的主视觉（原创题名图形例外见案例转化说明） → 可控排版与语言重排 → 事实、字形、图面和规格QA → 用户审核及定向修订。用户已明确确认的决定直接沿用，未确认事项不自行填为人审通过。

用户只改文字关系时保留认可的主视觉；不要随机生成。不得虚构活动事实、官方身份、字体名称、授权、二维码或观众反馈。字体与题名选择按条件，不固化某张参考的画风。

## 实体资源与检查

- [Font catalog](assets/fonts/catalog.json) · [Role profiles](assets/fonts/role-profiles.json)
- [Chinese role index](assets/fonts/roles-zh-CN.md) · [English role index](assets/fonts/roles-en.md)
- [Pre-generation record](assets/pre-generation-review-template.json) · [Review record](assets/review-record-template.json)

```powershell
python scripts/font_engine.py --profile anime-character --language zh-CN --role title --text "实际活动题名"
python scripts/inventory_inputs.py INPUT_FOLDER --hash --output input-manifest.json
python scripts/validate_brief.py brief.yaml --json
python scripts/validate_delivery.py brief.yaml delivery-manifest.json --output-root output --json
```

YAML检查需要PyYAML；可改用JSON。字体调度只需Python标准库。运行语法正确不代表审美通过；新策略当前为trial，缺图与缺类保持未验证。参考图不可直接作为商业主视觉。

- [Composition routes](references/design-routes.md)
- [Font comparison specimens](references/font-proofs.md)


案例借鉴增强版本：reference-learning-v2-2026-10-12

## 动漫／游戏展三案例生成要求

本类生成前必须读取[主视觉效果、视觉风格与文字排版借鉴](references/case-guided-generation.md)并实际看图。优先以本轮选定案例中适配的一例指导生成，三个维度分别落实到提示、字体与真实文案排版、成稿对照；用户新参考或限定范围优先。

动漫与游戏展补充版本：anime-game-three-case-v3-2026-10-12

## 动漫／游戏展：严格参考字体与排版

本类任务默认执行[严格参考标准](references/strict-reference-typography.md)：先选择最佳适配文字参考，再按实际原图锁定各角色字体、比例、字距、换行及图文位置，制作并列对照并记录必要差异。字体覆盖检查与默认候选不代表匹配成功。

动漫与游戏展字体排版版本：anime-game-strict-reference-type-v4-2026-10-13
