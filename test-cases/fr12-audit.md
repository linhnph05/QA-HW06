# FR-12 Human Audit

I reviewed the 35 AI cases against FR-12, FR-19, SEC-01 to SEC-07, the API specification, and normal Bearer-token parsing rules.

| ID | Label | Human reason | Correction for final test |
|---|---|---|---|
| FR12-AI-01 | INCOMPLETE | The user-list fields are inferred from code, not fully defined by the API specification. | Assert array shape, required public/admin fields, and absence of secrets; do not invent an exact whole-object schema. |
| FR12-AI-02 | VALID | An empty collection should be represented by an empty JSON array. | None. |
| FR12-AI-03 | INCOMPLETE | Password and reset token must be absent, but the spec does not say phone is secret from an admin. | Forbid `password` and `reset_token`; allow documented management fields such as phone. |
| FR12-AI-04 | INCOMPLETE | An API JSON response cannot prove the admin UI escapes stored text. | Assert JSON content type here and add a separate browser check that the admin UI does not execute the value. |
| FR12-AI-05 | VALID | It checks Unicode and nullable field schema. | None. |
| FR12-AI-06 | VALID | SEC-02 requires a token. | None. |
| FR12-AI-07 | VALID | An empty authorization value is unauthenticated. | None. |
| FR12-AI-08 | VALID | A Bearer scheme without credentials is unauthenticated. | None. |
| FR12-AI-09 | VALID | A raw JWT must not be accepted without the scheme. | None. |
| FR12-AI-10 | VALID | A JWT under the Basic scheme must not be accepted. | None. |
| FR12-AI-11 | INVALID | Bearer authentication grammar permits one or more spaces, so two spaces should not change authorization. | Expect the same 200 result as a normal admin token after trimming valid whitespace. |
| FR12-AI-12 | VALID | HTTP authentication schemes are case-insensitive. | None. |
| FR12-AI-13 | VALID | A malformed JWT must be rejected. | None. |
| FR12-AI-14 | VALID | Signature validation is required by SEC-02. | None. |
| FR12-AI-15 | VALID | Editing a payload without resigning must fail. | None. |
| FR12-AI-16 | VALID | Expired JWTs must be rejected. | None. |
| FR12-AI-17 | VALID | `alg:none` must never bypass signature validation. | None. |
| FR12-AI-18 | VALID | This is the main SEC-03 normal-user denial case. | None. |
| FR12-AI-19 | VALID | It checks the allowed admin role partition. | None. |
| FR12-AI-20 | VALID | A token without role cannot meet SEC-03. | None. |
| FR12-AI-21 | VALID | Only the exact stored role `admin` is authorized. | None. |
| FR12-AI-22 | VALID | Null role is not admin. | None. |
| FR12-AI-23 | VALID | It connects SEC-06 role escalation to FR-12 access. | None. |
| FR12-AI-24 | VALID | Extra registration fields must not create an admin. | None. |
| FR12-AI-25 | VALID | A normal user cannot use an admin delete route, even on their own ID. | None. |
| FR12-AI-26 | VALID | It covers IDOR against another user's ID. | None. |
| FR12-AI-27 | INCOMPLETE | The delete behavior is right, but the response body is not specified. | Assert success status and that only the disposable target is gone; do not require an invented exact body. |
| FR12-AI-28 | VALID | It checks path-parameter SQL injection and deletion scope. | None. |
| FR12-AI-29 | VALID | Anonymous mutation must be blocked before database access. | None. |
| FR12-AI-30 | VALID | FR-12 applies consistently to admin order reads. | None. |
| FR12-AI-31 | VALID | A normal user must not mutate order state. | None. |
| FR12-AI-32 | VALID | A normal user must not create coupons. | None. |
| FR12-AI-33 | VALID | A normal user must not delete coupons. | None. |
| FR12-AI-34 | VALID | Bulk product import is an admin-only mutation. | None. |
| FR12-AI-35 | VALID | FR-12 also protects data-changing product APIs. | None. |

## Audit result

- Valid: 30
- Invalid: 1
- Incomplete: 4
- Total reviewed: 35

