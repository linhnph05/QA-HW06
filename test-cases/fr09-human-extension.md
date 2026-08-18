# FR-09 Human Extension

These five cases are my additions after the AI audit.

| ID | Area | Preconditions and steps | Expected result | Why the AI missed it |
|---|---|---|---|---|
| H-FR09-36 | Omitted identity bypass | User is already at the coupon limit. Send a valid JWT but omit body `user_id`. | The server uses the JWT subject and returns 400 because the real user is at the limit. | The AI tested a spoofed ID but did not test the implementation branch created by a missing ID. |
| H-FR09-37 | Anonymous branch bypass | Send a qualifying coupon request with no JWT and no `user_id`. | Return 401; the request must not enter a less protected calculation branch. | The AI's anonymous test still supplied `user_id`, so it missed the optional-field branch. |
| H-FR09-38 | Concurrent usage race | Coupon has one use left. Run two checkout flows concurrently so both apply and record usage. | At most one checkout receives the discount; usage must not exceed the maximum. | The AI modeled usage transitions sequentially, not as a race. |
| H-FR09-39 | Usage-record integrity | Call `/api/coupon-usage` directly for a nonexistent coupon and for a real coupon without a matching successful checkout. | Reject both requests; usage records must reference a valid coupon and completed checkout. | The prompt focused on apply-coupon and did not make the helper trace the related write endpoint. |
| H-FR09-40 | Numeric overflow | Use `total_amount` above JavaScript's safe integer range with a valid coupon. | Return 400; monetary results must stay exact integers and must not overflow or lose precision. | Typical partition lists include negative and decimal values but often miss numeric precision limits. |

The added tests focus on optional-branch bypasses, atomic usage state, and money precision.

