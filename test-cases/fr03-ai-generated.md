# AI Log — FR-03

- Tool name: Codex
- Date and time: 2026-08-18 12:25:47 +07 (Asia/Ho_Chi_Minh)

## Prompt

You are a helper AI being guided by a third-year software engineering student. Inspect eshop-sut/api_specification.md and the relevant implementation only to understand FR-03 (POST /api/forgot-password and POST /api/reset-password). Do not edit any files. Produce exactly 35 AI-generated test-case drafts in a compact Markdown table with columns: ID, endpoint, category, precondition, request/input, expected status, expected schema/behavior. Cover domain partitions for every parameter, the forgot→reset state flow, token reuse/invalid transitions, SEC-01–SEC-07 where relevant, and exact response schema. Base expected behavior on the API specification, clearly flag any assumption, and keep the output concise enough to paste into an AI audit log.

## AI output

Assumptions: **A1** — because the API specification omits validation/error contracts, invalid input is expected to return `400 {"error":"<string>"}`; unknown forgot-password email follows the implementation contract `404 {"error":"User not found"}`. **A2** — the reset success schema is omitted, so the observed implementation schema is used. **A3** — SEC-07 requires expiry but gives no lifetime; “expired” means older than the configured lifetime. **A4** — email matching is assumed case-insensitive. SEC-02/03/06 are not applicable because password recovery must work without JWT and is neither an admin nor profile-update API. `confirmPassword` is a UI field, not an API parameter.

