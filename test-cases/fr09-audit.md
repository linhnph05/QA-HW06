# FR-09 Human Audit

I reviewed the 35 AI cases against FR-09, FR-17, SEC-02, SEC-04, SEC-05, and the API specification. A valid JWT is authoritative; a client-supplied `user_id` must never choose whose usage limit is checked.

| ID | Label | Human reason | Correction for final test |
|---|---|---|---|
| FR09-AI-001 | VALID | It checks the required percent formula with a known coupon. | None. |
| FR09-AI-002 | VALID | It checks the required fixed-discount formula. | None. |
| FR09-AI-003 | VALID | Coupon code is required. | None. |
| FR09-AI-004 | VALID | Null is outside the code domain. | None. |
| FR09-AI-005 | VALID | Empty code is invalid. | None. |
| FR09-AI-006 | VALID | Whitespace-only code is invalid. | None. |
| FR09-AI-007 | VALID | C1 requires an existing active code. | None. |
| FR09-AI-008 | INCOMPLETE | The requirements do not define case sensitivity. | Expect exact matching for the current database and record case sensitivity as an assumption. |
| FR09-AI-009 | VALID | C1 explicitly rejects inactive coupons. | None. |
| FR09-AI-010 | VALID | It directly checks SEC-05. | None. |
| FR09-AI-011 | VALID | It checks hostile text handling under SEC-04. | None. |
| FR09-AI-012 | VALID | `total_amount` is required for all calculations. | None. |
| FR09-AI-013 | VALID | Null is not a valid monetary total. | None. |
| FR09-AI-014 | VALID | Zero is below the seeded positive minimum. | None. |
| FR09-AI-015 | VALID | A negative order total is invalid. | None. |
| FR09-AI-016 | VALID | A numeric string should not silently change type. | None. |
| FR09-AI-017 | VALID | An object total must be rejected without a crash. | None. |
| FR09-AI-018 | VALID | It covers one unit below the minimum. | None. |
| FR09-AI-019 | VALID | FR-09 says the minimum comparison is greater than or equal. | None. |
| FR09-AI-020 | VALID | It covers one unit above the minimum and rounding. | None. |
| FR09-AI-021 | INCOMPLETE | Vietnamese dong normally uses integer units, but the spec does not state decimal handling. | Reject fractional `total_amount` as 400 and document the integer-money assumption. |
| FR09-AI-022 | VALID | C2 rejects expired coupons. | None. |
| FR09-AI-023 | VALID | Equality is not before the expiry time, so it is expired. | None. |
| FR09-AI-024 | VALID | A future expiry satisfies C2. | None. |
| FR09-AI-025 | INVALID | FR-17 requires a positive `discount_value`; a zero-value coupon is invalid test data. | Expect the coupon creation/setup to reject zero, or expect apply-coupon to reject the invalid configuration. |
| FR09-AI-026 | VALID | A 100% coupon follows the specified formula and gives final amount zero. | None. |
| FR09-AI-027 | VALID | A 101% stored value is invalid and must not create a negative total. | None. |
| FR09-AI-028 | INCOMPLETE | The formula allows a negative result, but safe business behavior is not defined. | Assert that `final_amount` is never below zero; accept reject or cap-at-zero only after the product rule is confirmed. |
| FR09-AI-029 | VALID | FR-17 limits type to percent or fixed. | None. |
| FR09-AI-030 | VALID | C4 and SEC-02 require a JWT. | None. |
| FR09-AI-031 | VALID | An invalid JWT must not access the coupon operation. | None. |
| FR09-AI-032 | INCOMPLETE | Rejecting a body `user_id` is not necessary if the server ignores it. | Ignore body `user_id` and use only the JWT subject for usage checks. |
| FR09-AI-033 | VALID | It is the main IDOR/usage-limit bypass case. | None. |
| FR09-AI-034 | VALID | It covers the C5 state boundary before and at the maximum. | None. |
| FR09-AI-035 | INCOMPLETE | The spec names two required fields but does not forbid extra response fields. | Assert required numeric fields and formula invariants; do not reject harmless documented extras. |

## Audit result

- Valid: 29
- Invalid: 1
- Incomplete: 5
- Total reviewed: 35

