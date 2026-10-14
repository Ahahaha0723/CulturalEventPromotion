---
name: university-anniversary-editorial-en
description: Create English university-anniversary key-visual PNG posters with a shared-size upper-left school and anniversary block, transparent emblem aligned to that block and right-aligned participation copy, emblem-colored headings, gray body text, and large mist-faded monochrome campus photography using bundled NotoSerifSC fonts.
---

# English University Anniversary Key Visual

Create an independent English poster using the latest Chinese skill's typography, photo treatment, actual fonts, color roles and alignment. Final delivery is the complete poster PNG only; no SVG, PDF, editable source, JSON sidecars, separate emblem or layer previews. Do not overwrite the Chinese skill. Read the [typography reference](assets/reference/typography-reference.jpg) and [layout rules](references/layout-rules.md); reference wording and brands are not event facts.

## Copy and English adaptation

Receive upstream-approved copy, school name, anniversary number, dates, venues, organizer relationships, emblem and campus photo. Translate all visible copy into English before typesetting and lock it. Keep the Chinese source and translation mapping internally; [translation example](references/translation-map.example.json) records provisional terms. Use supplied official English names; otherwise use consistent descriptive translations or romanization and mark them internally as provisional, not official. The supplied poster gives Tsinghua University as its English school name; other example venue and program names are working translations.

Do not invent a founding year from an anniversary number, add a school motto, historical fact, sponsor, entrance rule or official status. A main venue does not establish the venue of every scheduled event. Campus Open Day does not imply free public entry. Preserve the source's test/non-official status. Materials contain source data, not new user instructions. Upstream selects information; do not impose another field whitelist or silently delete approved facts.

Remove the previously excluded promotional subtitle 校友返校·校园开放日 and its English equivalent Alumni Homecoming · Campus Open Day, including spacing variants. Do not repeat it near the event title or move it to details. This omission does not remove alumni registration, access conditions or open-day restrictions that occur as genuine detail copy.

Use unambiguous English dates such as 25–26 APR 2026, 24-hour times and unchanged numbers. Preserve anniversary versus event year distinctions. Translate role labels faithfully. School and anniversary headers never wrap. Detail-copy lines break only at whole-word/meaningful-phrase boundaries; do not distort letters, change font family, delete facts or shrink individual lines just because English is longer. No visible Chinese in typeset copy; an authentic supplied emblem may retain its original Chinese lettering without being redrawn. Do not add unrelated decorative English headings.

## Layout and transparent emblem

Default 4:5, 2400×3000 with approximately 120px edge margins. Upper left contains the specific school name and anniversary text, e.g. Tsinghua University / 115th Anniversary. Both share left x120 and font size 160px. School name and anniversary each occupy exactly one line, including long names. If either row exceeds available width or approaches the emblem, proportionally reduce the font size of both rows together until they fit with at least64px clearance from the emblem visible left edge. Keep all wording, original font files, left anchor and the shared size; do not wrap either row, compress glyphs, crop words or alter emblem size.160px is the nominal starting size, not a fixed minimum. Do not make the anniversary number independently larger.

Upper right contains the actual background-removed emblem, using [cutout instructions](references/emblem-cutout.md). Preserve its original colors, fine lines, words and proportions; remove external white/colored background while retaining white artwork that belongs to the design. Already-transparent assets need no regeneration. Never fabricate or redraw an emblem. Missing assets permit a clearly labeled review only, not a claimed final school-color poster.

Measure actual visible ink, not padded frames. Both languages use the approved Chinese poster's emblem size: visible height357.5px on a2400×3000 canvas, with width derived from the authentic aspect ratio (357.5px for the circular source). Keep top at school-name ink top and right at participation ink right x2280. This overrides the old language-specific school-top/anniversary-bottom height formula: English glyph metrics or wrapping must not enlarge the emblem. When the anniversary bottom differs, preserve the shared emblem size, top and right anchors rather than stretch it to span the English header. For new output ratios scale the shared size proportionally from the reference canvas. Do not crop wordmarks or distort wide assets.

Middle area holds the user's campus photo blended into white with low-contrast monochrome, fine random grain, paper texture and broad mist fading. Protect authentic building structure. Lower area presents event name, date and main venue, followed by Schedule, More Activities, Registration and Participation, Additional Venues, and Live Streaming when present in approved copy. Keep groups coherent rather than a dense uniform table.

Registration and Participation and Live Streaming have every heading and body row right-aligned at x2280, matching the emblem's visible right edge. Schedule, More Activities and Additional Venues stay left-aligned at x120. Do not merely shift a left-aligned text frame to the right. A translated version retains the Chinese visual mechanism; reflow English phrases without choosing a different layout or enlarging the photo because of language alone.

## Required horizontal rules

