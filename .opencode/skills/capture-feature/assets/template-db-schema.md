<!--
TEMPLATE GUIDE
DBML format. For a brand-new table, add a full "Table" block under "New tables". For a change to an existing table
(new column, new index, etc.), don't repeat the whole table — list only the delta under "Changes to existing tables".
Column/table names and `note:` values are all in English. Delete this comment before saving.
-->

# Relational Model — {feature-name}

## New tables

```dbml
Table {table_name} {
  id integer [pk, increment]
  {column_name} {column_type} [not null, note: '{explanation}']
  created_at datetime [default: `CURRENT_TIMESTAMP`]
  updated_at datetime [default: `CURRENT_TIMESTAMP`]

  indexes {
    ({indexed_column})
  }
}
```

<!-- Omit this section if the feature doesn't touch existing tables -->
## Changes to existing tables

- `{existing_table}`: add column `{column_name} {column_type}` — {reason}.
