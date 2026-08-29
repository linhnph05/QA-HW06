# AI Log — FR-09

- Tool: Codex
- Date/time (Asia/Ho_Chi_Minh): 2026-08-18 12:25:59 +07

## Original prompt

> You are a helper AI being guided by a third-year software engineering student. Inspect eshop-sut/api_specification.md and the relevant implementation only to understand FR-09 (POST /api/apply-coupon, with coupon usage state when relevant). Do not edit any files. Produce exactly 35 AI-generated test-case drafts in a compact Markdown table with columns: ID, endpoint, category, precondition, request/input, expected status, expected schema/behavior. Cover domain partitions for code, total_amount, user_id, coupon type/value/minimum/expiry/usage state, boundary and state transitions, SEC-01–SEC-07 where relevant, and exact response schema. Base expected behavior on the API specification, clearly flag any assumption, and keep the output concise enough to paste into an AI audit log.

## Final output

Assumptions used in the drafts:

- The API specification guarantees `200` success with numeric `discount_amount` and `final_amount`. It does not define failure status codes or the complete failure schema. `400/401/403/404` and `{error:string}` below are assumptions based on common REST behavior and the current implementation.
- FR-09 says a valid JWT is required. Therefore, the authenticated JWT user should be authoritative; client `user_id` must not bypass usage limits.
- Percentage calculation follows the requirement: `floor(total_amount × discount_value / 100)`.
- Coupon fixtures outside the seeded data require test setup.
- SEC-01, SEC-03, SEC-06, and SEC-07 are not applicable to this non-password, non-admin, non-profile, non-OTP endpoint. SEC-02, SEC-04, and SEC-05 are relevant.

