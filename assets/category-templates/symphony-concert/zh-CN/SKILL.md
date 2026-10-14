---
name: cultural-traditional-performance-poster
description: "为传统与古典演出整理资料、制定中英文海报策略、调用随包字体、执行生成前确认与图面迭代。按具体小类与真实内容决策；不用于商品营销。"
---

# 传统与古典演出海报补充

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

- [chinese-opera](references/subtypes/chinese-opera.md)
- [xiangsheng](references/subtypes/xiangsheng.md)
- [symphony](references/subtypes/symphony.md)

## 执行顺序

资料盘点 → 事实母本与冲突检查 → 主类型与小类 → 文化／主题命题与方向 → 字体样张和五项确认 → 无正式文字的主视觉（原创题名图形例外见案例转化说明） → 可控排版与语言重排 → 事实、字形、图面和规格QA → 用户审核及定向修订。用户已明确确认的决定直接沿用，未确认事项不自行填为人审通过。

用户只改文字关系时保留认可的主视觉；不要随机生成。不得虚构活动事实、官方身份、字体名称、授权、二维码或观众反馈。字体与题名选择按条件，不固化某张参考的画风。

## 实体资源与检查

- [Font catalog](assets/fonts/catalog.json) · [Role profiles](assets/fonts/role-profiles.json)
- [Chinese role index](assets/fonts/roles-zh-CN.md) · [English role index](assets/fonts/roles-en.md)
- [Pre-generation record](assets/pre-generation-review-template.json) · [Review record](assets/review-record-template.json)

```powershell
python scripts/font_engine.py --profile opera-classical --language zh-CN --role title --text "实际活动题名"
python scripts/inventory_inputs.py INPUT_FOLDER --hash --output input-manifest.json
python scripts/validate_brief.py brief.yaml --json
python scripts/validate_delivery.py brief.yaml delivery-manifest.json --output-root output --json
```

YAML检查需要PyYAML；可改用JSON。字体调度只需Python标准库。运行语法正确不代表审美通过；新策略当前为trial，缺图与缺类保持未验证。参考图不可直接作为商业主视觉。

- [Composition routes](references/design-routes.md)
- [Font comparison specimens](references/font-proofs.md)


案例借鉴增强版本：reference-learning-v2-2026-10-12

- [主视觉效果／视觉风格／文字排版的案例借鉴](references/case-guided-generation.md)

传统与古典演出补充版本：traditional-case-guided-v3-2026-10-12
