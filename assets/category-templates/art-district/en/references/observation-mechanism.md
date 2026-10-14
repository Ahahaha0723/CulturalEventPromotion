# Community Observation: Artwork Layers

Use the approved v25 composition and this edition's English typography/white palette. Text anchors and nominal sizes are in SKILL.md and fixed-layout.json. This reference specifies artwork, not an alternative free typography layout.

## Locked original soft appearance

View assets/layout/silhouette-soft-reference.png before generating artwork. The full reference is included for portability; compare only people/primary props, not its obsolete copy or layout. Restore the soft green, broadly fading silhouettes seen there. The later hard-edged green cutout/furniture illustration is a rejected rendering, not a new style option.

Simplify interior detail while preserving normal external anatomy AND broad softness. The main mass is recognizable, with extensive green-to-transparent transition across its edge region; it does not remain fully opaque until a one-pixel rim. Do not sharpen or vector-trace the soft figure into a clean filled path. Keep independent2px/1.3px gray contours, with the inner fade visible inside them. No opaque white keyline around the body.

Approved people/prop assets are locked against typography-only regeneration. Keep the same raster asset/alpha when changing fonts, tilted papers, nearby labels or footer information. A uniform reposition/rescale is allowed for layout, but recheck final fade width and contour weight. New activities can change actions/props only while matching the reference treatment.

## Natural human outline, simplified interior

Preserve natural proportions, real head/hair silhouette, neck/shoulder connection, torso thickness, limb volume, joint transitions and body weight. Standing, sitting, leaning and lifted hands must look like normal people performing the source activity. A profile may retain the nose tip and jaw outline; garments can shape the outer contour. Omit internal eyes/nose/mouth, hair strands, fabric folds/texture, skin/material detail, muscle shading and photographic lighting.

Simplify interiors, not anatomy. No perfect-circle heads with rod limbs, restroom icons, geometric people, children's stick figures or assembled circle/rectangle bodies. Keep normal shoulders, joints and limb volume. Workshop poses should naturally lean/work; exchange poses should pass objects; photography and music poses should naturally hold their relevant objects.

## Broad edge fade

Core color #018F69. On broad torso regions, default transition60px, typically40-90px on the final2400px canvas. Use roughly15%-25% of an individual person's torso short side as an initial scale reference; never the combined width of an entire group. Adjust for actual figure size and anatomy.

Roughly90% of the transition extends inward from the unfaded normal outline and10% outward. At60px this is54px inward/6px outward. Reduce solidity across a broad interior edge region rather than adding a tiny blur ring. Suggested continuous alpha profile from the inner start to the outer end:

| Transition position | Alpha |
|---|---:|
| 0% | 0.95 |
| 35% | 0.75 |
| 70% | 0.30 |
| 100% | 0.00 |

Interpolate smoothly without color bands. Core alpha0.9-1.0; apply the scene-slot opacity separately. Values are controllable-rendering guides; inspect generated assets instead of claiming the image tool honored exact numerical settings.

Locally reduce the fade on heads, wrists, fingers, narrow calves and feet so normal contours/actions remain legible. It must be clearly visible in a960px full preview and preserve soft solidity/transparency layers at375px. Do not blur the entire person uniformly, create a large glowing cloud, or accept a tiny edge visible only when zoomed in.

Contour paths use the normal shape before fading: offsets14/28px, not thresholds taken from unstable pale pixels. Keep both outlines sharp and independent of silhouette fading. Make room for fades without invading labels, formal English text or neighboring scenes.

## Double contours

Every scene has two separate closed paths following the natural human/group/necessary-object outline. Use subtle stepped-line rhythm from the approved observation-frame mechanism.

- Inner offset14px, stroke2px.
- Outer offset28px, stroke1.3px.
- Both #858585, opacity0.65, fill none, approximately14px between paths.
- Do not draw the same path twice, use a thick stroke/glow/shadow, or substitute a rectangular card.
- These widths apply after asset placement on the final2400px canvas. Scale proportionally for another export, and avoid different stroke thicknesses caused by differently scaled scene assets.

If a generated asset has one contour, edit it or add the missing controlled vector contour. Preserve the broad fading silhouette. Verify every scene with independent layers or zoomed evidence; do not inspect one scene and assume the others pass.

## Paper layers and window

