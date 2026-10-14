# 字体识别、候选与下载

本次没有任何原字体达到“可确证身份”标准：参考均为位图，没有设计源文件的字体元数据或设计者确认。下表记录可见风格与实际下载的开放候选；风格置信度与字体身份置信度分开。定制字标的候选只是可辨构字起点，不保证复现原图。

|Case|Role|Observed evidence|Identity status|Bundled candidates|
|---|---|---|---|---|
|潮流-014|title|OTAKUTHON：宽重斜体无衬线字标；特殊字形作为品牌资产|brand-lettering-unconfirmed|barlow|
|潮流-014|subtitle|法英副标题：竖向比例较长的斜体无衬线|unverified-original|barlow-condensed|
|潮流-014|body|介绍与场馆：细窄／粗窄无衬线，原图部分低对比|unverified-original|barlow-condensed|
|潮流-014|numeric|超大日期：极窄重黑数字，0有特殊斜向内白|modified-or-font-unconfirmed|anton / bebas-neue|
|潮流-022|title|MANGA字标：几何宽重、内白改造；BARCELONA紧密黑体|brand-lettering-unconfirmed|archivo-black|
|潮流-022|subtitle|未见独立叙述副标题，活动身份由字标组合承载|not-applicable|barlow|
|潮流-022|body|底部场馆／官网：紧密粗无衬线，小字需另做可读检查|unverified-original|barlow / barlow-condensed|
|潮流-022|numeric|日期：粗无衬线与多语言月份，不照抄字体身份|unverified-original|barlow|
|潮流-044|all|文件缺失|missing-image||
|潮流-052|title|ARCANE WORLD：超窄重无衬线，局部破损和滴落效果|modified-or-font-unconfirmed|bebas-neue / anton|
|潮流-052|subtitle|地点Latin为大写衬线，泰文混排；非纯英文稿|unverified-original|spectral / noto-sans-thai|
|潮流-052|body|泰文地点／日期：稳健无衬线；品牌Logo另为资产|unverified-original|noto-sans-thai|
|潮流-052|numeric|泰文日期行含数字，原家族不能确证|unverified-original|noto-sans-thai / barlow|
|潮流-053|title|NYCC：宽重无衬线；上方创作者名用高对比斜体衬线|unverified-original|archivo-black / spectral|
|潮流-053|subtitle|Table F20／Artist Alley：粗斜无衬线，字号差明显|unverified-original|barlow|
|潮流-053|body|右下地点日期：紧密小型无衬线，像素不足以确证家族|unverified-original|barlow|
|潮流-053|numeric|摊位F20与文字同一斜体组；日期小字独立|unverified-original|barlow|

完整机器记录：assets/font-identification.json；CSV可筛选角色。实体字体与许可证：assets/fonts；按角色调用见font-routing.md。识别证据：笔画对比、宽窄、端点、数字与改造；未有原文件时不输出虚假的“精确匹配率”。提供可编辑源文件或设计规范后，可替换候选并记录确认依据。

[Font comparisons and specimens](font-proofs.md)

## 严格字体与排版标准

生成及文字修订前读取[最佳适配参考的字体与排版锁定](strict-reference-typography.md)，实际看图、对照样张并按角色锁定字形与布局。旧候选次序不能代替匹配判断；新增斜体、字族或布局变动须有本案／原图依据。
