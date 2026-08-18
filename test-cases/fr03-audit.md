# FR-03 Human Audit

I reviewed the 35 cases against FR-01, FR-03, SEC-01, SEC-05, SEC-07, the API specification, and the SUT code. `VALID` means the test idea and expected requirement are correct. `INVALID` means I changed the expected result. `INCOMPLETE` means I kept the idea but made the oracle more precise.

| ID | Label | Human reason | Correction for final test |
|---|---|---|---|
| AI-FR03-01 | VALID | FR-03 and SEC-07 require a six-digit OTP and the response schema is given. | None. |
| AI-FR03-02 | INCOMPLETE | The spec does not define the response for an unknown email, and a clear 404 reveals account existence. | Record the observed 404 as a security bug; the secure oracle is the same generic response as a known email. |
| AI-FR03-03 | VALID | `email` is required for the first state transition. | None. |
| AI-FR03-04 | VALID | Empty email is outside the valid email partition. | None. |
| AI-FR03-05 | VALID | Whitespace-only email is equivalent to empty input. | None. |
| AI-FR03-06 | VALID | FR-01 gives a valid email format rule. | None. |
| AI-FR03-07 | VALID | Null is not a valid email string. | None. |
| AI-FR03-08 | VALID | A number is not a valid email string. | None. |
| AI-FR03-09 | VALID | An object must not be treated as a database operator. | None. |
| AI-FR03-10 | VALID | The 254-character email boundary is a useful robustness partition. | None. |
| AI-FR03-11 | VALID | It directly checks SEC-05 parameterized queries. | None. |
| AI-FR03-12 | VALID | It checks safe handling of hostile user input under SEC-04. | None. |
| AI-FR03-13 | INVALID | The requirements never say email matching is case-insensitive, and SQLite equality here is case-sensitive. | Expect 404 for the uppercase variant and document case sensitivity as an assumption. |
| AI-FR03-14 | VALID | A newer OTP must invalidate the previous OTP. | None. |
| AI-FR03-15 | INCOMPLETE | One hundred random samples cannot prove entropy and can fail by chance. | Check six-digit format, range, and multiple distinct values; also review the generation code for at least 900,000 possibilities. |
| AI-FR03-16 | VALID | It covers the main reset transition and exact success schema. | None. |
| AI-FR03-17 | VALID | FR-03 says an OTP cannot be used for another email. | None. |
| AI-FR03-18 | VALID | An incorrect OTP must not change the password. | None. |
| AI-FR03-19 | VALID | Email is required to bind the reset to an account. | None. |
| AI-FR03-20 | VALID | The OTP is required for reset. | None. |
| AI-FR03-21 | INCOMPLETE | The rejection is right, but the spec does not state whether an invalid request consumes an OTP. | Assert 400 and then retry with a valid password to prove the OTP was not consumed. |
| AI-FR03-22 | VALID | Malformed email is outside the valid partition. | None. |
| AI-FR03-23 | VALID | Null email must not reach a successful reset. | None. |
| AI-FR03-24 | VALID | Empty OTP is invalid. | None. |
| AI-FR03-25 | VALID | SEC-07 requires at least six digits. | None. |
| AI-FR03-26 | VALID | FR-03 defines a six-digit OTP, so seven digits are invalid. | None. |
| AI-FR03-27 | VALID | The API returns the OTP as a string, so numeric coercion should not be accepted. | None. |
| AI-FR03-28 | VALID | FR-01 requires at least eight password characters. | None. |
| AI-FR03-29 | VALID | FR-01 requires an uppercase character. | None. |
| AI-FR03-30 | VALID | FR-01 requires a lowercase character. | None. |
| AI-FR03-31 | VALID | FR-01 requires a digit. | None. |
| AI-FR03-32 | VALID | FR-01 requires a special character. | None. |
| AI-FR03-33 | VALID | Null is outside the password domain and must not crash the server. | None. |
| AI-FR03-34 | INCOMPLETE | SEC-07 requires expiry but no lifetime is configured in the specification. | Use the project-configured lifetime when available; also inspect storage for an issue timestamp. Missing expiry data is a bug. |
| AI-FR03-35 | VALID | It checks both one-time use and SEC-01 password hashing. | None. |

## Audit result

- Valid: 30
- Invalid: 1
- Incomplete: 4
- Total reviewed: 35

