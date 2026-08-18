# Test Design Guide

For every endpoint, review these areas:

- Domain partitions: valid, missing, empty, wrong type, too short, too long, boundary, and special characters.
- State: initial state, valid transition, repeated request, invalid transition, and stale data.
- Security: missing token, invalid token, expired token, wrong role, IDOR, injection, and mass assignment.
- Schema: exact required fields, field types, no sensitive data, and correct error shape.
- Headers: content type, authorization when required, and `X-Student-Id` for homework execution.

The specification is the source of truth. Mark a test `INCOMPLETE` when the expected behavior is not defined.
