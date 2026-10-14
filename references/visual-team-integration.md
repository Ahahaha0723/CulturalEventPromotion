# 视觉团队模块接入说明

本文件把视觉团队提供的八大类策略、八种表达方向、第二轮案例证据和修正规则接入当前 Skill 的 14 个活动类型策略。事实母本、双语确认、素材授权和最终 QA 仍由当前 Skill 的共享规则管理。

## 使用顺序

1. 从内容母本确认活动事实、主类型、次类型、受众、传播任务和媒介。
2. 读取对应的 `references/activity-types/*.md`，确定该活动的信息优先级、字体方向和文化风险。
3. 读取 [活动视觉定位表](visual-team/activity-positioning.md)，形成内容锚点、受众、任务、主辅气质、文化线索和媒介条件。
4. 从 [八种表达方向](visual-team/visual-directions.md) 选候选机制，并按 [14 类与视觉策略映射](#14-类与视觉策略映射) 读取 [类别路由](visual-team/category-routing.md) 和 [视觉策略库](visual-team/visual-strategies.md)。通常使用一条主策略，最多两条支撑策略。
5. 如需案例依据，只从 [案例证据库](visual-team/case-evidence.json) 读取相关案例，并查看对应的 `assets/reference-posters/` 图片；不一次性加载全部案例。
6. 生成与排版遵循 [素材、生成与精确排版](visual-team/assets-and-generation.md)；同题择优遵循 [评价与验收](visual-team/selection-and-quality.md)，修正遵循 [修正规则](visual-team/repair-rules.md)。

## 14 类与视觉策略映射

| 活动类型策略文件 | 视觉团队大类 | 建议策略顺序 | 证据口径 |
|---|---|---|---|
| `traditional-cultural-exhibition.md` | 展览 | S02 → S01 → S03 | 文物/考古有参考；非遗工艺部分为设计推导 |
| `red-theme-exhibition.md` | 展览·红色主题 | S02 → S06 → S05 | 颜色策略为条件调用，历史事实必须核验 |
| `symphony-concert.md` | 演出 | S02 → S01 → S07 | 交响/戏曲主要为设计推导；民族音乐有单人记录 |
| `festival-lantern.md` | 节庆 | S02 → S06 → S05 | 节庆案例可借机制，不代表完整活动信息 |
| `university-anniversary.md` | 节庆·校庆 | S02 → S01 → S06 | 有单人记录，周年与机构事实需核对 |
| `sports-event.md` | 体育 | S02 → S01 → S07 | 对抗赛事参考有限，票务和赛事信息独立核验 |
| `art-district.md` | 街区 | S05 → S01 → S02，或 S06 → S02 → S05 | 多点位优先信息模块；参与型活动可强化地方线索 |
| `academic-forum.md` | 学术 | S01 → S05 → S07 | 字体只作局部表达，不能替代议题与信息 |
| `workshop.md` | 学术·工作坊 | 按子类使用 S01/S02/S05/S07 | 艺术疗愈有5人记录；书籍印刷、设计建筑证据较少；其他子类为设计推导 |
| `brand-pop-up.md` | 市集/潮流 | S06 → S05 → S02 | 快闪参考为部分认可，品牌授权独立确认 |
| `anime-game-expo.md` | 潮流 | S04 → S06/S07 → S05 | 角色场景证据有限，需限制受众和 IP 条件 |
| `music-festival.md` | 演出 | S05 → S08 → S06 | 大型音乐节主要为设计推导；长阵容优先分组 |
| `heritage-market.md` | 市集 | S02 → S05 → S06 | 主要为设计推导，不把工作坊机制当市集共识 |
| `digital-art-exhibition.md` | 展览 | S02 → S07 → S01 | 数字艺术主要为设计推导，不冒充艺术家作品 |

## 证据与优先级

- 用户当前要求和已确认事实最高优先。
- 当前 Skill 的内容母本、双语、权限、版权和 QA 规则高于视觉案例中的局部建议。
- 视觉团队第二轮数据是团队偏好和机制观察，不是公众效果测试，也不是模型训练结果。
- `S01`—`S08` 是视觉策略，`M01`—`M08` 是表达方向；两套命名不能混用。
- 32 张参考图只用于分析主题锚点、层级、材料、字体和图文关系；除非授权明确，不直接作为新海报素材。
- 五项建议权重为定位匹配 25%、信息传达 25%、视觉完成度 20%、概念独特性 20%、场景适配 10%；这是设计自检起点，不是经过公众测试校准的合格线。

## 统一接口

需要结构化交接时读取 [模块接口](visual-team/module-contracts.md)，沿用：

`posterBrief → positioning → copyPlan → assetPlan → visualPlan → production → review → delivery`

这些对象应从同一内容母本派生；下游模块不得自行修改事实确认状态。
