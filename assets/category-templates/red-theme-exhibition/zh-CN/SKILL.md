---
name: red-theme-poster-zh
description: 红色文化/党史主题展览海报的中文类别模块。负责叙事、历史溯源、策展与视觉传播平衡、本地安装的真实字体选择、分类QA；供 cultural-event-poster 总 Skill 合并。
---
# 红色主题海报 — 中文版 ZH

## 类型及调用边界
- 仅由总 Skill 分类器在确认 `red-theme-exhibition` 后加载，不自行覆盖总 Skill 分类、事实母本及 Gate。
- 默认输出语言：简体中文。双语版共享已核实事实及视觉主题，但分别排版，不能只做换字。

## 必须阅读
1. `references/red-theme-exhibition.md`：叙事与真实性、策展结构、防模板化、生成前确认。
2. `references/red-theme-typography.md`：宋、黑、文楷、毛笔字体的角色分工与中英文版式。
3. `references/red-theme-qa.md`：类别 QA、失败回退。
4. `references/font-manifest.json`：九份已随包字体的实际共享路径、hash、许可；按字体策略文件将提示计划及排版绑定到真实文件。

## 核心执行
Brief 核实 → 总 Skill 分类 Gate → 叙事选择 → 历史证据表 → 展览身份与策展单元 → 视觉与字体系 → 用户明确确认 Gate → 无最终文字主视觉 → 可控工具加载真实字体排版 → QA → 定向回退。
- 未核验历史依据不可宣称真实史料；未确认方案不应生成正式海报。
- 提示计划的字体字段用 `scripts/resolve_font.py` 解析并核对真实标题，保存绝对字体路径和hash；图片模型输出不等于已应用字体，排版阶段须通过 HTML/SVG/Pillow 等显式加载返回文件。
- 字体检查：运行 `python scripts/check_fonts.py`；真实字体样张：运行 `python scripts/render_font_sample.py`。两者不是完整海报生成功能。

## 交付边界
此包为可合并的类别 Skill，不是总 Skill 的完整可运行替代品。组员应依 `README_合并与验证.md` 合并资源和规则，并完成 Codex 端到端渲染验证。
