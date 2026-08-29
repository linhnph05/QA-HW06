# AI Log — FR-12

- Tool: Codex
- Date/time (Asia/Ho_Chi_Minh): 2026-08-18 12:26:09 +07

## Original prompt from the primary agent

> You are a helper AI being guided by a third-year software engineering student. Inspect eshop-sut/api_specification.md and the relevant implementation only to understand FR-12 access control. Use GET /api/admin/users as the representative selected API, with related admin endpoints only when needed to test authorization consistency. Do not edit any files. Produce exactly 35 AI-generated test-case drafts in a compact Markdown table with columns: ID, endpoint, category, precondition, request/input, expected status, expected schema/behavior. Cover Authorization header/token partitions, anonymous/user/admin roles, role escalation and IDOR, SEC-01–SEC-07 where relevant, and exact response schema. Base expected behavior on the API specification, clearly flag any assumption, and keep the output concise enough to paste into an AI audit log.

## Exact final output

Assumptions used because the API specification does not define response bodies in detail:

- `U` is the exact successful user object inferred from the selected route: `{id:number,name:string|null,email:string|null,role:string|null,login_attempts:number,locked_until:string|null,shipping_address:string|null}`. No extra keys are allowed.
- Missing/malformed credentials return `{"error":"Unauthorized"}`; invalid JWT or insufficient role returns `{"error":"Forbidden"}`.
- `Bearer` is case-insensitive under normal HTTP authentication rules. A deleted/nonexistent resource returns 404 where the specification is silent.
- SEC-07’s OTP entropy/lifetime rules are outside FR-12; only reset-token disclosure through the user-list response is relevant here.

