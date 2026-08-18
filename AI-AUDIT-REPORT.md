# AI Audit Report

I use AI tools for the following tasks.

This audit contains only my interactions with the helper AIs used to generate test drafts. It does not include any conversation between the repository assistant and the homework owner.

| Interaction | AI tool | Date and time | Task | Exact prompt and output |
|---|---|---|---|---|
| 1 | Codex helper AI (Hegel) | 2026-08-18 12:25:47 +07 | Generate 35 FR-03 cases | [FR-03 exact interaction log](test-cases/fr03-ai-generated.md) |
| 2 | Codex helper AI (Banach) | 2026-08-18 12:25:59 +07 | Generate 35 FR-09 cases | [FR-09 exact interaction log](test-cases/fr09-ai-generated.md) |
| 3 | Codex helper AI (Raman) | 2026-08-18 12:26:09 +07 | Generate 35 FR-12 cases | [FR-12 exact interaction log](test-cases/fr12-ai-generated.md) |

Each linked log includes the AI tool name, date and time, my full prompt, and the full AI output. These files are the unchanged conversation records. I reviewed their outputs in the separate human-audit files and did not treat them as final answers.

## Non-AI Tools

- Postman collection format for request organization, variables, pre-request scripts, and test scripts.
- Newman 6.2.2 for CLI execution and HTML/JSON reports.
- GitHub Actions for CI/CD execution.

## Human Responsibility

I checked all 105 generated cases. I marked 89 as valid, 3 as invalid, and 13 as incomplete. I corrected the invalid or incomplete oracles and added 15 human cases. The final decisions, execution results, and bug reports are my responsibility.
