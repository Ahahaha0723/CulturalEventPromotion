# 按角色的字体调度索引

以下是候选顺序，不是强制美学结论。字体实体按字族存储，同一字体不重复复制到各角色目录。

|Profile|Role|Ordered font files|
|---|---|---|
|anime-character|主标题|`zcool-qingke-huangyou/ZCOOLQingKeHuangYou-Regular.ttf` → `zcool-kuaile/ZCOOLKuaiLe-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Heavy.otf`|
|anime-character|副标题／活动形式|`source-han-sans-cn/SourceHanSansCN-Medium.otf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|anime-character|正文／功能信息|`source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|anime-character|日期／数字|`barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|主标题|`source-han-sans-cn/SourceHanSansCN-Heavy.otf` → `zcool-qingke-huangyou/ZCOOLQingKeHuangYou-Regular.ttf`|
|game-modular|副标题／活动形式|`source-han-sans-cn/SourceHanSansCN-Medium.otf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|正文／功能信息|`source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|日期／数字|`rajdhani/Rajdhani-Bold.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|ip-portrait|主标题|`source-han-sans-cn/SourceHanSansCN-Heavy.otf` → `zcool-qingke-huangyou/ZCOOLQingKeHuangYou-Regular.ttf`|
|ip-portrait|副标题／活动形式|`source-han-sans-cn/SourceHanSansCN-Medium.otf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|ip-portrait|正文／功能信息|`source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|ip-portrait|日期／数字|`barlow-condensed/BarlowCondensed-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf` → `noto-sans-thai/NotoSansThai[wdth,wght].ttf`|
|artist-alley|主标题|`source-han-sans-cn/SourceHanSansCN-Heavy.otf` → `zcool-kuaile/ZCOOLKuaiLe-Regular.ttf`|
|artist-alley|副标题／活动形式|`source-han-sans-cn/SourceHanSansCN-Medium.otf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|artist-alley|正文／功能信息|`source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|artist-alley|日期／数字|`barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|

## artist-signature

Creator signature: en title → Spectral Italic; zh-CN title → Source Han Sans CN Medium. Actual files and coverage are dispatched through role-profiles.json; font identity remains a substitute, not a source match. Body/date use their own roles. For a bold italic booth code use artist-alley / en / subtitle (Barlow BoldItalic first; compare and lock actual width).

## Strict reference candidates

reference-022: heavy geometric identity/date. reference-052: heavy condensed heading. reference-053: wide heavy event mark and normal-width Barlow BoldItalic table text. Artist signature retains artist-signature / en / title. These profiles provide candidates only; explicit reference comparison precedes selection. scripts/reference_font_check.py verifies a locked file without silent fallback.
