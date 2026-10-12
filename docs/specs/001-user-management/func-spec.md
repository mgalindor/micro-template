# user-management — Functional Specification

## Overview

This feature adds authentication and user administration to the backend. It exposes an OAuth2-compatible
password grant endpoint that exchanges a username and password for a signed JWT access token, and it lets
an administrator manage user accounts (creation, data updates, deactivation). Roles and the permissions
they grant are administered directly in the database and are embedded in the JWT so other modules can
authorize requests without querying the database on every call.

## Feature

### Authentication

A client submits a username and password using the standard OAuth2 password grant, form-encoded request.
On success, the system returns a signed JWT access token in the standard OAuth2 bearer response shape. The
token carries the user's identity, the names of their assigned roles, and the deduplicated list of
permissions granted by those roles, each in its own claim. Tokens expire after 30 minutes and there is no
refresh token; the client must re-authenticate when the token expires. Disabled users cannot obtain a new
token even with correct credentials.

### User creation

An administrator creates new user accounts by providing a username (max 30 characters), an optional email,
a password, and the roles to assign. Passwords are hashed with bcrypt before being stored and are never
returned in plain text. Usernames are unique across the system.

### User data update

A user can update their own email and password; changing their own password requires confirming the
current password. An administrator can update any user's email, password, and role assignments without
providing the current password.

### User deactivation

An administrator can disable a user account. Disabling marks the account inactive without deleting the
record: the user is preserved for historical purposes but can no longer authenticate or obtain new tokens.

### Roles and permissions

Roles and their permissions are administered directly in the database; this feature does not expose an API
to create, update, or delete roles or permissions. Each role has a name and a list of permissions. A user
can be assigned one or more roles. When a token is issued, permissions from all of the user's roles are
aggregated into a single deduplicated list for the JWT.

### Admin bootstrap

On startup, the system ensures a default admin user exists. The admin username and password come from
environment variables; the password variable already holds the bcrypt hash, not a plain-text password. If
the admin user already exists, startup does not recreate or overwrite it.

## Requirements

### Authentication
- [ ] The user can authenticate with a username and password using an OAuth2 password grant, form-encoded request.
- [ ] The system returns an access_token and token_type on successful authentication, matching the OAuth2 password grant response shape.
- [ ] The system embeds the user's role names in a dedicated JWT claim.
- [ ] The system embeds the deduplicated permissions derived from the user's roles in a separate JWT claim.
- [ ] The system rejects authentication for disabled users.
- [ ] The system rejects authentication for invalid credentials.
- [ ] The access token expires 30 minutes after issuance.

### User creation
- [ ] The admin can create a user by providing username, optional email, password, and roles.
- [ ] The system rejects creation when the username already exists.
- [ ] The system rejects usernames longer than 30 characters.
- [ ] The system stores the password hashed with bcrypt.
- [ ] Only a user with the admin role can create users.

### User data update
- [ ] The user can update their own email and password.
- [ ] The system requires the current password when a user changes their own password.
- [ ] The system rejects a self-service password update when the current password confirmation does not match.
- [ ] The admin can update any user's email, password, and roles without providing the current password.

### User deactivation
- [ ] The admin can disable a user account.
- [ ] The system prevents a disabled user from authenticating or obtaining a new token.
- [ ] Disabling a user does not delete their record.
- [ ] Only a user with the admin role can disable users.

### Roles and permissions
- [ ] A user can be assigned one or more roles.
- [ ] A role has a list of permissions stored in the database.
- [ ] The system does not expose an API to create, update, or delete roles or permissions.
- [ ] The system deduplicates permissions aggregated from multiple roles before writing the JWT claim.

### Admin bootstrap
- [ ] The system creates a default admin user from environment variables if it does not already exist.
- [ ] The environment variable for the admin password holds a value already hashed with bcrypt.
- [ ] The system does not overwrite an existing admin user on subsequent startups.
