---
name: api-test-generator
description: Generate auditable CSV API test cases from a Markdown API specification. Use when an API testing task needs systematic domain partitions, negative cases, authentication checks, security checks, state checks, and response-schema checks before human review.
---

# API Test Generator

Turn API specification endpoints into a first test draft. Treat the output as input to human review, not as final truth.

## Workflow

1. Read the requested feature and its security rules in the specification.
2. Run `scripts/generate_api_tests.py <spec.md> <output.csv> [endpoint-filter]`.
3. Add feature-specific partitions from `references/test-design-guide.md`.
4. Trace each expected result back to the specification.
5. Label uncertain cases `INCOMPLETE` and ask a human to decide.
6. Check every parameter, state, role, and response field at least once.
7. Execute the reviewed CSV through Postman, Newman, or an equivalent runner.

## Output Rules

- Keep one behavior per test case.
- Include positive, negative, boundary, security, and schema cases.
- State the expected status and response shape clearly.
- Do not invent undocumented requirements without marking them as assumptions.
- Never replace human audit with generated output.

## Resources

- Run `scripts/generate_api_tests.py` for a repeatable CSV draft.
- Read `references/test-design-guide.md` when adding feature-specific cases.