Use generated title-paper-layers.svg from the typography script for the current title, and factory-window from assets/layout/decorative-layers.svg. Do not reuse obsolete fixed paper rectangles or ask an image model to guess them. Two paper groups, each with back/front sheets. Back fill #018F69/opacity0.12, gray border2px/opacity0.45. Front fill #FFFFFF/opacity0.84, gray border2.5px/opacity0.65. Fold corners #858585,2px/opacity0.45. Both title lines use one shared measured font size. Each sheet surrounds its own title ink with50px padding on all sides; the back sheet is offset(-18,+15) and slightly larger. Slightly rotate each entire title row with its own front sheet, at the same angle/center (-1deg and+1.5deg); do not rotate individual glyphs or synthesize italic. Restore overlap between the two paper groups (target40px,min20px), adjusting the lower title baseline from paper geometry while keeping upper glyphs unobscured. Include the generated paper geometry in the current grid exclusion mask.

Window bounds x1460-1830,y330-905, a gently perspective-shifted rectangle with one vertical mullion and two horizontal mullions. Keep fine simple gray lines, no detailed brickwork, glass textures or full architecture. Mask the entire window plane from the background grid.

## Relevant objects

Every activity scene needs at least one minimal source-supported object. A main prop or necessary table/chair silhouette should stay visually soft with the person when represented as a filled scene mass; do not substitute a full rigid gray outline illustration. Use simple line/geometric contours, #858585 both inside green silhouettes and in white space, roughly2.5-5px strokes/opacity0.6-0.75. Objects cannot obscure labels or formal English type.

The accepted example has a picture frame, cup/small table, open book and worktable/drawing board. Replace them for new activities: small plate/roller for printmaking, simplified camera for photography, box/book for exchange, suitable instrument for music. Prefer one main object plus at most a necessary support object. Avoid detailed chair rungs, table braces, drawers/panels, guitar strings, camera controls or dense construction lines. A worktable overlay can be a tabletop and two simple legs; a guitar/camera needs only its recognizable outer form. The shared window does not count as every activity's own object.

## Asset-generation prompt

"Use the bundled earlier soft silhouette reference as the visual target for [new event/activity]. Create transparent-background people/primary-prop assets in that SAME soft fading silhouette style. Natural human proportions and recognizable poses; simplify interiors, not anatomy. Green #018F69 forms with clearly broad soft alpha transitions across the inner edge region, default60px/40-90px on the final2400px canvas, approximately90% inward/10% outward; fade is visibly extensive, not a thin blur ring around an otherwise crisp solid figure. Retain a readable central core and reduce local fade for narrow limbs. No hard-edge vector cutout, sticker, opaque white keyline, full anatomical illustration, internal facial/clothing detail, photographic lighting or round-headed stick figures. Two independent fine gray #858585 contours, inner2px/outer1.3px, offsets14/28px, separated and clear; only these outline paths are sharp. Necessary principal props/furniture are minimal softened forms or a few simple independent overlay lines, never a detailed structural line drawing of a table/chair/instrument. Do not generate text/brands/QR codes. Keep poses supported by the new mother text and preserve layout clearances. White background, masked grid, window, title sheets and formal English typography are separate controlled layers. For text-only changes use the already approved asset instead of generating this again."

Use available built-in image tools and follow image-editing skill/tool rules for bitmap edits. Confirm actual contours/stroke behavior in the final layout instead of accepting prompt wording as evidence.

## Grid mask and final layers

Grid #858585,1.8px,opacity0.17,spacing145px as in fixed-layout.json. Exclude interiors of new silhouettes/contours, the whole window plane, four papers, relevant objects and foreground shapes. Never reuse an old figure mask for new activities. Solid green label blocks cover their own grid; translucent silhouettes/papers/windows need explicit masks.

Keep white background, green silhouettes, #2D2D2D title, #4B4B4B general English copy, #858585 booking notes at36px, and #FFFFFF label copy on green. Activity labels are complete single-line white names in extended green blocks with one common52px size/height; place them20px below their own final visible outer contours (preferred maximum40px), with horizontal projection overlap; use measured scene_bounds rather than empty asset edges. Relocate them into close safe free space before exceptional wrapping. Retain at most the three decorative circles; they are not label bullets. No slogan corner path, frame or invented navigation route; retain the four English slogan rows/keyword weights and paper fold corners.
