# 红色主题 / 党史展览 Skill 模块｜合并与验证说明


> 当前合并版：九份字体已随总包提供，马善政／志莽行书原成员哈希匹配。以 `references/font-manifest.json` 的共享路径为准；本机无需再次执行安装脚本。提示计划与排版文件按 `references/red-theme-typography.md` 的绑定步骤执行。下文安装步骤仅保留原成员包历史说明。

本包是独立的**类别模块**，供小组整合到 `cultural-event-poster`，**不替代**总 Skill 的 SKILL.md / Gate / 文件解析与工具路由。中文与英文分别打包，便于与同学作业形式一致。

## 内容
- `SKILL.md`：类别入口；`references/red-theme-exhibition.md`：红色主题专属设计规则。
- `references/red-theme-typography.md`：字体策略与双语排版。
- `references/red-theme-qa.md`：分类 QA 与定向回退。
- `references/font-manifest.json`：字体相对路径、字重、实际 SHA-256、版权文档。
- `fonts/`：需通过 `scripts/install_local_fonts.py` 从用户自行保管的下载包在本地安装；此 ZIP 不含字体二进制文件。
- `scripts/check_fonts.py`：字体文件 hash、可读性和基本中英字形覆盖自检；`scripts/render_font_sample.py`：用真实包内字体输出 PNG 样张，证明字形实际被绘制（**并非完整海报生成器**）。

## 合并路径
1. 将 `references/red-theme-exhibition.md` 的规则合并入主 Skill 的 `references/activity-types/red-theme-exhibition.md`，避免直接覆盖其它组员改动。
2. 将本包字体合并到主 Skill 的 `assets/fonts/red-theme/`，同步调整 `font-manifest.json` 的相对路径，避免在主文件夹中查找错误。
3. 将本包排版和 QA 规则分别整合到总 Skill 的双语排版与类别 QA 流程；脚本可作为辅助测试，不得声称已接入总 Skill 的渲染器。
4. 总 Skill 必须落实分类确认和设计方向确认 Gate。不同类别保持通用 Gate 逻辑一致，不要各写一套互相冲突的主流程。

## 如何本地检查
安装 `fonttools` 和 `Pillow`，在解压后的模块根目录运行：
`python scripts/check_fonts.py`
`python scripts/render_font_sample.py`

## 已知边界
- 本包验证字体文件、来源许可随附和基本字形渲染。真实的 Codex 调用路径、完整海报流程及 Gate 是否生效，仍需在合并后的环境做端到端测试。
- 两个包是独立交付候选件，组员合并时只需合并相同资源一次，避免重复占用空间。
- 历史事实由用户原始 Brief + 可核实文献决定，不得生成虚构的历史证明/照片，或宣称模拟活动是真实举办。
