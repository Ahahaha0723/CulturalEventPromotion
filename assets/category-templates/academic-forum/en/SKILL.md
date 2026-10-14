---
name: academic-forum-fixed-type-en
description: Create English academic forum posters with a locked 4-to-5 typography grid, mandatory Playball-Regular H1 and one sans-serif family for all other text.
---

# English academic forum fixed typography

Reduce H1 interline whitespace by 50% using `interline_gap_factor: 0.5`. Preserve fitted size and glyph shapes, do not halve the full line advance or compound reductions. All non-H1 positions and spacing remain unchanged.

Use with the parent content master and QA. Read [fixed-layout.md](../references/fixed-layout.md), [coordinates](../references/layout-spec.json), and inspect the [reference](../references/left-headline-reference.jpg).

English H1 MUST load the bundled user-provided [Playball-Regular.ttf](../../../fonts/playball/Playball-Regular.ttf), regardless of subject. Never reuse the Chinese Slidexiaxing/VonwaonBitmap selection for English. Use exactly one font file and a shared fitted size for the complete H1 group, with real glyph measurements and the 50% interline whitespace rule. Do not simulate, mix, distort or silently substitute the font. Missing font or glyphs blocks export. Every non-H1 element, including the full forum name H2, uses HarmonyOS Sans SC with real weight and size changes only. This is intentionally a different title font from the Chinese poster.

Follow the NEW reference: dominant upper-left H1 thematic words, the full forum name below in sans serif, compact sourced auxiliary theme, stacked lower-left information groups, and a separate lower-right location/form/date cluster with two large date nodes and an independent year. No rotated rails, upper-right title, editorial columns, ovals or full-width rules. Keep complete identity and conditions; working translations remain pending. Do not add decorative Chinese.

The reference locks typography only, not white/black colors. Use a visibly colored single-hue background and coordinated, readable lettering. Inspect suitable source-pack imagery, extract its main visual hue and prepare a blurred tonal background with an image-editing tool; without images, use a theme-derived tonal gradient. Never treat the typography reference as a source-pack background image. Share the background and palette with Chinese while keeping all locked text positions and font rules.

Remove displayed title/forum-name years when other visible information contains a year. Retain source names and date years. Establish compact line spacing from the NEW reference; do not halve old-frame leading again. Positive glyph gaps remain 0.5 of natural measurements without glyph scaling. The full forum name H2 and ALL non-H1 text use HarmonyOS Sans SC.

Execute the fixed-layout prompt and English [render.py](../scripts/render.py) view. Run [check_assets.py](../scripts/check_assets.py) first. Deliver a complete 2400x3000 English PNG alongside Chinese; keep source, decisions, measurements and QA in the workspace. No free layout or former central hero image.
