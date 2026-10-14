# Campus photo editing prompts

The user campus photo controls subject identity, structures and scene relationships. The [style reference](../assets/reference/photo-style-reference.jpg) controls soft tonal range, grain, paper and fading only. A poster screenshot is a layout reference, not automatically a source campus photograph. Missing photos leave open space; do not invent a campus or reuse the reference woodland.

## Main prompt

Transform the supplied [campus photo] while preserving its authentic building proportions, perspective, roof, columns, arches, windows and base, and the original positions/relationships of trees and surrounding elements. Add no structures and alter no architecture. Create a low-contrast monochrome printed image on white or warm-white paper, using pale and soft midtone versions of [confirmed emblem themeColor] for the image. Keep recognizable structure and a readable subject core, reduce photographic high contrast and heavy dark blocks.

Add fine, random, soft print grain, subtle paper fibers and a dry printed surface. Grain follows image density like a light print embedded in paper; avoid coarse regular halftone dots, dense hatching and uniform heavy noise. Broad continuous irregular mist fading extends through sky, trees, ground and all four peripheral edges, not just a thin blurred border. Preserve a more legible center rather than wash out the entire subject at one opacity.

Adapt to a4:5 portrait canvas2400×3000. Proportionally enlarge the actual visible campus subject and related scene toward88–95% canvas width; transparent padding and bigger files do not count as subject enlargement. Protect the whole key building, including roof, pillars, arch and base. Place the photo mainly in the middle and fade toward upper-left titles, upper-right emblem and lower details. Keep lettering zones extremely pale with sparse texture. The four edges and grain progressively disappear into the same white paper; no photograph rectangle, visible seam, dark border or uniform white halo. Output the background layer only, with no words, digits, emblems, dot labels, logos or QR codes.

## Refinements

If only the outermost edge fades: broaden the peripheral transition to approximately20–35% of the image region, retain the recognizable core and slowly lower peripheral density to white. This is design guidance, not a guaranteed numerical mask.

If photographic lighting remains too realistic: compress tonal structure into pale and gentle middle tones, reduce sharpening, camera gloss, realistic highlights and cast shadows; express architecture with flat print-tone layers.

If enlargement crowds the header or details: recompute the safe region after English reflow and emblem resizing; do not crop the source building or stretch its geometry. No grayscale-to-purple conversion of the original emblem. A neutral gray image is used only when requested.

## Negative constraints and QA

Avoid high-contrast blacks, vivid multicolor photography, coarse dot screens, dense crosshatching, painterly strokes, cartoon buildings, plastic effects, hard rectangular image boundaries, thin-edge-only blur, uniform opacity reduction, noise over text, duplicated trees, changed architecture, fabricated campus structures, copied reference wording or dots. Use the tool's actual supported parameters; do not invent seeds or sampler guarantees.

Retain source and edited photo internally and compare structures/subject extent before composition. Check broad fading, source identity, light detail zones, absence of frames/halos and fine rather than overpowering grain. This prompt module does not by itself prove a successfully edited background. Final delivery remains the combined poster PNG only.
