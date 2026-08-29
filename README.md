# HW06 - API Testing

Student: Nguyễn Phan Hùng Linh  
Student ID: 23127081  
Repository: https://github.com/linhnph05/QA-HW06

This repository contains my API testing homework for the EShop SUT. I selected FR-03, FR-09, and FR-12, one feature from each required pool.

## Test Summary

| Item | Result |
|---|---:|
| APIs tested | 3 |
| AI-generated cases | 105 |
| Human-added cases | 15 |
| Total executed cases | 120 |
| Passed cases | 54 |
| Failed cases | 66 |
| Passed assertions | 195 |
| Failed assertions | 74 |
| Bugs reported | 9 |

The failed cases are kept because they show real requirement mismatches in the SUT. The full Newman report is in `newman/newman-report.html`.

## Self-Assessment

| No. | Criteria | Grade | Self-Assessed Grade |
|---:|---|---:|---:|
| 1 | FR-03 full pipeline | 30 | 30 |
| 2 | FR-09 full pipeline | 30 | 30 |
| 3 | FR-12 full pipeline | 30 | 30 |
| 4 | Agent Skill | 10 | 10 |
| | **Total** | **100** | **100/100** |

## Main Files

- `REPORT.md`: main homework report
- `AI-AUDIT-REPORT.md`: AI-use declaration with the exact interaction logs embedded
- `reports/ci-cd-report.md`: CI/CD evidence
- `reports/bug-report.md`: nine bug reports and issue links
- `test-cases/test-cases.csv`: all 120 test cases
- `collections/EShop-HW06.postman_collection.json`: strict bug-finding collection
- `newman/newman-report.html`: Newman HTML report
- `api-test-generator/`: reusable Agent Skill

The video is not included, as requested.
