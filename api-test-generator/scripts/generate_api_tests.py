#!/usr/bin/env python3

import csv
import re
import sys

spec_path = sys.argv[1]
output_path = sys.argv[2]
endpoint_filter = sys.argv[3] if len(sys.argv) > 3 else ""

text = open(spec_path, encoding="utf-8").read()
endpoints = re.findall(r"(?:Endpoint|(?:Thêm sản phẩm|Cập nhật|Xóa)):\*?\*? `?(GET|POST|PUT|PATCH|DELETE) ([^`\s]+)", text)
if not endpoints:
    endpoints = re.findall(r"`(GET|POST|PUT|PATCH|DELETE) ([^`\s]+)`", text)

templates = [
    ("positive", "valid request", "valid values", "success status and documented schema"),
    ("domain", "missing required input", "omit one required value", "4xx error; no state change"),
    ("domain", "empty required input", "send an empty value", "4xx error; no state change"),
    ("domain", "wrong input type", "replace one value with the wrong JSON type", "4xx error; no server crash"),
    ("boundary", "oversized input", "send a very long string", "4xx error or documented limit handling"),
    ("security", "SQL injection input", "send ' OR 1=1 -- in a string field", "request is rejected or treated as plain text"),
    ("security", "missing authorization", "omit Authorization header", "401 for protected endpoint"),
    ("security", "wrong role", "use a normal-user token for an admin action", "403 for admin endpoint"),
    ("schema", "response schema", "send a valid request", "field names and types exactly match the specification"),
    ("header", "student identifier", "send X-Student-Id: 23127081", "request is processed with the required header"),
]

rows = []
for method, endpoint in endpoints:
    if endpoint_filter and endpoint_filter not in endpoint:
        continue
    for category, title, test_input, expected in templates:
        rows.append({
            "id": f"GEN-{len(rows) + 1:03d}",
            "method": method,
            "endpoint": endpoint,
            "category": category,
            "title": title,
            "input": test_input,
            "expected": expected,
            "review": "INCOMPLETE",
        })

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"generated {len(rows)} draft cases in {output_path}")
