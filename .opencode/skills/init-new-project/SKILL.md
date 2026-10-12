---
name: init-new-project
description: "Trigger: when the user wants to start, bootstrap, initialize, configure, or set up a new project from this template — including 'let's start a new project', 'configure this template for a client'"
metadata:
    type: skill
    version: "1.1.0"
    updated-at: "2026-10-12"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

## Critical Patterns

- This skill only edits the root `README.md` (front matter `type: project-brief`). It is the entry point that turns the generic template into a project-specific brief.
- Assume the user may be non-technical. Explain every question and option in plain language, avoiding jargon (e.g. "front matter", "repository") — describe what each input is for in terms of the project, not the file format.
- Never invent values for client, project name, summary, or working mode — always ask the user. Only the `created-at` date is filled automatically (today's date, `YYYY-MM-DD`).
- Before asking anything, read the current front matter. If `configured: true` already, tell the user the project looks already initialized and ask for explicit confirmation before overwriting the existing values.
- The skill is only complete once `configured: true` is set — do not stop at `false` or leave it unanswered.

## Workflow

1. **Check current state**: read the README front matter (`client`, `project`, `summary`, `working-mode`, `configured`). If `configured: true`, show the current values and ask the user to confirm re-initialization before continuing.
2. **Interview the user** for the following inputs, one topic at a time:
   - `client`: the client or organization name this project is for.
   - `project`: the project name (used as the README title and the `project` front matter field). Suggest a kebab-case form if the user gives a long name.
   - `summary`: one or two sentences describing what the project does, for someone skimming the README.
   - `working-mode`: one of `strict`, `relaxed`, `yolo`. Explain the options before asking (see below) so the choice is informed.
   - `initial idea`: a free-form description (a few sentences) of what the user thinks this project should do — the rough problem or product idea, before it gets broken down into features.
3. **Update `README.md`**:
   - Front matter: set `client`, `project`, `summary`, `working-mode` to the collected values, `created-at` to today's date, and `configured: true`.
   - Replace the placeholder title `# project-name-here` with `# {project}`.
   - Add a new `## Initial idea` section right after the title (before `## Main features`) containing the user's initial idea, written as prose.
4. **Confirm and suggest next step**: show the user the updated front matter and new section, then suggest using a feature-capture skill to turn the initial idea into the first concrete feature spec.

## Working Mode Options

Explain these to the user in plain, non-technical language before they pick one (copy for the interview, do not just link to it):

- **strict**: nothing gets built until the idea is written down and agreed on first — best when you need everything documented and predictable.
- **relaxed**: you describe what you want in your own words, no technical detail needed — written notes are still kept, but the agent works out the technical side for you.
- **yolo**: skip the write-up and go straight to building — fastest option, best for quick experiments where speed matters more than documentation.

## Front Matter Result

After this skill runs, the front matter must look like this (values filled in, nothing left as a placeholder):

```yaml
---
client: {client}
project: {project}
summary: {summary}
type: project-brief
created-at: {today, YYYY-MM-DD}
working-mode: {strict|relaxed|yolo}
configured: true
---
```
