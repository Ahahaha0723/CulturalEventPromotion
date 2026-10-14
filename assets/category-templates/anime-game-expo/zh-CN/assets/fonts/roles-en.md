# Font dispatch by role

Ordered candidates, not aesthetic mandates. Binaries are stored by family rather than duplicated in role folders.

|Profile|Role|Ordered font files|
|---|---|---|
|anime-character|title|`archivo-black/ArchivoBlack-Regular.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Heavy.otf`|
|anime-character|subtitle|`barlow-condensed/BarlowCondensed-Bold.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|anime-character|body|`barlow/Barlow-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|anime-character|numeric|`barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|title|`rajdhani/Rajdhani-Bold.ttf` → `archivo-black/ArchivoBlack-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Heavy.otf`|
|game-modular|subtitle|`rajdhani/Rajdhani-Regular.ttf` → `barlow/Barlow-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|body|`barlow/Barlow-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|game-modular|numeric|`rajdhani/Rajdhani-Bold.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|ip-portrait|title|`bebas-neue/BebasNeue-Regular.ttf` → `anton/Anton-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Heavy.otf`|
|ip-portrait|subtitle|`spectral/Spectral-SemiBold.ttf` → `barlow-condensed/BarlowCondensed-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf` → `noto-sans-thai/NotoSansThai[wdth,wght].ttf`|
|ip-portrait|body|`barlow/Barlow-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf` → `noto-sans-thai/NotoSansThai[wdth,wght].ttf`|
|ip-portrait|numeric|`barlow-condensed/BarlowCondensed-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf` → `noto-sans-thai/NotoSansThai[wdth,wght].ttf`|
|artist-alley|title|`archivo-black/ArchivoBlack-Regular.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Heavy.otf`|
|artist-alley|subtitle|`barlow-condensed/BarlowCondensed-BoldItalic.ttf` → `barlow/Barlow-Italic.ttf` → `barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|artist-alley|body|`barlow/Barlow-Regular.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|
|artist-alley|numeric|`barlow/Barlow-Bold.ttf` → `source-han-sans-cn/SourceHanSansCN-Regular.otf`|

## artist-signature

Creator signature: en title → Spectral Italic; zh-CN title → Source Han Sans CN Medium. Actual files and coverage are dispatched through role-profiles.json; font identity remains a substitute, not a source match. Body/date use their own roles. For a bold italic booth code use artist-alley / en / subtitle (Barlow BoldItalic first; compare and lock actual width).

## Strict reference candidates

reference-022: heavy geometric identity/date. reference-052: heavy condensed heading. reference-053: wide heavy event mark and normal-width Barlow BoldItalic table text. Artist signature retains artist-signature / en / title. These profiles provide candidates only; explicit reference comparison precedes selection. scripts/reference_font_check.py verifies a locked file without silent fallback.
