---
metadata:
    type: instructions
    version: "1.0.0"
    updated-at: "2026-10-11"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

# Naming Conventions
- Kebab-case only  Use lowercase and hyphens for all file and folder names e.g., `my-file.md`, `my_file.txt`, folder `project-management`. 
- Use `.md` for all documentation and text content.
- Only when creating new documentation files of the same type in a folder, include a date prefix in `YYYYMMDD` format for versioning and tracking. e.g., `20240601-project-overview.md` when format is not specified by instructions or template. 

# Versioning

- Use semantic versioning for any documents that are expected to evolve over time, especially templates and skills, architecture, database documentation
- Start with version `1.0.0` for new documents and update as needed when changes are made  include in the front matter as `version: 1.0.0` and `updated` date (format: YYYY-MM-DD)

# Working Mode
Working mode is selected in the front matter of the readme


- strict: Require creates specs before proceeding with any implementation. 
- relaxed: For non technical users, require capture specs but user only describe functionality and features without delving into technical details. agents generates technical details based on the captured specs.
- yolo: For non technical users, allow proceeding without capturing detailed specs, prioritizing speed and experimentation.