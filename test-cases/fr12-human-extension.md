# FR-12 Human Extension

These five cases are my additions after the AI audit.

| ID | Area | Preconditions and steps | Expected result | Why the AI missed it |
|---|---|---|---|---|
| H-FR12-36 | Known-secret token forgery | Read the published server code, sign a JWT with the hard-coded secret and `role:"admin"`, then request `/api/admin/users`. | Return 403; production secrets must not be in source and attacker-created tokens must fail. | The AI tested wrong signatures and `alg:none`, but it did not connect source-code secret disclosure to a correctly signed forged token. |
| H-FR12-37 | Deleted-user token | Login as a disposable user, delete that user as admin, then reuse the old user JWT on a protected endpoint. | Return 401/403 because the token subject no longer exists. | The AI treated signature validity as enough and did not verify account state after token issue. |
| H-FR12-38 | Stale admin role | Issue an admin JWT, change that account's stored role to user, then reuse the old JWT on `/api/admin/users`. | Return 403; current server-side role must be checked for high-risk admin actions. | The AI varied role claims at issue time but missed role revocation after issue. |
| H-FR12-39 | Admin self-delete | Login as admin and call `DELETE /api/admin/users/{own-id}`. Then reuse the token. | Return 400/403 and keep the current admin account, as required by FR-19. | The AI tested a normal user deleting self, not the special authorized-admin self-delete rule. |
| H-FR12-40 | Admin-read consistency | Login as a normal user and call `GET /api/coupons`, which the API specification labels as admin-only. | Return 403 and disclose no coupon-management data. | The AI sampled several `/api/admin/*` mutations but missed this admin route outside the `/api/admin/` path prefix. |

These additions focus on authorization revocation, secret management, and protected routes that do not share the admin URL prefix.

