---
name: brand-pop-up-poster-en-fixed-v2
description: Toy / brand pop-up poster English standalone test Skill for validating a fixed template before merging back into the master cultural-event-poster Skill.
---
# Toy / Brand Pop-up Poster — English Standalone Test Skill (Fixed Template Edition)

## Single purpose
This package is only for one purpose:
**to verify whether the toy / brand pop-up category can reliably follow a fixed poster template.**

It is not the master Skill. It does not replace global classification, fact management, or other event categories.

## Default mode
When the user asks to “test the brand pop-up template”, “check whether the template is fixed”, or “do not freestyle the layout”, enter:
**Fixed Template Test Mode**.

In this mode:
1. Use `Character-Centered Fixed Template V2` by default.
2. Do not change the core composition logic.
3. Only swap content, color, and text within the defined zones.
4. If the user says “report first, do not generate the poster yet”, stop before rendering.

## Required reading order
1. `references/brand-pop-up.md`
2. `references/brand-pop-up-fixed-template.md`
3. `references/brand-pop-up-typography.md`
4. `references/brand-pop-up-qa.md`
5. `references/font-manifest.json`

## Workflow for the fixed-template test
### A. Decide first, render later
Before rendering, report:
1. identified activity type
2. selected template
3. selected color scheme
4. selected font system
5. whether the provided assets are sufficient

If the user explicitly says “do not generate yet”, stop here.

### B. Generate only after confirmation
Only after confirmation, continue with:
fact check → template application → key visual generation / asset selection → real-font typesetting → QA.

## Required output fields
Every test should report:
- `activity_type`
- `template_name`
- `language`
- `color_scheme`
- `title_font`
- `meta_font`
- `hero_strategy`
- `qa_focus`

## Hard constraints
- Do not turn one category into a completely different free-form composition.
- Do not allow the hero character to clash heavily with the dominant palette.
- Do not make the bottom panel an irregular decorative shape by default; use a **dark semi-transparent rounded rectangle**.
- Icons are optional, not mandatory; when the information load is high, remove icons and use centered text.
- Do not invent collaborations, gifts, inventory numbers, or authorization claims.
- For real brands / IP, prefer real recognizable names and include a clear “concept event / unofficial release” notice when needed.


## cultural-event-poster integration

本模块已接入总包对应品牌快闪类别。按本语言提示执行固定五区模板，不再运行旧多构图自由策略。总母本、Gate与中英两张完整海报交付保持；已确认事项直接沿用。此类别固定1080×1440、3:4，作为类别规格例外写入项目brief，其他类别默认规格不变。字体从本目录references/font-manifest.json解析真实共享文件并核验SHA与字形；不要按独立包的fonts路径寻找不存在的文件。示例和README不是新活动事实或发布授权。
