# Font use and dispatch

Choose a profile in assets/fonts/role-profiles.json by subtype, content, mood and information load, then compare specimens with real copy. Category labels do not lock the entire poster to one family. Role indexes are assets/fonts/roles-zh-CN.md and roles-en.md. A physical font is stored once per family and may serve several roles.

Distinguish confirmed original identity (source metadata, designer statement or official specification), observed style (stroke, proportion, terminals, numerals, spacing and graphic treatment) and usable substitute. Similarity in a raster poster does not confirm a font name. Every bundled font in this release is an open alternative, not a claimed exact original; its source and license have been verified.

FEEL, Black/White Forest, Manga and IP lettering contain apparent custom or brand treatment. Do not turn a cropped logo into a font. Use authorized original assets when appropriate; for a new title, adapt a mechanism through controllable lettering while verifying exact characters.

```powershell
python scripts/font_engine.py --profile PROFILE --language en --role title --text "Actual Event Title"
python scripts/font_engine.py --profile PROFILE --language zh-CN --role body --text-file copy.txt
```

Replace PROFILE with a category profile ID; text files are UTF-8. The script returns the actual file, internal family, weight, fallback status and rejected missing-glyph candidates. It installs nothing and contacts no network. The root is inferred from the script location; --root can override it, so the package is relocatable.

Preference order: explicit user/brand choice, usable authorized original asset/font, suitable available local candidate, bundled open alternative. Verify official sources and permitted use before additional downloads. If the specified font is unavailable, show concrete alternatives rather than silently substituting it.

Load the returned file path using its internal family or a stable alias. A font-family name in SVG does not embed the font. Cross-machine editing requires the same font; license-permitted embedding or outlining should retain an editable text copy. Do not copy unverified system fonts into a redistribution package.

The script selects a candidate covering the entire field, rather than randomly swapping families per character. Mixed Chinese, Latin or Thai may require an explicit, optically checked run strategy. If none of the bundled candidates covers the complete field, the selector fails visibly instead of inserting boxes or fake letters.

All bundled files except Noto Sans Thai are static. The Thai variable font can load at its default axes; if the renderer lacks variable support, report it unavailable rather than applying fake weight or deformation. Variable-axis behavior is not guaranteed in untested renderers.

Use a genuine condensed face or a larger text box instead of horizontally compressing type. Do not penalize mixed subtitles automatically, prescribe a universal headline ratio, or treat hierarchy and overall composition as the same check.

Each family retains OFL.txt, copyright, official commit and SHA-256. These font binaries are unmodified. Follow the included OFL terms for bundling; do not sell fonts by themselves or disregard reserved font names. Font permission does not grant rights to reference artwork, characters or logos.
