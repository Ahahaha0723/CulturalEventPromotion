# Printed lettering with real fonts

Typeset accurate FontQu Smile main title and Noto Serif SC body first. Preserve English content, glyph outlines, positions, centered header, left/center/right columns, sizes and spacing before applying print finish. Do not regenerate characters or substitute fonts.

## Prompt

Start from the correctly typeset poster. Keep every word, digit, punctuation mark, font contour, size, position, line spacing and alignment unchanged. Lettering itself should feel like real ink printed into natural paper: retain original ink colors, add minute random density differences inside strokes, very sparse pin-sized local ink loss and subtle fiber show-through. Edges may have extremely slight natural ink softness while retaining the original FontQu Smile forms and Noto serifs, stems and turns. It should not look like perfectly smooth digital lettering pasted on textured paper.

The main title can have slightly stronger texture; subtitle and details are lighter and more complete. Preserve descending three-level header sizes; all bottom details share42px and weight hierarchy, with left/center/right alignment and equal outside margins. Graphic and text share a paper/ink feeling, without fading entire rows, adding words, broken glyphs, color-registration ghosts, glow, thick outlines or3D shadows.

## Implementation and verification

Prefer subtle coverage changes within actual glyph alpha masks. render_poster.cjs renders true fonts to a separate layer and applies limited density variation, protecting thin stems; inkTexture=false is available only for internal comparison, with finish enabled by default. This is native text rendering, not generated replacement lettering.

If an image editor applies finish, provide the accurate poster as the source and compare every glyph and layout afterwards; restored original lettering is required when the model rewrites it. Do not use whole-image blur/heavy noise as ink texture. Avoid broad damage, lost serifs, missing letters, tracking changes, coarse screens, strong smearing, stains or yellowing. Assess texture at actual viewing size; stronger distress is not automatically better printing.
