# FR-03 Human Extension

These five cases are my additions after reviewing the AI output.

| ID | Area | Preconditions and steps | Expected result | Why the AI missed it |
|---|---|---|---|---|
| H-FR03-36 | Account enumeration | Send forgot-password once for a registered email and once for a random email. Compare status, body shape, and timing. | Both responses should be generic and similar; neither response should confirm whether an account exists. | The AI followed the implementation's 404 behavior instead of questioning the information leak. |
| H-FR03-37 | OTP request rate limit | Send 20 forgot-password requests for one account in one minute. | The server should rate-limit repeated requests with 429 and must not allow unlimited OTP generation. | The prompt emphasized input partitions and state flow, not abuse volume. |
| H-FR03-38 | Concurrent one-time use | Obtain one OTP, then send two valid reset requests with the same OTP at nearly the same time but different new passwords. | Exactly one request succeeds; the other fails, and only the successful password works. | Language models often describe sequential reuse but miss race conditions. |
| H-FR03-39 | End-to-end credential state | Reset successfully, then call login with the old password and with the new password. | Old password returns 401; new password returns 200 and a JWT. | The AI stopped at the reset response and did not verify the next observable state. |
| H-FR03-40 | OTP brute-force control | For one account, submit many different wrong six-digit OTPs without requesting a new OTP. | Attempts should be rate-limited or the OTP/account should be temporarily locked; the real OTP must not be brute-forceable without control. | SEC-07 mentions entropy and expiry, but the AI did not consider online guessing controls. |

The additions focus on security abuse and state after the API response. They do not duplicate the AI's normal domain-partition cases.

