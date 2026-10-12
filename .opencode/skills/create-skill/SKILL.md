---
name: create-skill
description: "Creates new AI agent skills following the Agent Skills spec. Trigger: When user asks to create , modify or verify a skill, add agent instructions, or document patterns for AI."
metadata: 
    type: skill
    version: "1.0.1"
    updated-at: "2026-05-15"
---

## When to Create a Skill

Create a skill when:
- A pattern is used repeatedly and AI needs guidance
- Project-specific conventions differ from generic best practices
- Complex workflows need step-by-step instructions
- Decision trees help AI choose the right approach

**Don't create a skill when:**
- Documentation already exists (create a reference instead)
- Pattern is trivial or self-explanatory
- It's a one-off task

## Drive the user

**Very important**: Before start to create the skill, try to get clarify the skill details listed below. Do not ask directly what is the skill goal instead ask indirect questions to gather the the information like "what are you planning to do?", "do you think you need to generate a file ?", " all the files generated with this skill require the same structure?" 

Information required to create a skill:
- skill goal
- decide the type of the skill (generic, actionable, workflow)
- identify if the the skill require a template (template is usefull when the user wants to generate a document with a specific structure or content, or when the output is complex enough to require guidance beyond general instructions)
- identify if the skill require a checklist (checklist is usefull when the user need steps to verify the correct implementation of the skill, eg. steps to verify structure or verify the content was made based on verificable facts instead of assumptions)
- identify if the the skill require a workflow (workflow is usefull when the user need to execute a complex process with multiple steps and need guidance for each step, or when the process require to control the execution flow based on conditions or verifications). In this case is really important to evaluate an verify what steps are required to complete the process. Drive the user to break down the process in clear steps with a defined input and output for each step. This will help to create a clear and efficient workflow skill that can be easily followed by the AI.
- identify if the skill is part of the core of gene2 (in this case the skill have to be placed in the folder `.gene2/skills/`) or if it's a project specific skill (in this case the skill have to be placed in the folder `.github/skills/`)

## Skill Folder Structure

```
skills/{skill-name}/
├── SKILL.md              # Required - main skill file
├── scripts/              # Optional: executable code
├── assets/               # Optional - Used by the skill to generate output (templates, schemas, examples)
│   ├── template.md       # Optional - File in markdown format with placeholders and instructions to generate a new document
│   ├── checklist.md      # Optional - List of items in checkbox markdown format `- [ ] item` to verify the correct implementation of the skill. Checklist have to include the next disclaimer `**Very Important**: This checklist is a guide to verify the implementation is completed is not required to create an output document with this list of items`
│   ├── workflow.md       # Optional - List of tasks in checkbox markdown format `- [ ] task `. This file is used to control of the steps execution order and as a memory aid for the AI.
│   └── schema.json       # Optional
└── references/           # Optional - links to local docs
    └── docs.md           # Optional - File in markdown format with references to local documentation that the AI can use to create the output document
```

## SKILL.md Template

Follow this [template](./assets/template-skill.md) when creating a new skill.

## Taxonomy and Naming Conventions

| Type             | Pattern             | Description                                                         | Examples                                          |
| ---------------- | ------------------- | ------------------------------------------------------------------- | ------------------------------------------------- |
| Generic skill    | `{technology}`      | General knowledge                                                   | `pytest`, `playwright`, `typescript`              |
| Actionable skill | `{action}-{target}` | Performs a specific action usually to create a document or artifact | `create-skill`, `create-jira-task`, `review-code` |
| Workflow skill   | `{workflow}`        | Guides through a multi-step process                                 | `implement-user-story`, `create-software-architecture`     |

### Workflow Skills
Workflow skills will be designed to execute a series of steps to produce a comprehensive output. Each step corresponds to a section in the output document and has its own detailed instructions and information sources. To avoid overwhelming the AI with too much context, the workflow skill will load only the relevant step instructions and information sources for the current step being executed. This allows for a focused and efficient generation process while still leveraging the full depth of information available in the workspace. The way to design an efficient workflow skill follow the next principles:

- SKILL.md : Describe the overall workflow, the expected output, and the triggers for loading the skill. Include instructions for how to proceed through the steps and how to track progress. Explain the resources available for the workflow and how load them step by step. Specify as very important to not load all resources at once, but only the relevant ones for each step.
- assets/workflow.yaml : Define the sequence of steps in the workflow, with references on how execute each step or quality check verifications. It can contains conditions to control the flow can also be included here. 
- assets/step-{n}-{name}.md : For each step, create a detail file
- assets/template-{optional number}.md : Template of expected output. This can be one or many depending on the complexity of the workflow. 

