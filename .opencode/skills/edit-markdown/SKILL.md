---
name: edit-markdown
description: 'markdown formatting guidelines for project documentation'
metadata:
    type: skill
    version: "1.0.0"
    updated-at: "2026-10-11"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

# Markdown Formatting Guidelines
- Do not include by default line separator Eg. `---` in markdown documents, only when explicitly required by the template or instructions.

# Documentation Front Matter
- All markdown project documentation files must include a YAML front matter header at the top of the document enclosed by `---` lines
- The front matter should include the following fields:
  - `title`: A clear and descriptive title of the document
  - `created-at`: The date when the document was created or last updated (format: YYYY-MM-DD)
  - `type`: The type of document See [Document types](#document-types)

## Document types

| Front matter type   | Code | Name                         | Description                                                                                                                                                                                                                                                                                    |
| :------------------ | :--- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `analysis`          | ANL  | Analysis Document            | Contains research findings, data analysis, user insights, and conclusions drawn from the analysis.                                                                                                                                                                                            |
| `architecture`      | ARC  | Architecture Document        | Describes the overall structure, components, and design decisions of a system or project.                                                                                                                                                                                                      |
| `change-management` | CM   | Change Management Document   | Outlines the process, steps, and communication plan for managing changes in a project or organization.                                                                                                                                                                                         |
| `decision-record`   | DR   | Decision Record              | Documents important decisions made during a project, including the context, options considered, and rationale for the chosen solution.                                                                                                                                                         |
| `discovery`         | DSC  | Discovery Document           | Contains research findings, user insights, market analysis, and requirements gathering information collected during the discovery phase of a project.                                                                                                                                         |
| `management`        | MGMT | Management Document          | Contains project management artifacts such as timelines, resource allocation, progress tracking, and status reports.                                                                                                                                                                         |
| `meeting-notes`     | MN   | Meeting Notes                | Records the discussions, decisions, and action items from a meeting.                                                                                                                                                                                                                           |
| `project-brief`     | BRF  | Project Brief                | A high-level overview of a project including objectives, key stakeholders, expected outcomes, challenges, and team. Client-facing entry point to the repository. Lives in README.md.                                                                                                           |
| `reference`         | REF  | Reference Document           | Provides background information, research, or supporting materials relevant to a project or topic. External or third-party information provided as input, constraint, or integration guide. Includes client-provided data, API specifications, integration guidelines, and external standards. |
| `risk-management`   | RM   | Risk Management Document     | Identifies potential risks, their impact, likelihood, and mitigation strategies for a project or organization.                                                                                                                                                                                 |
| `sow`               | SOW  | Statement of Work            | Defines the scope, deliverables, timeline, and terms of a project or engagement.                                                                                                                                                                                                               |
| `specification`     | SP   | Specification                | Describes a feature or functionality it could be a user story or technical task implementation specification                                                                                                                                                                                   |
| `tech-manual`       | TM   | Technical Manual             | Provides detailed instructions, guidelines, and information for using or maintaining a system, product, or technology.                                                                                                                                                                         |
| `transcript`        | TR   | Transcript                   | A verbatim record of spoken communication, such as an interview, presentation, or conversation.                                                                                                                                                                                                |
| `user-manual`       | UM   | User Manual                  | Provides instructions and information for end users on how to use a product, system, or service.                                                                                                                                                                                               |


# Tasks
- When creating tasks, actionable activities or action items in any documents, use the following format:
`- [ ] Task description here`
- This format creates a checkbox that can be marked as completed when the task is done. For example:
`- [X] Schedule follow-up meeting with the client` indicates that the task has been completed, while `- [ ] Schedule follow-up meeting with the client` indicates that the task is still pending.
- Tasks can contains additional metadata in the next format `[metadata:: metadata-value]` for example:
`- [ ] Schedule follow-up meeting with the client [priority:: high] [due:: 2024-07-01]` indicates that the task has a high priority and is due by July 1, 2024.
- Common metadata fields include (**Very important not all fields are required.Only use when required**) :
  - `priority`: low, medium, high
  - `owner`: name or email or company name of the person responsible for the task
  - `due`: YYYY-MM-DD format date for when the task is due
  - `created`: YYYY-MM-DD format date for when the task was created
  - `completion`: YYYY-MM-DD format date for when the task was completed
  - `start`: YYYY-MM-DD format date for when the task is started
  - `scheduled`: YYYY-MM-DD format date for when the task is scheduled
- **Very important:** Mark tasks as completed by changing the checkbox from `[ ]` to `[X]` and adding the completion date in the metadata exactly after was completed, for example:
`- [X] Schedule follow-up meeting with the client [due:: 2024-07-01] [completion:: 2024-06-30]` indicates that the task was completed on June 30, 2024.


# Blockquotes
- Use simple `>` for blockquotes to highlight information
- Use `> [!NOTE]` to highlights information that users should take into account, even when skimming.
- Use `> [!TIP]` to highlights for optional information to help a user be more successful.
- Use `> [!IMPORTANT]` to highlights for crucial information necessary for users to succeed.
- Use `> [!WARNING]` to highlights for critical content demanding immediate user attention due to potential risks.
- Use `> [!CAUTION]` to highlights for negative potential consequences of an action.