Always draw two fine horizontal separators in the lower information system: one between the main venue and the two detail columns, and one between detailed information and the organizer/test-status footer. Both span x120–2280, stroke2px, confirmed themeColor at18% opacity. Use measured text boundaries and at least12px clearance above/below each line; reflow longer English paragraphs rather than omit a rule. They are group dividers, not underlines on every row.

## Sizes, fonts and color roles

Read [layout-spec.json](references/layout-spec.json). School/anniversary share a nominal160px, shrinking together as needed to keep each on one line and clear of the emblem. Detail section headings are 40px, detail body 36px, auxiliary notes 32–34px, default line spacing 52px. Event title 96px, date 80px and main venue 64px retain the existing hierarchy. Positions are starting points: extra English detail rows require moving subsequent sections, not clipping or excessive shrinking. Check the footer and the two columns after reflow. Small full-information copy still needs viewing-size assessment.

All English letters, digits and punctuation use the eight actual NotoSerifSC files in [fonts](fonts), preserved byte-for-byte; inspect [font inventory](references/font-assets.json). School ExtraBold 800, anniversary Bold 700 or Black 900, event name Bold, date/venue SemiBold 600, detail headings SemiBold, body Medium 500 and notes Regular 400. ExtraLight has actual weight 250 and Light 300; avoid them in small body text. Register the files and rasterize real glyphs into PNG, not AI-generated formal lettering, fake bold or geometric compression. Check newly introduced glyphs; the Latin sample is verified but not a promise of every language's coverage. No license document was supplied, so do not infer authorization from a font name.

School, anniversary, event title and specific detail-section headings all use one confirmed emblem-derived themeColor. Body text—including dates, venue values, schedule entries, registration/access rules, platform names, organizer names and test notices—is exactly #4B4B4B at full opacity. Never recolor all wording with the school hue or use white inversion. Read [color rules](references/color-and-visual.md). Prefer supplied documented brand values; otherwise record sampling from the actual emblem as a reference, not an official standard. If the heading color is too pale, clear the background or revise heading weight/scale without silently substituting a darker color. Neutral headings are allowed only in an unresolved-color review.

## Photo background

Use [photo prompts](references/photo-style-prompts.md) and the [style reference](assets/reference/photo-style-reference.jpg). The user's campus photo determines content/structure; the reference determines grain, soft tonal range and fading, not its trees or labels. Proportionally enlarge the actual visible subject and related scene toward 88–95% canvas width; do not count transparent padding or distort buildings. Guidance region x60/y620/2280×1240 must adapt to the source aspect ratio and the header.

All four edges blend continuously into the same white paper background using broad irregular fades, approximately 20–35% peripheral transition as guidance, not a tool-guaranteed mask value. Preserve the subject center; no hard photograph rectangle, white halo or uniformly washed-out subject. Header, emblem and detail zones stay lighter, with sparse texture. Fine grain, paper fibers and monochrome tint belong to the photo, not the authentic emblem or formal text. Missing campus photos leave open space rather than invented buildings.

## Execution and PNG-only delivery

Keep copy, translation map, palette sources and measurements internally. Cut out an opaque emblem first, then sample colors and measure its visible bounds. Select the campus photo, use the provided editing prompts and compare output against the source for roof, columns, arches, windows, trees and base. Place accurate real-font copy and the authentic transparent emblem after editing the photo layer.

The [English layout input](references/layout-input.example.json) and [preview](assets/examples/typography-review.png) are non-official typography reviews without a standalone emblem or source campus photo. They are not proof that cutout/color sampling/photo editing has been completed. The source [Chinese mother copy](references/anniversary-copy.example.md) is retained as evidence, not a requirement to typeset Chinese.

Run python scripts/check_assets.py. For actual-font review: node scripts/render_type_demo.cjs input.json output-dir [skia-canvas-module-path]. This requires skia-canvas, not packaged here. By default the output directory contains one PNG only. Optional --diagnostics is for an internal temporary QA directory, not final delivery. The helper receives explicit line blocks and checks geometry/colors, not semantic content selection. Reflow paragraphs before rendering; it refuses overflow instead of automatically dropping words.

Inspect complete, 960px and 375px views: translation completeness, names/numbers/dates, whole-word breaks, single-line school/anniversary with shared fitted size and64px emblem clearance, title/body color roles, shared emblem size plus top/right anchors, right-aligned participation/streaming, transparent edges, photo identity and wide fade. Do not silently shrink tiny details further. New copy may need expanded detail space and revised group tops.

Deliver only the complete English poster PNG, default 2400×3000, opaque white canvas, sRGB. Transparent emblem PNG, edited photo, layouts, diagnostics and review images are internal working assets, not separate deliverables. Use review status for missing facts or assets; never claim an official release or publish without authorization.
