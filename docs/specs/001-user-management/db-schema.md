# Relational Model — user-management

## New tables

```dbml
Table users {
  id             integer       [pk, increment]
  username       varchar(30)   [not null, unique]
  email          varchar(255)  [unique, note: 'optional']
  password_hash  varchar(255)  [not null, note: 'bcrypt hash']
  is_active      boolean       [not null, default: true]
  created_at     timestamp     [default: `CURRENT_TIMESTAMP`]
  updated_at     timestamp     [default: `CURRENT_TIMESTAMP`]

  indexes {
    username [name: 'uq_users_username', unique]
    email [name: 'uq_users_email', unique]
  }
}

Table roles {
  id           integer       [pk, increment]
  name         varchar(50)   [not null, unique, note: 'administered directly in the database, no API']
  permissions  jsonb         [not null, default: '[]', note: 'list of permission strings granted by this role']
  created_at   timestamp     [default: `CURRENT_TIMESTAMP`]
  updated_at   timestamp     [default: `CURRENT_TIMESTAMP`]

  indexes {
    name [name: 'uq_roles_name', unique]
  }
}

Table user_roles {
  user_id  integer  [ref: > users.id, not null]
  role_id  integer  [ref: > roles.id, not null]

  indexes {
    (user_id, role_id) [pk]
  }
}
```