Workflows require a strategy to control the execution of each step and help as memory to allow the user review , validate or resume the workflow at any moment. This can be achieved by 

- front-matter : using a front-matter field `progress` with the name of the step and its status (not started, doing, draft, done)  
- file : creating a file in the workspace with a list of tasks in checkbox markdown format `- [ ] task ` or yaml with a step and state to control of the steps execution order and as a memory aid for the AI. This file can be generated by the workflow skill at the beginning of the execution and updated after each step is completed.

The agent will check workflow state and load the relevant step instructions and resources and resume the workflow until all steps are completed. The user can also ask to review or modify the workflow state, or to jump to a specific step if needed.

**Very Important**: Evaluate if step files are really needed. If the step description is simple enough to be included in the workflow file, avoid creating separate files for each step. The goal is to provide clear instructions without overwhelming the AI with too many documents. Use step files only when the instructions are complex or require specific information sources that cannot be easily summarized in the workflow file.

## Front-matter Fields

| Field              | Required | Description                           |
| ------------------ | -------- | ------------------------------------- |
| `name`             | Yes      | Skill identifier (lowercase, hyphens) |
| `description`      | Yes      | Single line with What + Trigger (see below) |
| `user-invocable`   | No       | General knowledge skills have to be false, otherwise skip |
| `metadata.version` | Yes      | Version                               |

### Writing the `description` Field

The `description` is the **primary trigger mechanism** — the AI loads the skill based on semantic match against this field. The skill name alone does not trigger loading.

A good description has two parts:

```
{What the skill produces or does, single line expression avoid details about how be cociese of the output}. Trigger: {When the AI should load it}.
```

**Rules for the Trigger clause:**
- Cover **creation verbs**: create, write, generate, add
- Cover **transformation verbs**: transform, convert, turn into, reformat, update, restructure
- Cover **consultation queries**: "how should I document X", "what's the best way to...", "help me structure..."
- Cover **multiple surfaces**: don't list only one action — users approach the same task with different words

**Examples:**

| Too narrow | Better |
|---|---|
| `Trigger: When user asks to create an article.` | `Trigger: When user asks to write, create, or format an article — or wants to transform raw content, notes, or ideas into a publishable format.` |
| `Trigger: When user asks to document a pattern.` | `Trigger: When user asks to document, capture, write, or structure a design pattern, a recurring practice, or a proven solution — including "how should I document X" or "turn this into a pattern".` |

## Portability Principle

Skills must be **exportable between projects**. A skill created in one workspace should work in any other workspace that follows the same conventions.

To achieve this:
- **Do NOT hardcode specific file paths** (e.g., `01-kickoff/`, `02-management/21-meeting-notes/`, `README.md`)
- **Refer to folders and files by their purpose** (e.g., "the kickoff folder", "the meeting notes folder", "the project brief file")
- **Defer path resolution to the workspace organization** defined in the project's global instructions (eg. `copilot-instructions.md`)
- **Never assume a fixed folder structure** — the workspace organization is external to the skill


## Content Guidelines

### DO
- Start with the most critical patterns
- Use tables for decision trees
- Keep code examples minimal and focused
- Include Commands section with copy-paste commands
- Avoid duplicate content from existing docs (reference instead)
- Reference locations by purpose, not by path
- Skip emojis
- Use expression "search architecture folder" or "search for file" instead mention relative or absolute paths for resources outside the skill
- You can mention "load skills to achieve your task" instead of mentioning specific skill names to avoid hardcoding dependencies between skills

## Checklist Before Creating

- [ ] Skill doesn't already exist (check `skills/`)
- [ ] Pattern is reusable (not one-off)
- [ ] Identify type of skill (generic, actionable, workflow)
- [ ] Ask user for specific details if needed (technology, action, workflow name)
- [ ] Confirmed no workspace-specific paths will be hardcoded in the skill

## Checklist After Publishing
- [ ] Name follows conventions
- [ ] Frontmatter is complete
- [ ] Description covers creation, transformation, AND consultation triggers (not just creation verbs)
- [ ] Critical patterns are clear
- [ ] Code examples are minimal
- [ ] Commands section exists
- [ ] No hardcoded file paths — locations are referenced by purpose only
- [ ] Skill is portable: it would work in any workspace following the same conventions


## Resources

- **Templates**: See [assets/](assets/) for SKILL.md template