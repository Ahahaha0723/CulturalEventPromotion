# English Layout v3: Tilted Overlapping Titles, Nearby Labels, Muted Notes

## Resources and unchanged anchors

Read SKILL.md and fixed-layout.json. Original v25 PNG is inherited composition history only, with obsolete Chinese text/colors/indented hours/slogan line/fixed papers. Use the updated English rules. decorative-layers.svg now has window, objects and decorative circles only; title sheets are generated from current measured glyphs by the typography script. Do not composite both old and new sheets.

Canvas2400x3000. Organizer ink left150/top150; first subtitle right2250/top150; second subtitle baseline first+80. Date/hours ink left150 and baselines450/555. Slogan anchors/baselines remain x850/920/820/920,y1090/1230/1370/1510. No slogan line. Normal human contours, broad fading40-90px/default60, double gray contours, masked grid and general palette roles remain unchanged; booking notes are now#858585,36px.

Right-aligned x=2250-actualBoundingBoxRight; ink-top150 baseline=150+actualBoundingBoxAscent; ink-left150 x=150+actualBoundingBoxLeft. The mixed-font renderer measures the union of actual ink from Trajan/Futura letter runs and Harmony digit runs. Re-measure after fitting.

## One title size and content-sized sheets

Two title lines use the SAME Trajan Bold actual size. Start at240px, measure both, and take the smallest shared size required by their content width limits900/820px. Minimum120px. Never shrink just the longer row while keeping the shorter row larger, or scale letters horizontally. Keep unrotated ink-left anchors150/580 and first baseline2000; derive the second baseline from the required paper overlap rather than forcing2320.

For each row, measure left/top/right/bottom ink after choosing the shared size. Front sheet x=inkLeft-50,y=inkTop-50,width=inkWidth+100,height=inkHeight+100. Back sheet x=frontX-18,y=frontY+15,width=frontWidth+20,height=frontHeight+16. Front rotations-1/1.5deg; back rotations-4/4deg, each around its own center. Gray front border2.5px/opacity0.65; back2px/0.45. Front white fill/opacity0.84; back green fill/opacity0.12. Front folded corners gray2px/0.45. Rotate the entire title row with its own front sheet using the same angle and center; never separately rotate letters or use an italic substitute. Keep both lines at the shared size. Target40px vertical overlap between front-sheet groups, minimum20px. Derive second-sheet top from first-sheet bottom minus overlap; derive its title baseline from that top, padding and measured ascent. Decrease overlap only enough to keep the rotated lower sheet clear of the rotated upper title ink (with6px safety). Record the resulting second baseline and actual overlap.

The renderer writes title-paper-layers.svg and titlePapers in text-metrics.json. Place it behind title type and include its sheet geometry in the grid mask. Equal padding controls the relationship between words and paper; paper widths may differ with word length. Inspect rotating sheets against nearby labels/scenes; a width check does not prove a complete composition is clear.

## Single-line activity labels: extend, then relocate

Supply four unique complete activity_labels as strings. Inherited arrays are joined with spaces; do not retain a manual split just because an old block was too short. Use one52px Futura Bold size, white text, green block,18px horizontal/12px vertical padding. Single-line block height uses the common maximum ascender/descender across all labels, so all four have identical heights. Width is actual advance+36px.

Place labels from final figure/outer-contour bounds, not distant old caption baselines. Each target label is20px below the visible outer contour, horizontally centered/overlapping its scene, and should remain within20-40px. optional scene_bounds is an array of four {left,top,right,bottom} rectangles in final-canvas pixels, ordered like activity_labels. Measure these from visible final outer contours, excluding empty asset margins; if absent, the renderer uses configured scene slots only as a provisional fallback and records that basis.

Extend blocks into white space and clamp to safe x150-2250. Avoid window x1460-1830,y330-905 plus24px clearance. The top-middle caption can shift left while still horizontally overlapping its figure. The default upper-right scene moves down from y310 to390 so its nearby caption can sit below the window; retain normal proportions/other scene sizes. The middle decorative circle moves from x740 to1000 at y1640 to avoid forcing the left caption far from the figure. If actual new shapes create collisions, prioritize a closer safe label location or a small ornament/scene-plus-label adjustment, not a large empty gap. Log any proximity greater than40px and resolve it against actual artwork before final delivery.