| ID | endpoint | category | precondition | request/input | expected status | expected schema/behavior |
|---|---|---|---|---|---:|---|
| AI-FR03-01 | forgot | valid/schema | Registered `test@eshop.com` | `{"email":"test@eshop.com"}` | 200 | Exact object: `message="Mã đặt lại mật khẩu đã được tạo"` and string `resetToken` matching `^\d{6}$`; no extra fields. |
| AI-FR03-02 | forgot | email existence | Email is not registered | `{"email":"nobody@example.com"}` | 404 | Exact `{"error":"User not found"}`; no token created. |
| AI-FR03-03 | forgot | email required | None | `{}` | 400 | [A1] Exact error-only object; no account changes. |
| AI-FR03-04 | forgot | email empty | None | `{"email":""}` | 400 | [A1] Reject empty string; exact error-only object. |
| AI-FR03-05 | forgot | email whitespace | Registered email exists | `{"email":"   "}` | 400 | [A1] Reject whitespace-only value; no token created. |
| AI-FR03-06 | forgot | email format | None | `{"email":"test-at-eshop"}` | 400 | [A1] Reject malformed email; exact error-only object. |
| AI-FR03-07 | forgot | email type | None | `{"email":null}` | 400 | [A1] Reject null; no server error. |
| AI-FR03-08 | forgot | email type | None | `{"email":12345}` | 400 | [A1] Reject non-string number. |
| AI-FR03-09 | forgot | email type | None | `{"email":{"$ne":null}}` | 400 | [A1] Reject object input; no query-operator interpretation. |
| AI-FR03-10 | forgot | email boundary | None | Email string longer than 254 characters | 400 | [A1] Reject oversized email cleanly; no `500`. |
| AI-FR03-11 | forgot | SEC-05 SQL injection | A registered user exists | `{"email":"' OR 1=1 --"}` | 400 | [A1] Input is data, never SQL; no token for any user and exact error-only response. |
| AI-FR03-12 | forgot | SEC-04 injection | None | `{"email":"<script>alert(1)</script>@x.com"}` | 400 | [A1] Reject and never reflect executable markup in response. |
| AI-FR03-13 | forgot | email case | Registered `test@eshop.com` | `{"email":"TEST@ESHOP.COM"}` | 200 | [A4] Same account is found; exact success schema and six-digit token. |
| AI-FR03-14 | forgot→reset | token replacement | One valid OTP already exists | Call forgot again, then reset once with old OTP and once with new OTP | 400, then 200 | SEC-07: new issue invalidates old OTP; new OTP resets password with [A2] exact success schema. |
| AI-FR03-15 | forgot | SEC-07 entropy | Registered account; isolated repeatable test | Request 100 OTPs | 200 each | Every response has exact schema; each OTP is exactly six random digits and not an obvious fixed/sequential value. |
| AI-FR03-16 | reset | valid/schema | Fresh OTP belongs to email | `{"email":"test@eshop.com","resetToken":"123456","newPassword":"Aa1!aaaa"}` using actual OTP | 200 | [A2] Exact `{"message":"Password reset successfully"}`; no token/password fields. |
| AI-FR03-17 | reset | state/email binding | Fresh OTP belongs to user A; user B exists | User B email with user A OTP and valid password | 400 | Exact [A1] error-only object; neither password changes. |
| AI-FR03-18 | reset | token invalid | Account has a different active OTP | Correct email, `"000000"`, valid password | 400 | Exact [A1] error-only object; password unchanged. |
| AI-FR03-19 | reset | email required | Fresh OTP exists | Omit `email` | 400 | [A1] Reject; OTP remains unused. |
| AI-FR03-20 | reset | token required | Account exists | Omit `resetToken` | 400 | [A1] Reject; password unchanged. |
| AI-FR03-21 | reset | password required | Fresh OTP exists | Omit `newPassword` | 400 | [A1] Reject; OTP remains usable for a corrected request. |
| AI-FR03-22 | reset | email format | Fresh OTP exists | `"email":"bad-email"` with valid OTP/password | 400 | [A1] Reject malformed email; no state change. |
| AI-FR03-23 | reset | email type | Fresh OTP exists | `"email":null` | 400 | [A1] Reject null without `500`; OTP not consumed. |
| AI-FR03-24 | reset | token empty | Fresh OTP exists | `"resetToken":""` | 400 | [A1] Reject empty token; password unchanged. |
| AI-FR03-25 | reset | token lower boundary | Fresh OTP exists | `"resetToken":"12345"` | 400 | SEC-07: reject fewer than six digits. |
| AI-FR03-26 | reset | token upper boundary | Fresh OTP exists | `"resetToken":"1234567"` | 400 | FR-03: reject more than six digits. |
| AI-FR03-27 | reset | token type | Fresh OTP value is `123456` | `"resetToken":123456` as JSON number | 400 | [A1] Reject non-string type; no coercion and no password change. |
| AI-FR03-28 | reset | password length | Fresh OTP exists | `"newPassword":"Aa1!aaa"` (7 chars) | 400 | Reject below minimum 8; OTP remains usable. |
| AI-FR03-29 | reset | password uppercase | Fresh OTP exists | `"newPassword":"aa1!aaaa"` | 400 | Reject password with no uppercase letter. |
| AI-FR03-30 | reset | password lowercase | Fresh OTP exists | `"newPassword":"AA1!AAAA"` | 400 | Reject password with no lowercase letter. |
| AI-FR03-31 | reset | password digit | Fresh OTP exists | `"newPassword":"Aaa!aaaa"` | 400 | Reject password with no digit. |
| AI-FR03-32 | reset | password special | Fresh OTP exists | `"newPassword":"Aaa1aaaa"` | 400 | Reject password lacking one of `@ $ ! % * ? &`. |
| AI-FR03-33 | reset | password type | Fresh OTP exists | `"newPassword":null` | 400 | [A1] Reject non-string password without `500`; OTP not consumed. |
| AI-FR03-34 | forgot→reset | SEC-07 expiry | OTP is older than configured lifetime [A3] | Correct email, expired OTP, valid password | 400 | Expired OTP is rejected and password stays unchanged. |
| AI-FR03-35 | forgot→reset | SEC-01/SEC-07 reuse | One reset has succeeded | Reuse same email/OTP with another valid password; inspect test DB | 400 | Used OTP stays invalid; second password is not applied; first new password is stored as a one-way hash, never plaintext. |
