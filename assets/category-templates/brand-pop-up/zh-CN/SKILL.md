---
name: brand-pop-up-poster-zh-fixed-v2
description: 潮玩/品牌快闪海报中文独立测试 Skill。目标是验证固定模板能否稳定执行，而不是替代总 Skill。
---
# 潮玩 / 品牌快闪海报 — 中文独立测试 Skill（固定模板版）

## 本 Skill 的唯一目标
本包只做一件事：
**验证“潮玩 / 品牌快闪”这一文化活动类别，是否能稳定执行固定模板。**

它不是总 Skill，也不负责总分类枚举、全局 Gate、事实母本统筹或其他活动类别。
如果测试结果满意，再由组员把本类别规则合并回总 Skill。

## 默认测试模式
当用户说“测试潮玩/品牌快闪模板”“先判断模板是否固定”“先不要自由发挥”时，默认进入：
**Fixed Template Test Mode（固定模板测试模式）**。

在该模式下：
1. 优先使用 `Character-Centered Fixed Template V2`。
2. 不随意更换构图逻辑。
3. 仅允许在已定义区域内替换内容、颜色与文字。
4. 若用户先要求“只汇报判断，不生成海报”，必须停在汇报阶段，不得自动渲染。

## 强制阅读顺序
1. `references/brand-pop-up.md`
2. `references/brand-pop-up-fixed-template.md`
3. `references/brand-pop-up-typography.md`
4. `references/brand-pop-up-qa.md`
5. `references/font-manifest.json`

## 固定模板版的工作流
### A. 先判断，后出图
先输出：
1. 当前是否属于潮玩 / 品牌快闪类别
2. 是否适合使用固定模板
3. 选用的色彩方案
4. 选用的字体方案
5. 是否具备足够素材进入渲染

若用户明确说“先不要生成海报”，则停止在这里。

### B. 确认后再生成
只有在用户确认继续后，才进入：
事实核对 → 模板套用 → 主视觉生成 / 选图 → 真实字体排版 → QA。

## 输出要求
每次测试都必须明确汇报以下字段：
- `activity_type`
- `template_name`
- `language`
- `color_scheme`
- `title_font`
- `meta_font`
- `hero_strategy`
- `qa_focus`

## 关键约束
- 不得把“同一类活动”又跑成完全不同的自由构图。
- 不得让主角色颜色与整张海报主色严重冲突。
- 不得把底部信息板做成花哨异形；默认使用**深色半透明平面圆角矩形**。
- 不得把图标设为强制项；当信息偏多时，默认删去 icon，改用居中文本。
- 不得默认虚构联名、赠品、库存、授权关系。
- 涉及真实品牌/IP时，应优先使用真实品牌名称与明确的“概念活动 / 非官方”标注规则。


## cultural-event-poster integration

本模块已接入总包对应品牌快闪类别。按本语言提示执行固定五区模板，不再运行旧多构图自由策略。总母本、Gate与中英两张完整海报交付保持；已确认事项直接沿用。此类别固定1080×1440、3:4，作为类别规格例外写入项目brief，其他类别默认规格不变。字体从本目录references/font-manifest.json解析真实共享文件并核验SHA与字形；不要按独立包的fonts路径寻找不存在的文件。示例和README不是新活动事实或发布授权。
