<!--
TEMPLATE GUIDE
One "##" section per functional area, using the same area names and order as func-spec.md's "Requerimientos" section.
Each endpoint is a single checklist line: `METHOD /path — short description`.
Use "- [ ]" for endpoints to build; "- [x]" only if already implemented elsewhere in the app and reused as-is.
Paths are resource-oriented and in English, nested under their parent resource when they belong to it
(e.g. /trips/{trip_id}/expenses). Delete this comment before saving.
-->

# {feature-name} — API

## {feature-area-1-name}
- [ ] {METHOD} {path} — {short-description}
```yaml
# {HTTP-METHOD} {/api/path}
security:
  type:   # jwt, basic, oauth2, public
  role:   # admin, user, public
request:
  {field-name}: {example-value}  # type, required|optional, constraints
response:
  {field-name}: {example-value}  # type, required|optional, constraints
```

## {feature-area-2-name}
- [ ] {METHOD} {path} — {short-description}
```yaml
# {HTTP-METHOD} {/api/path}
security:
  type:   # jwt, basic, oauth2, public
  role:   # admin, user, public
request:
  {field-name}: {example-value}  # type, required|optional, constraints
response:
  {field-name}: {example-value}  # type, required|optional, constraints
```