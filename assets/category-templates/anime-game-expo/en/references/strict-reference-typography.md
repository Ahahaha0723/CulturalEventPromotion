# Strict typography matching to the best-fitting reference

## Default standard for anime/game exhibition work
The user requires strict, accurate imitation of the best-fitting reference's font selection and typography. Apply this during generation, recomposition and font repair in this category. New explicit user font/layout/brand requirements take precedence. Keep three-dimensional visual analysis; this file specifies the text-layer standard.

Choose the fitting typography reference first, then lock font roles and layout relationships from the actual image. Never let a glyph-coverage dispatcher pick a font and retrospectively call it visually matched. Broad stylistic freedom or “roughly similar” does not meet this request.

## Choose a justified typography lead
Inspect candidates against event format, communication task, image mood, actual title/copy density, script/language, canvas and viewing size. Record comparison evidence, nontransferable roles and the choice. “Best” means a reasoned fit to this brief, not an invented objective ranking or similarity percentage.
- Honor an explicitly selected typography reference. Explain necessary language/canvas changes rather than replacing it with a default.
- Broad conventions usually compare022/014, single-IP experiences052, creator announcements053. Game expos require real content fit.
- Visual and typography references may differ. Keep one typography lead; a secondary role needs an explicit source, reason and compatible relationship rather than mixing isolated favorites.

## Build a source-to-output role map
Record title, event form/subtitle, slogan, creator/brand, date/numerals, venue/body and CTA. If a source has no matching role, mark it absent and extend an existing visual role; do not invent an unrelated family.

|Element|Record|Execute|
|---|---|---|
|Character|Serif/sans, visible weight/width, stroke contrast, counters, terminals, slant and custom treatment.|Use a confirmed available original, or compare declared same-class alternatives; unknown originals remain unknown.|
|Hierarchy|Visible glyph height, width, mass, title/subtitle ratio, grouping and full formal name.|Set actual copy with reference-derived optical proportions, not a category-wide size ratio.|
|Space|Bounds, baseline, alignment axes, gaps, tracking, leading and image/band junction.|Normalize x/W, y/H, glyph height/H and text width/W where useful; label measurement versus estimation and confidence.|
|Reading|Rows, length transitions, phrases, date groups and sequence.|Retain roles/cadence without dropping facts, breaking names or imitating an arbitrary row count.|
|Treatment|Capitals, italics, grain, outlines, distress, occlusion and wordmarks.|Only transfer supported treatments; official marks remain assets, original titles may use editable lettering.|

Estimated coordinates are not precise measurements. When aspect ratio/copy length differs, retain roles, mass and adjacent relationships while recomputing placement; disclose necessary changes. Never distort glyphs or shrink everything to inherit coordinates.

## Select and lock real fonts
1. Compare the actual source lettering region. Custom MANGA is neither confirmed ZCOOL QingKe HuangYou nor Archivo Black.
2. For unknown originals, make parallel source/candidate samples using real copy and, when useful, the same reference words. Compare at similar visible glyph height, not merely equal point size. Record weight/width/counter differences and selection reasons; do not fabricate match scores.
3. Lock file, weight/italic, checksum, role, size/tracking and wrapping. Use [explicit font verification](../scripts/reference_font_check.py) on the chosen file without silent fallback. If no font meets the target, seek an appropriate face or make editable original lettering; retain the gap and review status rather than claiming an exact reproduction.
4. Check Chinese/English separately. Chinese cannot copy Latin counters/proportions literally: preserve equivalent stroke character, mass, roles and relationships, explaining language adaptation. No horizontal squeezing or automatic letter-by-letter Chinese splitting.

reference-022, reference-052 and reference-053 are starting candidates, not aesthetic selectors. General profiles are not selectors either. font_engine coverage still needs visual comparison; reference_font_check verifies a selected font without choosing another.

## Source-specific rules
- **022/Manga Barcelona:** wide heavy geometric identity, heavy date and compact functional copy in a separate bottom band. Compare stable geometric heavy Chinese or controlled lettering; “Chinese comics” does not imply playful rounded type. The source has no italic-serif slogan: added slogans extend an existing role instead of automatically gaining decorative italics. A three-row city split requires an actually suitable name/lockup.
- **052/Arcane World:** tall condensed heavy white sans heading participates with shoulders; centered facts/date order remain clear. Compare actual Anton/Bebas Neue visible weight, never call either the source font by default. Keep distress legible; venue serif evidence does not make all body text serif.
- **053/NYCC Artist Alley:** high-contrast italic-serif tracked creator signature; normal-width bold italic sans Artist Alley/Table F20; huge heavy upright NYCC. Roles are not interchangeable. Newly bundled Barlow BoldItalic is a comparison candidate for table text; condensed bold italic is materially narrower and must not win merely because it is italic. Improve dense small copy at intended viewing size and record the change.

## Lock layout and review
Use the [typography reference lock](../assets/typography-reference-lock-template.json) with actual bilingual copy. Compare title/subtitle/date/body modules before combining with imagery. Preserve roles, weight relationships, optical proportions, axes, tracking/leading, grouping, date position and image junction; deviations need a reason.

Compare original crop, candidate composition and output text region side by side, then inspect the whole poster and actual thumbnails. Review character match, hierarchy, row cadence, spacing/alignment, numerals, image relationship and complete copy separately, with evidence and unresolved differences. Copy/glyph/bounds checks alone are insufficient.

Unsupported extra italics/families, obvious width/roundness changes, altered hierarchy, relocated dates or a generic template require text repair and cannot be marked strict matching complete. Necessary readability/semantic/aspect changes need recorded impact. Keep accepted imagery for text repairs; final aesthetics/publication need human review without adding repeated approvals for routine trials.

## Scope of this feedback
Guoman v01 passed technical checks; that did not establish strict typography matching. This request raises the font/layout standard. Its ZCOOL title, italic English slogan, sizes and band ratio must not become defaults. This update changes instructions/candidates; it does not revise v01 or claim acceptance under the new standard.

- [Originals and three-dimensional analysis](case-guided-generation.md)
- [Identity evidence and candidates](font-identification.md)
- [Strict comparison specimens](../assets/strict-font-proofs/022.png), [052](../assets/strict-font-proofs/052.png), [053](../assets/strict-font-proofs/053.png)
