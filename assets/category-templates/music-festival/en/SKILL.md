---
name: cultural-pop-performance-poster
description: "Build Chinese and English posters for popular and contemporary live performance: source intake, subtype strategy, bundled font dispatch, pre-generation decisions and visual review. Excludes product marketing."
---

# Popular and Contemporary Live Performance Poster Supplement

A self-contained specialist supplement that can also extend cultural-event-poster. Establish content/evidence before expression and fonts. Download provenance does not confirm the original case font, and supplied scores do not establish audience effectiveness.

- [Intake and facts](references/intake-and-facts.md)
- [Category strategy](references/category-strategy.md)
- [Five pre-generation decisions](references/pre-generation-approval.md)
- [Chinese poster strategy](references/zh-poster-strategy.md)
- [English poster strategy](references/en-poster-strategy.md)
- [Font use and dispatch](references/font-routing.md)
- [Font identification](references/font-identification.md)
- [Case evidence and gaps](references/case-evidence.md)
- [Production and review](references/production-and-qa.md)


- [Analyze and transfer excellent references](references/reference-learning.md)：Read before concepts, fonts and prompts when exemplars are supplied; inspect images and carry mechanisms into production.
## Subtype routing

- [livehouse](references/subtypes/livehouse.md)
- [music-festival](references/subtypes/music-festival.md)
- [concert-tour](references/subtypes/concert-tour.md)

## Workflow

Inventory → sourced master and conflict checks → primary type/subtype → content proposition and direction → font specimens and five decisions → key visual without formal copy (original-title exception: reference-learning.md) → controlled typography and language recomposition → fact/glyph/visual/specification QA → human review and targeted repair. Inherit explicit decisions; never mark unresolved items as human-approved.

Retain an accepted visual for typography-only repair. Do not invent facts, official identity, font names, permissions, QR codes or audience feedback. Typography and visual mechanisms are conditional rather than a fixed reference style.

## Resources and checks

- [Font catalog](assets/fonts/catalog.json) · [Role profiles](assets/fonts/role-profiles.json)
- [Chinese role index](assets/fonts/roles-zh-CN.md) · [English role index](assets/fonts/roles-en.md)
- [Pre-generation record](assets/pre-generation-review-template.json) · [Review record](assets/review-record-template.json)

```powershell
python scripts/font_engine.py --profile livehouse-atmospheric --language en --role title --text "Actual Event Title"
python scripts/inventory_inputs.py INPUT_FOLDER --hash --output input-manifest.json
python scripts/validate_brief.py brief.yaml --json
python scripts/validate_delivery.py brief.yaml delivery-manifest.json --output-root output --json
```

YAML validation requires PyYAML; JSON avoids that dependency. Font dispatch needs only the standard library. Technical success is not aesthetic approval; strategies are trial and missing images/subtypes remain unvalidated. Reference artwork is not a ready-made commercial key visual.

- [Composition routes](references/design-routes.md)
- [Font comparison specimens](references/font-proofs.md)


Reference-learning revision: reference-learning-v2-2026-10-12