Default maximum text width1000px. Only after that capacity is exceeded may a complete name wrap by words into at most two rows; this is an explicit logged exception, never the first response to a short block. Do not shorten/drop an activity qualifier, add leading bullets or independently shrink labels. Check against actual new figures, props, title sheets, slogan and other captions. The script knows the bundled window, three decorative circles and generated title sheets, not arbitrary new artwork, so final collision checks remain mandatory.

## Bottom: two3-row groups plus separate booking notes

Use footer_left_lines and footer_right_lines, each exactly three semantically planned English strings. The left group is district name / entrance / full address; the right is access / reservation summary / action prompt. Align actual ink left150 and right2250. Maximum text width900px per column creates a minimum300px central gutter (left text ends by1050,right starts no earlier than1350).

Both groups use baselines2555/2640/2725, sizes52/48/44; first row Futura Medium, subsequent rows Futura Book. Digits remain Harmony at the matching role. If measured fitting is needed, never reduce these groups below42px; redistribute clauses instead. Do not use long single-line combined venue-and-entrance sentences.

booking_notes contains zero to two complete semantic strings from the mother text. Baselines2830/2895, ink left150,max width2100,size36,minimum34,color#858585; both rows share one actual size. This is a separate small information paragraph, LEFT aligned, not centered. Include the complete activity-specific booking method, on-site participation conditions and source contact/session information when supplied. General access/reservation summaries can be concise, but notes cannot silently lose facts. Avoid repeating the entire long explanation in both areas.

Example: left Wutongli Arts District / East Gate Service Station / 26 Jiuchang St,Hexi District,Wuzhou. Right Free public access / Selected activities require advance booking / Start at East Gate; collect your co-creation map. Notes specify printmaking and photography need advance booking, swap/concert can be joined on site, and booking/session details are available at the East Gate station. Never reuse these facts for another brief.

## Scene slots

| Slot | x,y,width,height | Opacity | Label |
|---|---|---:|---|
| Cropped upper figure | 0,-270,380,371 | 0.80 | None |
| Top-middle | 1032,80,360,579 | 0.88 | 1 |
| Upper-right | 2050,390,350,518 | 0.84 | 2 |
| Left-middle | 140,840,400,742 | 0.86 | 3 |
| Lower-right main scene | 1530,1270,950,991 | 1.00 | 4 |

Maintain proportions, never stretch figures. Map the principal activity to the lower-right scene, record mappings, and never invent a fifth activity for the cropped figure. Four activities are template capacity; other counts require a documented adjustment, never omission or duplication.

## Fonts, schema and execution

Trajan Bold.ttf for main-title letters/punctuation. FuturaStd-Bold.otf for subtitles/labels/emphasis; Book for general copy and notes; Medium for date/leading footer rows. All0-9 digits use HarmonyOS Bold/Regular/Medium by role. Split digit/non-digit runs without adding spaces and share baseline/size/color. Verify registered files and Latin glyph coverage; do not use synthetic bold or fallback. Trajan Regular and Futura ExtraBold/Heavy/Light remain optional supplied variants.

layout-text.json requires two title_lines,two subtitle_lines,four slogan_lines,organizer,date,opening_hours,four activity_labels,three footer_left_lines,three footer_right_lines,and optional booking_notes (max2). The source facts belong in brief/translation_map even when layout grouping changes. Slogan rows may be strings or [{text,bold},...]; preserve English spaces and use one common fitted size. Existing width limits and60% fit floor for unchanged top/slogan copy remain.

```text
node scripts/render_typography.cjs layout-text.json output-dir [skia-canvas-module-path]
```

Outputs typography-outlined.svg,title-paper-layers.svg,text-metrics.json including runs/titlePapers/labelBoxes/adjustments. These layers are not a complete poster. Compose with actual artwork via XML-aware SVG handling and rebuilt masks; render2400x3000 plus960px/375px previews. No image-model formal lettering. If any source fact cannot fit, preserve it and revise semantic grouping; if still unreadable, prepare a concrete bounded layout exception for review rather than delivering a falsely complete final.
