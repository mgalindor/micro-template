---
title: Create Doc Template - Verification Checklist
date: 2026-02-24
type: checklist
scope: internal
---

# Verification Checklist – Create Doc Template

**Very Important**: This checklist is a guide to verify the implementation is completed — it is not required to create an output document with this list of items.

## Placeholders

- [ ] All specific values from the source file have been replaced with `{variable-name}` placeholders
- [ ] Placeholder names are descriptive and indicate the expected content
- [ ] Multi-word placeholder names use `kebab-case` (hyphens)
- [ ] Scalable sections use numbered placeholders (e.g., `{item-1}`, `{item-2}`)

## Comments

- [ ] A top-level guidelines block is present at the very top of the template
- [ ] The guidelines block explains the placeholder format
- [ ] The guidelines block explains the comment format used in this file
- [ ] The guidelines block includes usage instructions
- [ ] The guidelines block provides a section overview
- [ ] Each section has a comment explaining its purpose and expected content

## Structure

- [ ] All sections from the original source file are preserved
- [ ] All sections contains comments that explain their purpose, expected content, formatting requirements, and examples where helpful
- [ ] Optional sections are marked with `<!-- Optional section -->` or equivalent
- [ ] Icons, formatting elements, and visual structure match the original
- [ ] Scalable sections allow adding more items without structural changes

## File

- [ ] Output filename follows the pattern `template-{file-basename-no-extension}.{extension}`
- [ ] File is saved in the workspace root directory
- [ ] File includes the required YAML metadata header (title, date, type, scope)
