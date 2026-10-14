# Sports landmark, vivid gradient and print texture

## Composition and scale

Full-canvas gradient; one upper-middle deconstructed hero leads to the event title.2400×3000,4:5. central regionx120/y670/2160×1120; bottom-bandx80/y660/2240×1420. Keep the actual horizontal center near1200 with possible asymmetric tilt. Trim transparent padding before proportional placement. Actual visible subject/motion width targets75–85% for central,80–90% for bottom-band; do not count empty transparent canvas. Keep at least60px from lettering. If the silhouette is too tall, redesign the composition rather than squeeze it horizontally or add irrelevant debris.

Central's hero is above year and title; bottom-band's is larger/taller below the single-row slogan and left/right header credits. Those credits are44px and top-aligned. Do not introduce a second bottom graphic or let art obstruct title/date. Existing group downshift is included in the coordinates.

## Extracting a sporting landmark

Record sport, choice and at least two recognizable structure/action cues. Basketball can use partial sphere seams and shot trajectories; tennis racket frame/string mesh and strike direction; running shoe tread, lane curves and stride; swimming lane structure, ripples and propulsion. Esports cues come from the actual project/assets, not automatically from a game-company trademark. No unsupported trophy, mascot or brand logo as filler.

Use4–6 clearly separated major flat pieces with irregular cuts, torn edges, offsets, overlaps and large transparent negative spaces. Partial seams/mesh/landmark fragments establish sporting identity without keeping an intact closed photographic silhouette. Small fragments share one motion direction; keep them subordinate rather than scatter many generic sports icons.

Each piece uses a single flat color or limited two-color halftone. Prohibit spherical volume, realistic highlights, smooth shading, reflections, heavy cast shadows and photographic material. Halftone is print texture, not a way to recreate3D lighting. Do not merely tear two lines through a realistically lit ball. Local transparent overlaps and light grain support structure, not replace the sporting connection.

## Background gradient

Use2–3 vivid saturated related principal colors, full canvas, smooth vertical/diagonal/radial transitions, optionally one soft glow. Cool hues can imply speed and tension; warm hues heat and strength, always based on source theme/brand. Blue-purple is not universal. Avoid hard bands, muddy grays, overexposure and many competing bright spots.

Text colors remain#FFFFFF for title/subtitle/slogan,#F1FFF7 for all others. Target contrast4.5 for normal text and3 for large title against the actual background, not only one gradient endpoint. Brightness can focus near the hero while text areas remain darker/stable. Adjust gradient placement and texture rather than invert text or place every group on a card.

## Shared hero/background hues

Lock the gradient palette first. Derive the hero's light/mid/dark colors from the same hue family, separating pieces with flat luminance and saturation variation. Do not automatically retain natural orange basketball or fluorescent-yellow tennis colors. Green background: forest/emerald/mint hero, small neutral seams/paper edges, no large orange/red ball or trail. Blue-purple: deep blue/purple-blue/pale purple. Coloring only an aura around an unrelated object is insufficient; harmonize the object's entire chromatic surface.

Shared hue is not shared brightness: the hero must remain clearly distinct locally. Small neutral dots/structural lines/paper edges stay secondary, not a competing principal palette.

## Halftone and paper texture

Overlay low-strength black-and-white halftone dots, fine photocopy grain and subtle paper fibers over the colored gradient. Dot density follows value while retaining vivid principal colors; do not turn the entire background grayscale. Texture must not become stains, cracks or another focal subject. Start around3–8% overlay strength if controllable, adjusting by readability; prompt tools cannot guarantee an exact numerical opacity.

Reduce dot contrast/noise in title/date/credit areas. Add real glyphs and true logos above texture, not distressed or eroded by it. Inspect thumbnails for moiré, oversaturated dot density and muddy colors; inspect full size for natural even paper grain. Keep a continuous full-canvas texture rather than an obvious untextured rectangle behind words.

Hero can carry the same print grain/halftone with clearer structure; background texture is lighter. See [image prompts](image-prompts.md) and the [deconstruction reference](../assets/reference/deconstruction-reference.png).

## Plans and layers

visual-plan includes mode, sport, theme_evidence, landmark/selection_reason, recognition_cues, deconstruction_plan, abstract_mechanism, hero_region, gradient/color_reason, halftone/paper_texture, hero_prompt/background_prompt, text_contrast_plan and assets. Separate hero/background/actual type; no generated formal words, logos or QR codes. SVG: gradient first, then hero group/clips, with proportional viewBox placement. render_layout.cjs produces transparent type paths; compose_scene.py overlays them. Organic or raster assets use appropriate image generation/editing tools and embedded true transparent outputs.

Current SVG examples demonstrate enlarged flat pieces, English Jiangcheng titles and current layout; they do not validate generated halftone/paper textures. They use fictional basketball seam fragments/shot trajectories and a blue-purple gradient, no fabricated logo. They are not fixed templates for other sports.

For a Chinese-to-English adaptation, preserve the Chinese selected mode, hero region, visible-asset bounds, crop, scale and placement. These mode-specific targets are shared with the Chinese skill, not an English-only enlargement instruction. Longer English wording requires typography reflow, not a larger graphic or an automatic mode switch. Reuse the same approved hero asset for matched-language comparisons.
