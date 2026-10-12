<!--
TEMPLATE GUIDE
Placeholders use {kebab-case-name} format. Replace every placeholder with real content, then delete all comments
like this one before saving the final document.
Both the meta-instructions and the document content must be written in English.
Sections: Overview (1), Feature (one narrative subsection per functional area), Requirements (one checklist per area,
mirroring the Feature subsections 1:1).
-->

# {feature-name} — Functional Specification

<!-- 1-3 paragraphs: what the feature does, what triggers it, and why it matters to the user. No implementation details. -->
## Overview

{feature-overview-paragraph}

## Feature

<!--
One subsection per functional area of the feature. A short narrative (3-8 sentences) describing the behavior in plain
language — no checklists here. Duplicate this block for each additional area.
-->
### {feature-area-1-name}

{feature-area-1-narrative}

### {feature-area-2-name}

{feature-area-2-narrative}

## Requirements

<!--
Mirror the "Feature" subsections above, one checklist per area, same names and same order.
Each item is a single, testable sentence starting with "The user can..." or "The system...".
Use "- [ ]" for items this feature must deliver. Only use "- [x]" if the behavior already exists elsewhere in the app
and this feature merely reuses or extends it.
-->
### {feature-area-1-name}
- [ ] {requirement-1}
- [ ] {requirement-2}

### {feature-area-2-name}
- [ ] {requirement-1}
