---
name: capture-feature
description: "Trigger: when the user requests, proposes, or wants to describe/document/capture a new feature, functionality, or module to add to the app, when user wants to add new code in the project"
user-invocable: false
metadata:
    type: skill
    version: "1.0.0"
    updated-at: "2026-10-11"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

## Critical Patterns

- Specs live in the specs folder, one subfolder per feature: `{number}-{kebab-case-feature-name}` (e.g. `001-expenses`, `002-notifications`).
- `{number}` is a 3-digit, zero-padded sequence. Find the highest existing number in the specs folder and increment by 1.
- Each feature folder contains 4 documents, always created in this order: `func-spec.md` → `api.md` → `db-schema.md` → `tec-spec.md`. Do not start a later document until the previous one is confirmed with the user.
- Write every generated document in English, including section headers and code identifiers (table/column names, endpoint paths).
- Interview the user to fill each template — never invent requirements, endpoints, or fields. Ask focused questions when information is missing.
- When interviewing, explicitly ask which fields/columns need to be captured for each entity and whether the user can provide an example value so the expected format is clear.
- Each document must reference the previous ones instead of repeating their content (e.g. `tec-spec.md` links to `api.md`/`db-schema.md` rather than re-listing endpoints or tables).
- Remove all guidance comments (`<!-- ... -->`) from the generated files; they only exist to guide the fill-in process and must not appear in the final document.

## Workflow

1. Ask the user for a short feature name and a free-form description of what they want to build.
2. Determine the next feature number and create the folder `{number}-{kebab-case-feature-name}` in the specs folder.
3. Copy [assets/template-func-spec.md](assets/template-func-spec.md) into the new folder as `func-spec.md`, interview the user to fill it in, then confirm the result before continuing.
4. Repeat the copy → interview → confirm cycle for [assets/template-api.md](assets/template-api.md) → `api.md`, [assets/template-db-schema.md](assets/template-db-schema.md) → `db-schema.md`, and [assets/template-tec-spec.md](assets/template-tec-spec.md) → `tec-spec.md`, in that order.
5. When all 4 documents are confirmed, summarize the created folder and files to the user.

## API and Events Contract Notation

Use the lightweight YAML notation for all API input/output contracts. Every field comment must include: data type, required/optional, and applicable constraints (min/max length/value, enum values, format, ISO standard).

Always include the HTTP method and path or event name (in case documenting an event) as a header comment above the contract block.

```yaml
# POST /users  or 'on user-created'
security:
  type: jwt       # jwt, basic, oauth2, public
  role: admin     # admin, user, public
request:
  name: str       # str, required, min: 2, max: 100
  email: str      # str, required, email format
  age: int        # int, optional, min: 0, max: 150
  status: str     # str, required, enum: [active, inactive]
  nested: 
    field1: str    # str, required
    country: str    # str, required , 3char ISO 3166
response:
  id: int         # int, required
  created_at: str # str, required, ISO 8601
```

For gRPC or GraphQL, adapt the notation to the protocol but keep the same field-level comment convention.

## Database Changes

Use DBML code blocks for all table definitions. Always show the complete table definition — for modifications, add inline comments marking which fields are new or changed. Never show only the delta.

```dbml
Table users {
  id          int           [pk, increment]
  name        varchar(100)  [not null]
  email       varchar(255)  [not null, unique]
  status      varchar(20)   [not null, default: 'active']
  created_at  timestamp     [default: `now()`]

  indexes {
    email [name: 'idx_users_email', unique]
  }
}

Table bookings {
  id integer
  country varchar
  booking_date date
  created_at timestamp
  user_id integer [ref: > users.id] // link to users table field id

  indexes {
    (id, country) [pk] // composite primary key
    created_at [name: 'created_at_index', note: 'Date']
    booking_date
    (country, booking_date) [unique]
    booking_date [type: hash]
  }
}

## Templates

- [Functional spec](assets/template-func-spec.md) — feature overview, functional description, and checklist-style requirements.
- [API](assets/template-api.md) — endpoints grouped by functional area, checklist style.
- [DB schema](assets/template-db-schema.md) — DBML relational model, for new tables and/or changes to existing ones.
- [Technical spec](assets/template-tec-spec.md) — how the feature fits the existing architecture, key flows, and cross-references to `api.md`/`db-schema.md`.