| ID | endpoint | category | precondition | request/input | expected status | expected schema/behavior |
|---|---|---|---|---|---:|---|
| FR12-AI-01 | GET `/api/admin/users` | Positive / FR-12 | At least one user; valid admin JWT | `Authorization: Bearer <admin>` | 200 | JSON array of `U`; every stored user appears once. |
| FR12-AI-02 | GET `/api/admin/users` | Empty boundary | No users; valid admin JWT | Normal request | 200 | Exact body `[]`. |
| FR12-AI-03 | GET `/api/admin/users` | SEC-01, SEC-07 / disclosure | Valid admin JWT | Normal request | 200 | Each item has exactly `U`; must omit `password`, `reset_token`, `phone`, and other secret/internal fields. |
| FR12-AI-04 | GET `/api/admin/users` | SEC-04 / stored XSS | A user name/address contains `<script>alert(1)</script>`; admin JWT | Normal request | 200 | `application/json`; value is returned only as JSON text and never rendered/executed by the API response. |
| FR12-AI-05 | GET `/api/admin/users` | Data boundary | User contains Vietnamese/Unicode and null optional fields | Normal admin request | 200 | Valid JSON `U`; Unicode preserved; `locked_until`/`shipping_address` remain JSON null where unset. |
| FR12-AI-06 | GET `/api/admin/users` | SEC-02 / anonymous | None | No `Authorization` header | 401 | Exact `{"error":"Unauthorized"}`; no user data. |
| FR12-AI-07 | GET `/api/admin/users` | SEC-02 / empty header | None | `Authorization: ""` | 401 | Exact unauthorized error; no user data. |
| FR12-AI-08 | GET `/api/admin/users` | SEC-02 / missing credential | None | `Authorization: Bearer` | 401 | Exact unauthorized error; no user data. |
| FR12-AI-09 | GET `/api/admin/users` | SEC-02 / missing scheme | Valid admin token exists | `Authorization: <admin-token>` | 401 | Exact unauthorized error; raw token is not accepted. |
| FR12-AI-10 | GET `/api/admin/users` | SEC-02 / wrong scheme | Valid admin token exists | `Authorization: Basic <admin-token>` | 401 | Exact unauthorized error; JWT must not be accepted under `Basic`. |
| FR12-AI-11 | GET `/api/admin/users` | Header syntax | Valid admin token exists | `Authorization: Bearer  <admin-token>` | 401 | Exact unauthorized error under the specified single-space syntax. |
| FR12-AI-12 | GET `/api/admin/users` | Header compatibility | Valid admin JWT | `Authorization: bearer <admin-token>` | 200 | JSON array of `U`; auth scheme comparison is case-insensitive. |
| FR12-AI-13 | GET `/api/admin/users` | SEC-02 / malformed JWT | None | `Bearer abc.def` | 403 | Exact `{"error":"Forbidden"}`; no data. |
| FR12-AI-14 | GET `/api/admin/users` | SEC-02 / bad signature | JWT signed with another secret | `Bearer <wrong-signature-token>` | 403 | Exact forbidden error; no data. |
| FR12-AI-15 | GET `/api/admin/users` | SEC-02 / tampering | Start with valid user JWT, edit payload without resigning | Change payload role to `admin` | 403 | Exact forbidden error; signature validation blocks tampering. |
| FR12-AI-16 | GET `/api/admin/users` | SEC-02 / expiry | Expired admin JWT | `Bearer <expired-admin-token>` | 403 | Exact forbidden error; no data. |
| FR12-AI-17 | GET `/api/admin/users` | SEC-02 / algorithm attack | Crafted unsigned JWT | JWT with `alg:"none"` and `role:"admin"` | 403 | Exact forbidden error; unsigned token rejected. |
| FR12-AI-18 | GET `/api/admin/users` | SEC-03 / user role | Valid JWT with `role:"user"` | `Bearer <user-token>` | 403 | Exact forbidden error; no user list. |
| FR12-AI-19 | GET `/api/admin/users` | SEC-03 / admin role | Valid JWT with `role:"admin"` | `Bearer <admin-token>` | 200 | JSON array of exact `U`. |
| FR12-AI-20 | GET `/api/admin/users` | SEC-03 / missing claim | Validly signed JWT has `id` but no `role` | `Bearer <no-role-token>` | 403 | Exact forbidden error. |
| FR12-AI-21 | GET `/api/admin/users` | SEC-03 / case boundary | Valid JWT with `role:"ADMIN"` | `Bearer <uppercase-role-token>` | 403 | Exact forbidden error; only exact role `admin` is authorized. |
| FR12-AI-22 | GET `/api/admin/users` | SEC-03 / null claim | Valid JWT with `role:null` | `Bearer <null-role-token>` | 403 | Exact forbidden error. |
| FR12-AI-23 | PUT `/api/users/me` then GET `/api/admin/users` | SEC-06 / role escalation | Logged-in normal user | PUT body includes `{"name":"U","shipping_address":"A","phone":"1","role":"admin"}`, then obtain fresh JWT and GET | 403 on GET | Profile may update allowed fields, but stored/token role remains `user`; admin list is not disclosed. |
| FR12-AI-24 | POST `/api/register` then GET `/api/admin/users` | Role injection | New email | Register with extra `"role":"admin"`, log in, then GET with issued JWT | 403 on GET | Extra role is ignored; account/token role is `user`; exact forbidden error. |
| FR12-AI-25 | DELETE `/api/admin/users/:id` | IDOR / own record | Normal user JWT; own ID exists | DELETE own ID | 403 | Exact forbidden error; own account remains unchanged. |
| FR12-AI-26 | DELETE `/api/admin/users/:id` | IDOR / other record | Normal user JWT; another user exists | DELETE another user’s ID | 403 | Exact forbidden error; target remains unchanged. |
| FR12-AI-27 | DELETE `/api/admin/users/:id` | Positive authorization | Admin JWT; disposable target exists | DELETE target ID | 200 | Exact `{"message":"User deleted"}`; only target is removed. |
| FR12-AI-28 | DELETE `/api/admin/users/:id` | SEC-05 / injection | Admin JWT; multiple users exist | ID path value `1%20OR%201=1` | 404 | No user is deleted; ID is handled as one parameter, never concatenated SQL. |
| FR12-AI-29 | DELETE `/api/admin/users/:id` | SEC-02 / anonymous mutation | Target exists | No Authorization header | 401 | Exact unauthorized error; target remains unchanged. |
| FR12-AI-30 | GET `/api/admin/orders` | SEC-03 / consistency | Valid normal-user JWT | Normal request | 403 | Exact forbidden error; no order data. |
| FR12-AI-31 | PUT `/api/admin/orders/:id/status` | SEC-03 / mutation consistency | Normal-user JWT; pending order exists | `{"status":"confirmed"}` | 403 | Exact forbidden error; order status remains `pending`. |
| FR12-AI-32 | POST `/api/admin/coupons` | SEC-03 / mutation consistency | Normal-user JWT | Valid coupon JSON | 403 | Exact forbidden error; coupon is not created. |
| FR12-AI-33 | DELETE `/api/admin/coupons/:id` | SEC-03 / IDOR consistency | Normal-user JWT; coupon exists | DELETE coupon ID | 403 | Exact forbidden error; coupon remains unchanged. |
| FR12-AI-34 | POST `/api/admin/import-products` | SEC-03 / bulk mutation | Normal-user JWT | `{"products":[{"name":"P","price":1000,"category_id":1}]}` | 403 | Exact forbidden error; zero products inserted. |
| FR12-AI-35 | POST `/api/products` | FR-12 / protected data API | Normal-user JWT | Valid product JSON | 403 | Exact forbidden error; product is not created because data-changing product APIs require admin role. |
