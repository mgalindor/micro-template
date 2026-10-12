---
name: create-doc-template
description: "Guidelines to create a document template, this template will be used by AI to generate repetible documents in a uniform format. Trigger: When user asks to create a document template"
user-invocable: false
metadata:
    type: skill
    version: "1.0.0"
    updated-at: "2026-05-15"
---

## When to Use

- User ask to create a document template
- User provides a source file and asks to create a template from it
- User wants a reusable version of an existing document with placeholders
- User needs a template that an AI or a person can populate later

## Critical Patterns

### Placeholder Format

Replace all specific values with `{variable-name}` placeholders:

- Use descriptive names that indicate what content belongs there
- Use `kebab-case` (hyphens) for multi-word names
- Examples: `{project-name}`, `{service-1-name}`, `{technology-name}`, `{feature-1}`

### Comment Format by File Type

Use the appropriate syntax for the file format:

| File type | Comment syntax              |
| --------- | --------------------------- |
| Markdown  | `<!-- comment -->`          |
| YAML      | `# comment`                 |
| JSON      | `"_comment": "..."` field   |
| Code      | Language-specific (`//`, `#`, etc.) |

### Top-Level Guidelines Block

Every template **must** include a comment block at the very top explaining:

- The placeholder format (`{variable_name}`)
- The comment format used in this file
- How to use the template (fill in placeholders, remove comments)
- An overview of the main sections

### Per-Section Comments

Before each section add a comment that explains:

- Purpose of the section
- Expected content length and tone
- Any formatting requirements
- An example value where it helps

### Naming Convention

Output filename follows this pattern:

```
template-{fileBasenameNoExtension}.{extension}
```

Examples:
- `README.md` → `template-readme.md`
- `config.json` → `template-config.json`
- `meeting-notes.md` → `template-meeting-notes.md`

### Structure Rules

- Keep **all sections** from the original file — do not remove any
- Allow scalable sections (e.g., numbered placeholders: `{item-1}`, `{item-2}`, `{item-3}`)
- Mark optional sections with a comment: `<!-- Optional section -->`
- Preserve icons, formatting elements, and visual structure from the original

### Checklist Before Start

- [ ] Make sure the goal of the document is clear
- [ ] Make sure the target audience is defined
- [ ] Make sure the sections that a template should have are identified
- [ ] User can provide a file as example to create the template from, but it is not required
  - [ ] If the file is not provided, you can create a template based on the description and guidelines provided by the user
  - [ ] If there is no sections or guidelines provides or sections formulate 2-3 questions to the user to clarify the structure and content of the template before start creating it
- [ ] Verify the if there is an existing template with the similar goal and structure. If yes notify the user and ask to continue

### Checklist Before Create File
- [ ] Do a summary with 
  - Goal
  - Audience
  - List of sections with a brief description of the content of each section
- [ ] Confirm with the user that the summary is correct and includes all the relevant information before proceeding to create the template file.

## Verification

In order to verify that the skill is correctly implemented, you can follow these steps:

- **Checklist**: [Verification Checklist](assets/checklist.md)
