---
name: edit-harness
description: 'load when editing harness configuration files, such as skills, instructions, agents, and commands/prompts'
metadata:
    type: skill
    version: "1.0.0"
    updated-at: "2026-10-11"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

# Harness Front Matter
- This document defines additional required YAML frontmatter structure for all Copilot configuration files including **instructions**, **agents**, **prompts**, and **skills**.
- The front matter should include the following fields:
  - `metadata.type`: Type of configuration: `agent`, `prompt`,`command`, `skill`, or `instructions`
  - `metadata.version`: The version of the instructions, for example "1.0.0" semantic versioning format require to be updated when changes are made to the instructions
  - `metadata.updated-at`: The date when the instructions were last updated (format: YYYY-MM-DD)
  - `metadata.author.name`: The name of the author of the instructions
  - `metadata.author.email`: The email of the author of the instructions


- This front matter apply only to main files not to additional resources such as assets, templates or example files.