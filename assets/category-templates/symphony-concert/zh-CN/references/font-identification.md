# 字体识别、候选与下载

本次没有任何原字体达到“可确证身份”标准：参考均为位图，没有设计源文件的字体元数据或设计者确认。下表记录可见风格与实际下载的开放候选；风格置信度与字体身份置信度分开。定制字标的候选只是可辨构字起点，不保证复现原图。

|Case|Role|Observed evidence|Identity status|Bundled candidates|
|---|---|---|---|---|
|演出-053|title|流光之海：细宋／明朝风格，横细竖粗与三角衬线；具体字体未知|unverified-original|source-han-serif-cn|
|演出-053|subtitle|中部Latin：斜体衬线与宽字距，逐字散置|unverified-original|spectral|
|演出-053|body|正文与演出者：宋体／衬线，常规字重；英文底部品牌为独立标志|unverified-original|source-han-serif-cn / spectral|
|演出-053|numeric|日期：衬线数字，间隔与字重轻|unverified-original|spectral|
|演出-065|title|山海·大观：稳健粗黑体竖排，清晰直线骨架|unverified-original|source-han-sans-cn|
|演出-065|subtitle|东方融合音乐会与AMS&DaGuan：无衬线，大小与方向有分工|unverified-original|source-han-sans-cn / barlow|
|演出-065|body|嘉宾／地点／英文说明：常规无衬线，小字功能区|unverified-original|source-han-sans-cn / barlow|
|演出-065|numeric|场次与时间：常规无衬线数字，多组时间按活动区分|unverified-original|barlow|
|演出-109|title|颜真卿：书写性中文题名，笔画与组合可能定制|custom-lettering-unconfirmed|ma-shan-zheng|
|演出-109|subtitle|英文人名与演出形式：高对比衬线、紧密行组|unverified-original|spectral|
|演出-109|body|演职与地点票务：中文宋体、小字；部分像素不足|unverified-original|source-han-serif-cn|
|演出-109|numeric|场次：高对比衬线数字，与年月分层|unverified-original|spectral|

完整机器记录：assets/font-identification.json；CSV可筛选角色。实体字体与许可证：assets/fonts；按角色调用见font-routing.md。识别证据：笔画对比、宽窄、端点、数字与改造；未有原文件时不输出虚假的“精确匹配率”。提供可编辑源文件或设计规范后，可替换候选并记录确认依据。

[Font comparisons and specimens](font-proofs.md)