| ID | endpoint | category | precondition | request/input | expected status | expected schema/behavior |
|---|---|---|---|---|---|---|
| FR09-AI-001 | POST `/api/apply-coupon` | Happy path/percent | Valid JWT; active `SAVE10`, 10%, min 300000, future expiry, usage 0/1 | `{"code":"SAVE10","total_amount":500000,"user_id":1}` | 200 | JSON contains numeric `discount_amount:50000`, `final_amount:450000`. |
| FR09-AI-002 | POST `/api/apply-coupon` | Happy path/fixed | Valid JWT; active `BIGBUY`, fixed 50000, min 500000, future expiry, usage 0/1 | `{"code":"BIGBUY","total_amount":600000,"user_id":1}` | 200 | `discount_amount:50000`, `final_amount:550000`. |
| FR09-AI-003 | POST `/api/apply-coupon` | Code partition/missing | Valid JWT | `{"total_amount":500000,"user_id":1}` | 400* | `{error:string}`; coupon is not applied. |
| FR09-AI-004 | POST `/api/apply-coupon` | Code partition/null | Valid JWT | `{"code":null,"total_amount":500000,"user_id":1}` | 400* | `{error:string}`; no database/state change. |
| FR09-AI-005 | POST `/api/apply-coupon` | Code boundary/empty | Valid JWT | `{"code":"","total_amount":500000,"user_id":1}` | 400* | `{error:string}`. |
| FR09-AI-006 | POST `/api/apply-coupon` | Code boundary/whitespace | Valid JWT | `{"code":"   ","total_amount":500000,"user_id":1}` | 400* | `{error:string}`; whitespace-only code is invalid. |
| FR09-AI-007 | POST `/api/apply-coupon` | Code partition/unknown | Valid JWT; code absent from DB | `{"code":"NO_SUCH_CODE","total_amount":500000,"user_id":1}` | 404* | `{error:string}`; no discount. |
| FR09-AI-008 | POST `/api/apply-coupon` | Code/case sensitivity | Valid JWT; only uppercase `SAVE10` exists | `{"code":"save10","total_amount":500000,"user_id":1}` | 404* | Exact-code lookup assumed; must not silently select another coupon. |
| FR09-AI-009 | POST `/api/apply-coupon` | Coupon state/inactive | Valid JWT; coupon exists with `is_active=0` | Valid code, total above minimum | 404* | `{error:string}`; inactive coupon rejected. |
| FR09-AI-010 | POST `/api/apply-coupon` | SEC-05/SQL injection | Valid JWT | `code="' OR 1=1 --"` | 404* | Treated as literal value; no coupon/data leak; parameterized query used. |
| FR09-AI-011 | POST `/api/apply-coupon` | SEC-04/injection output | Valid JWT | `code="<script>alert(1)</script>"` | 404* | JSON error must not execute/return active HTML; input must not be inserted through `innerHTML` by clients. |
| FR09-AI-012 | POST `/api/apply-coupon` | Total partition/missing | Valid JWT; valid coupon | `{"code":"SAVE10","user_id":1}` | 400* | `{error:string}`; no `NaN` or null monetary fields. |
| FR09-AI-013 | POST `/api/apply-coupon` | Total partition/null | Valid JWT | `total_amount:null` | 400* | `{error:string}`; no discount. |
| FR09-AI-014 | POST `/api/apply-coupon` | Total boundary/zero | Valid JWT; coupon minimum > 0 | `total_amount:0` | 400* | Reject below minimum; `{error:string}`. |
| FR09-AI-015 | POST `/api/apply-coupon` | Total partition/negative | Valid JWT | `total_amount:-1` | 400* | Negative order total rejected. |
| FR09-AI-016 | POST `/api/apply-coupon` | Total type | Valid JWT | `total_amount:"500000"` | 400* | Numeric string rejected rather than coerced; `{error:string}`. |
| FR09-AI-017 | POST `/api/apply-coupon` | Total type/object | Valid JWT | `total_amount:{"value":500000}` | 400* | Object rejected; no server crash or non-finite result. |
| FR09-AI-018 | POST `/api/apply-coupon` | Minimum boundary/below | Valid JWT; min 300000 | `total_amount:299999` | 400* | Below-minimum order rejected. |
| FR09-AI-019 | POST `/api/apply-coupon` | Minimum boundary/equal | Valid JWT; active `SAVE10`, usage available | `total_amount:300000` | 200 | Requirement says `>=`; discount `30000`, final `270000`. |
| FR09-AI-020 | POST `/api/apply-coupon` | Minimum boundary/above | Valid JWT; active `SAVE10` | `total_amount:300001` | 200 | Discount `30000` after integer flooring; final `270001`. |
| FR09-AI-021 | POST `/api/apply-coupon` | Decimal money | Valid JWT; percent 10%, min satisfied | `total_amount:300000.50` | 200* | Formula applied consistently; assumed discount `30000`, final `270000.50`. Currency precision is unspecified. |
| FR09-AI-022 | POST `/api/apply-coupon` | Expiry state/expired | Valid JWT; active coupon expired one second ago | Valid code and qualifying total | 400* | `{error:string}`; expired coupon rejected. |
| FR09-AI-023 | POST `/api/apply-coupon` | Expiry boundary/exact | Valid JWT; `expired_at` equals current instant | Valid code and qualifying total | 400* | Requirement says current time must be before expiry; equality is expired. |
| FR09-AI-024 | POST `/api/apply-coupon` | Expiry state/future | Valid JWT; expiry one second in future | Valid code and qualifying total | 200 | Discount calculated normally. |
| FR09-AI-025 | POST `/api/apply-coupon` | Percent value/zero | Valid JWT; active percent coupon value 0 | Total above minimum | 200* | `discount_amount:0`; `final_amount` unchanged. Validity of zero-value coupons is unspecified. |
| FR09-AI-026 | POST `/api/apply-coupon` | Percent value/100 | Valid JWT; active percent coupon value 100 | `total_amount:500000` | 200* | `discount_amount:500000`, `final_amount:0`. |
| FR09-AI-027 | POST `/api/apply-coupon` | Percent value/out of range | Valid JWT; percent coupon value 101 exists | Qualifying total | 400* | Reject invalid coupon configuration; must not return negative final amount. Range validation is unspecified. |
| FR09-AI-028 | POST `/api/apply-coupon` | Fixed value/greater than total | Valid JWT; fixed discount 600000, total 500000 | Qualifying request | 400* | Assumption: reject unsafe configuration/result; final amount must not become negative. Spec formula otherwise implies `-100000`. |
| FR09-AI-029 | POST `/api/apply-coupon` | Coupon type/unsupported | Valid JWT; active coupon has `type:"bonus"` | Qualifying request | 400* | Unsupported type rejected; it must not be treated as fixed. |
| FR09-AI-030 | POST `/api/apply-coupon` | SEC-02/no authentication | Coupon valid; body claims existing user | No Authorization header; `user_id:1` | 401* | `{error:string}`; body `user_id` cannot replace JWT authentication. |
| FR09-AI-031 | POST `/api/apply-coupon` | SEC-02/invalid JWT | Valid coupon | `Authorization: Bearer invalid`; valid body | 401* | `{error:string}`; no coupon details or usage information leaked. |
| FR09-AI-032 | POST `/api/apply-coupon` | User ID type | Valid JWT for user 1 | `user_id:"abc"` | 400* | Invalid supplied type rejected, or ignored in favor of JWT subject; it must never select another usage record. |
| FR09-AI-033 | POST `/api/apply-coupon` | IDOR/user spoofing | JWT belongs to user 1; user 1 at limit; user 2 unused | Body sends `user_id:2` | 400/403* | Must use JWT user 1 and deny application; changing `user_id` cannot bypass limit. |
| FR09-AI-034 | POST `/api/apply-coupon` | Usage state transition | Valid JWT; coupon max 2 | Apply at usage 1, record successful checkout, then apply again at usage 2 | 200 then 400* | At `max-1`, apply succeeds; after usage reaches max, `{error:string}` and no discount. Merely previewing before checkout should not consume a use. |
| FR09-AI-035 | POST `/api/apply-coupon` | Exact response schema | Any valid percent request | Apply known coupon to known total | 200 | JSON object must contain numeric `discount_amount` and `final_amount`; values obey formula and `final_amount=total-discount`. The API spec does not define whether extra keys are allowed, so an exact whole-object key set cannot be asserted without clarification. |

`*` = assumed because the API specification does not explicitly define that status, validation rule, or complete error schema.

Implementation observations for human audit: the current handler has likely defects against these expectations—it does not authenticate `/api/apply-coupon`, trusts optional body `user_id`, checks `total_amount > min_order_amount` instead of `>=`, and computes percent discount as `floor(total × (1 - discount_value))` rather than `floor(total × discount_value / 100)`.
