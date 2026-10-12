<!--
TEMPLATE GUIDE
This feature is built inside an app that already has its own architecture, stack, and module conventions (see the app's
own tec-spec.md and the backend coding skill) — do not redefine them here, only describe what this feature adds or
changes. Keep this document short and link to func-spec.md / api.md / db-schema.md instead of repeating their content.
Delete this comment before saving.
-->

# {feature-name} — Technical Specification

<!-- 1 paragraph: what this feature adds to the app. Link to func-spec.md. -->
## Overview

{tec-spec-overview}

<!--
How this feature fits the existing module convention: a new module under modules/, or changes to an existing module.
List new/changed router, service, repository, domain pieces. Reference api.md and db-schema.md instead of repeating
endpoints or tables.
-->
## Design

{design-notes}

<!-- One subsection per non-trivial flow: a background job, a call to an external service, a multi-step validation, etc. -->
## Key Flows

### {flow-1-name}

{flow-1-steps}

<!-- New dependencies/libraries, config/env vars, migrations, or anything else that doesn't fit above. Omit if none apply -->
## Additional Considerations

{additional-considerations}
