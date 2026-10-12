---
name: coding-rest-api
description: "Trigger: when the user asks to create, design, review, or document a REST endpoint/API, or asks how to name routes, which verb/status code to use, or how to structure an error response."
metadata:
    type: skill
    version: "1.1.0"
    updated-at: "2026-10-11"
    author:
      name: "Miguel Galindo Rodriguez"
      email: "mgldrz@gmail.com"
---

# REST API Best Practices


## 1. Resource Naming

- Use **plural nouns**, never verbs: `/users`, `/orders`, not `/getUsers` or `/createOrder`.
- Nest resources only when the child cannot exist without the parent: `/orders/{order_id}/items`.
- IDs go in the path, filters/sorting/pagination go in query params: `/users/{user_id}`, `/users?status=active&page=2`.
- Do not include the version inside the resource name; it goes as a prefix: `/v1/users`.

## 2. HTTP Verbs

| Verb     | Use                                      | Idempotent | Body in response     |
|----------|-------------------------------------------|:----------:|:---------------------:|
| `GET`    | Read one or many resources                | Yes        | Yes                   |
| `POST`   | Create a new resource / non-idempotent action | No     | Yes (created resource) |
| `PUT`    | Replace a resource entirely                | Yes        | Optional               |
| `PATCH`  | Partially update a resource                | No*        | Optional               |
| `DELETE` | Delete a resource                          | Yes        | No (204)               |

\* `PATCH` can be designed idempotent (e.g. JSON Merge Patch) but it's not guaranteed by default.

**Golden rule:** the HTTP verb already expresses the action; the resource name must never repeat it.

## 3. Request and Response Body

- Every request and response body **must be a JSON object**, never a bare JSON array. Wrap collections in an object field, e.g. `{ "data": [...] }`.
  - Why: a top-level array cannot be extended later (pagination metadata, totals, links) without a breaking change for clients.
- A `GET` endpoint with filters that finds no matching records is **not an error**: return `200 OK` with an empty array in the collection field, e.g. `{ "data": [] }`. Never return `404` for an empty filtered list.
- Reserve `404` for when a specific resource identified by an ID in the path does not exist (see section 4).
- All fields in the request body have to include constraint validations such as type, format, required field, range, and regex, and need to be validated before processing the request.

## 4. Status Codes

Use the most specific code possible, not just generic `200` or `400`.

| Range | Meaning | Common examples |
|-------|---------|------------------|
| `2xx` | Success | `200 OK` (successful GET/PUT/PATCH, including empty filtered results), `201 Created` (POST that creates a resource), `204 No Content` (successful DELETE or response without body) |
| `4xx` | Client error | `400 Bad Request`, `404 Not Found`, `412 Precondition Failed` (see details below) |
| `5xx` | Server error | `500 Internal Server Error` (unhandled), `503 Service Unavailable` (dependency down) |

### 400 Bad Request — input validation

Use `400` when the request payload itself is malformed or fails field-level validation (type, format, required field, range, regex, etc.), **before** any business logic runs.

- Examples: missing required field, invalid email format, string where a number was expected, value outside allowed range.
- The response must list **every** invalid field, not just the first one found (see `location` in section 5).

### 404 Not Found — resource does not exist

Use `404` when the request references a resource **by ID** (in the path) and that ID does not exist in the database.

- Example: `GET /users/123` when no user with id `123` exists.
- Also applies to `PUT`, `PATCH`, and `DELETE` on a non-existent ID.
- If the resource exists but the caller must not know that it exists (authorization), prefer `404` over `403` to avoid leaking information.

### 412 Precondition Failed — business rule violation

Use `412` when the payload is well-formed and the referenced resources exist, but the operation violates a **business rule** (domain invariant), not a field validation.

- Examples: cancelling an order that has already shipped, withdrawing more balance than available, activating a user that is already active.
- Distinguish from `400`: `400` is "this data is not valid on its own"; `412` is "this data is valid, but the current state of the system does not allow this operation".
- Distinguish from `409 Conflict`: use `409` for concurrent-modification/duplicate-state conflicts (e.g. unique constraint), and `412` for explicit business-rule checks performed by the service layer.

## 5. Error Handling — Problem Details (RFC 7807)

All error responses must use the `application/problem+json` media type and follow the [Problem Details](https://www.rfc-editor.org/rfc/rfc7807) shape:

```json
{
  "type": "https://example.com/probs/not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with id 123 was not found",
  "instance": "/users/123"
}
```

- `type`: a stable URI identifying the error kind (can be a documentation link); clients may use it for `if/switch` logic.
- `title`: short, human-readable summary of the error kind, constant across occurrences.
- `status`: the HTTP status code, duplicated in the body for logging/clients that don't read headers.
- `detail`: human-readable explanation specific to this occurrence.
- `instance`: the request path that triggered the error.
- Never expose internal details (stack traces, SQL queries, file paths) in `detail`.

### Extension: `location` for field-level validation errors (400)

For `400 Bad Request` responses caused by input validation, extend Problem Details with a `location` array that pinpoints each invalid field, so clients can map errors back to form fields:

```json
{
  "type": "https://example.com/probs/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "One or more fields are invalid",
  "instance": "/users",
  "location": [
    { "name": "email", "description": "must be a valid email address" },
    { "name": "user.age", "description": "must be greater than 0" }
  ]
}
```

- `location` is an array; include **one entry per invalid field**, never truncate to the first error.
- `name`: the field name as it appears in the request body (use dotted path for nested fields, e.g. `address.zip_code`).
- `description`: human-readable reason that field failed validation.

### Example: 412 business rule violation

```json
{
  "type": "https://example.com/probs/business-rule-violation",
  "title": "Business Rule Violation",
  "status": 412,
  "detail": "Order 55 cannot be cancelled because it has already shipped",
  "instance": "/orders/55/cancel"
}
```