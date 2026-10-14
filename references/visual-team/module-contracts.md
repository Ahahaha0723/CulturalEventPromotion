# 组员模块接口

主skill覆盖完整流程；以下是统一数据接口，可接入组员的活动定位、文案、素材、视觉、制作、评价专项规则。接口存在不代表专项成果已收齐。字段可按实际任务扩展，用户要求与已确认事实贯穿全流程。

|对象|输入／输出内容|负责环节|
|---|---|---|
|posterBrief|大类、小类、题名、内容、受众、任务、情绪、文化线索、事实、媒介、约束、素材、confirmation|需求接收与共享事实|
|positioning|六维定位、定位句、锚点、信息优先级、待核验项|活动定位|
|copyPlan|题名、活动形式、亮点、事实文本、行动、附加说明、lockedFields|文案与信息组织|
|assetPlan|来源、身份、可用条件、素材角色、主视觉制作需求、待核验项|素材与制作准备|
|visualPlan|主策略、支撑策略、表达方向、调用条件、来源、各案图文构成、风险|视觉风格|
|production|实际工具、稳定方案ID、主视觉文件、排版文件、预览、尺寸与版本、制作状态|生成与排版|
|review|硬性检查、五维证据与可选自评分、保留淘汰、修正结果、推荐及限制|评价与修正|
|delivery|交付路径、成品／提案状态、用户要求的格式、预览、待核验事项|交付|

## 统一事实状态

字段事实写入confirmation：用户确认、已有资料支持、暂定假设、明确占位或待核验。定位推导与事实状态分开；后一个模块不能因为收到字段就自动把它变为已确认。文案、日期、机构或媒介变更时通知相关环节重新核对。

## 命名与版本

策略交接用visual.S01—visual.S08，表达方向用direction.M01—direction.M08；活动taxonomyVersion使用既有culture-activity-v3，规则版本单独保存。各方案有稳定ID，显示字母随机变化时不替代内部标识。

posterBrief保留schemaVersion与来源；同题三案引用同一份事实快照。review里区分designSelfAssessment与audienceEvidence，后一字段未测时为空或注明未验证。

## 合并约定

- 主SKILL.md只保留流程、优先级、输入输出与资料调用入口，组员详细规则放入对应references。
- 上游模块提出内容价值、文案或素材需求，下游反馈缺事实、图面容量或可读问题；通过共享brief解决，不各自改事实。
- 用户已确认的要求和事实优先；必要信息正确与可用优先；在这些条件内比较创意与美感。
- 每条规则保留条件与证据等级。病例观察、团队选择、设计推导和观众测量分别记录。
- 有真正工具脚本、模板或品牌资产时随模块提交依赖和调用方法；不能把尚未提供的文件写进主skill作为已可用资源。

## 汇总输出示意

```json
{
  "schemaVersion": "culture-poster-project-v1",
  "stage": "proposal",
  "positioning": {"status": "已形成定位，事实待确认"},
  "visualPlan": {
    "mainStrategy": "visual.S02",
    "supportStrategies": ["visual.S01"],
    "directions": ["direction.M01", "direction.M02", "direction.M03"]
  },
  "production": {"artifacts": []},
  "review": {"designSelfAssessment": null, "audienceEvidence": null},
  "delivery": {"finalArtifacts": [], "status": "方向提案；未制作成品"}
}
```

该示意说明提案状态的诚实交接，不代表任务可以止于示意。用户要求成品且工具资料具备时继续制作、预览、修正并交付。
