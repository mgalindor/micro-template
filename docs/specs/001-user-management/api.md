# user-management — API

## Authentication
- [ ] POST /api/token — exchange username/password for a JWT access token (OAuth2 password grant)
```yaml
# POST /api/token
security:
  type: public
  role: public
request:                   # application/x-www-form-urlencoded (OAuth2PasswordRequestForm)
  grant_type: password     # str, optional, must equal "password" when present
  username: jdoe           # str, required, max: 30
  password: s3cr3t         # str, required
response:
  access_token: eyJhbGciOi...  # str, required, signed JWT
  token_type: bearer           # str, required, constant "bearer"
```

## User creation
- [ ] POST /api/users — create a new user account
```yaml
# POST /api/users
security:
  type: jwt
  role: admin
request:
  username: jdoe            # str, required, max: 30, unique
  email: jdoe@example.com   # str, optional, email format
  password: s3cr3t          # str, required, min: 8
  roles: [viewer]           # list[str], optional, default: [], must reference existing role names
response:
  id: 1                      # int, required
  username: jdoe             # str, required
  email: jdoe@example.com    # str, optional
  roles: [viewer]            # list[str], required
  is_active: true             # bool, required
  created_at: "2026-10-12T00:00:00Z"  # str, required, ISO 8601
```

## User data update
- [ ] PUT /api/users/{user_id} — update a user's email, password, or roles
```yaml
# PUT /api/users/{user_id}
security:
  type: jwt
  role: user, admin   # a user may only target their own user_id; admin may target any user_id
request:
  email: jdoe@example.com      # str, optional, email format
  password: n3wpa55word        # str, optional, min: 8
  current_password: s3cr3t     # str, required when password is present and caller is not admin
  roles: [viewer, editor]      # list[str], optional, admin only, must reference existing role names
response:
  id: 1                      # int, required
  username: jdoe             # str, required
  email: jdoe@example.com    # str, optional
  roles: [viewer, editor]    # list[str], required
  is_active: true             # bool, required
  created_at: "2026-10-12T00:00:00Z"  # str, required, ISO 8601
```

## User deactivation
- [ ] DELETE /api/users/{user_id} — disable a user account (soft-delete, no body returned)
```yaml
# DELETE /api/users/{user_id}
security:
  type: jwt
  role: admin
request: {}
response: {}   # 204 No Content
```
