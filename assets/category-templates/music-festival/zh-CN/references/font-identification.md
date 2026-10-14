# 字体识别、候选与下载

本次没有任何原字体达到“可确证身份”标准：参考均为位图，没有设计源文件的字体元数据或设计者确认。下表记录可见风格与实际下载的开放候选；风格置信度与字体身份置信度分开。定制字标的候选只是可辨构字起点，不保证复现原图。

|Case|Role|Observed evidence|Identity status|Bundled candidates|
|---|---|---|---|---|
|演出-001|title|FEEL主字标：尖刺、金属轮廓、颗粒处理；疑似定制／改造|custom-lettering-unconfirmed|archivo-black|
|演出-001|subtitle|阵容：粗重中文字与拉丁厚重衬线；可见明显字级与组合|unverified-original|source-han-serif-cn / source-han-sans-cn|
|演出-001|body|主办／场馆与细节：常规小字，精确家族无法由像素确定|unverified-original|source-han-sans-cn / barlow|
|演出-001|numeric|日期为清晰常规数字；日与星期的字级独立|unverified-original|barlow|
|演出-029|title|AHTD：宽重无衬线，A含特殊缺口；可能有图形改造|modified-or-font-unconfirmed|archivo-black|
|演出-029|subtitle|城市／巡演说明：重斜体与紧窄竖向比例并置|unverified-original|barlow / barlow-condensed|
|演出-029|body|场馆与说明为细长窄体，局部有描边处理|unverified-original|barlow-condensed / bebas-neue|
|演出-029|numeric|日期／年份为竖向比例明显的窄体数字|unverified-original|bebas-neue / barlow-condensed|
|演出-039|title|黑白森林：高度改造的尖刺中文轮廓、发光描边；非可确认标准字族|custom-lettering-unconfirmed|source-han-sans-cn|
|演出-039|subtitle|英文补充题名：小型粗无衬线，身份未证实|unverified-original|barlow|
|演出-039|body|边缘英文与底部中文：紧密小字／无衬线，部分像素不足|unverified-original|barlow / source-han-sans-cn|
|演出-039|numeric|底部日期时刻：较粗数字；字重与大小用于定位|unverified-original|barlow|

完整机器记录：assets/font-identification.json；CSV可筛选角色。实体字体与许可证：assets/fonts；按角色调用见font-routing.md。识别证据：笔画对比、宽窄、端点、数字与改造；未有原文件时不输出虚假的“精确匹配率”。提供可编辑源文件或设计规范后，可替换候选并记录确认依据。

[Font comparisons and specimens](font-proofs.md)
