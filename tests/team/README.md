# Team tests (SE3002 SQE Final Project)

Everything in this folder is written by our team. Upstream tests (e.g. `leave/tests/`) earn no marks and are not counted.

| Folder | Brief section | Tool | Owner area |
|---|---|---|---|
| `unit/` | White-box unit tests, 100% statement + branch on leave business logic, MCC / MC/DC | pytest, pytest-django, coverage.py | Area 1 |
| `generator/` | OpenAPI spec + EP / 3-point BVA data generator | Python script | Area 2 |
| `api/` | API and integration tests using generator output | pytest + requests | Area 2 |
| `e2e/` | Use-case tests, usability + keyboard tests, axe-core | Playwright (Chromium) | Area 3 |
| `security/` | Access-matrix checks (Playwright), ZAP / pip-audit evidence | Playwright, OWASP ZAP, pip-audit | Area 3 |
| `perf/` | Load scripts (1 VU and ≥5 VU) | Grafana k6 OSS | Area 3 |
| `recovery/` | Failure-and-recovery test for a state-changing operation | pytest + test double | Area 3 |

Test-basis IDs (FR-xx, BR-xx) come from [`docs/team/SCOPE.md`](../../docs/team/SCOPE.md). Reference them in each test's docstring so the traceability matrix can be generated.
