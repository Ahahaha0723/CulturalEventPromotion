# 潮玩／品牌快闪类别 Skill — 合并说明（核查修订版）

此包为供 `cultural-event-poster` 总 Skill 合并的**类别参考包**，不是已集成到总 Skill 的最终可运行成品；请勿将其中独立 SKILL.md 当作主 Skill 的替代文件。

## 已核查
- 7 个字体成品文件都在包内，manifest 中 SHA-256 与包内文件一致；许可文本文件存在。
- 包含：思源黑体 SC Regular/Bold/Heavy；ChillRoundF；Kosefont-JP；Nunito Regular/Bold。
- **得意黑没有字体成品文件**，为候选而非可用字体。
- Kosefont-JP 是日文字形版本，尚未确认每个简体中文字形都符合预期。

## 合并指引
1. 将 `references/brand-pop-up.md` 的类别规则合并到总 Skill 对应类型规则，避免无条件覆盖旧文件。
2. 合并 `brand-pop-up-typography.md`、`brand-pop-up-qa.md` 的规则；接入总 QA、双语排版及 Gate，避免建立竞争的主流程。
3. 将 `fonts/` 内文件复制到总 Skill 指定字体资源路径，并将 `font-manifest.json` 中的 `file` 和 `license_file` 按新根目录重写。
4. 总 Skill 的正式渲染流程需显式调用本地字体文件，先生成不含正式文字的主视觉，再通过可控排版工具加文字。
5. 在 Codex 目标环境做中文、英文各一张端到端海报测试，并保留调用记录和视觉核查结果。此包不提供端到端海报渲染脚本，故不得声称此项测试已通过。

## 相对路径
在本独立包内，`references/font-manifest.json` 中字体路径均相对于包根目录，不能相对于 references 目录解析。

## 测试与授权提示
字体文件哈希验证不等于设计成品验证；许可文件存在不等于所有品牌/IP使用获得授权。真实品牌海报仍需校验素材、Logo及视觉使用许可。
