# Performance and Recovery Testing (Area 3, performance)

Carried out by Muhammad Wasay Tariq (24I-3071) as part of the Area 3 work taken over by team agreement. Brief §5: one operation with response-time and failure limits set **before** testing, Grafana k6 OSS with 1 and at least 5 concurrent users, each run twice for at least 60 s at the target user count on the same build, machine and data; plus one automated failure-and-recovery test for a state-changing operation.

## 1. Operation under test

**`GET /api/leave/available-leave/`**: the read of the shared record `AvailableLeave` (leave balance) for the logged-in employee.

Why this operation: it is the one call both workflows depend on. W2 reads the balance before every leave request (BR-01), W1 and W2 read it back after every approval or rejection, and the "My Leave" screen loads it each time it opens. It is also safe to repeat under load: it changes no data, so every run starts from and ends with the same database state.

## 2. Limits (set before the first run)

| Limit | Target | Why it suits this operation |
|---|---|---|
| Response time | **p95 ≤ 500 ms** at each workload | The balance is shown as the user opens the leave screen and right before they submit a request. Half a second keeps the screen feeling immediate (well inside the ~1 s limit at which users lose their flow of thought), and p95 rather than the average makes sure 19 of 20 users get that, not just the typical one. Same target as exit criterion **EC-3** in `RISK_REGISTER.md`. |
| Unexpected failures | **< 1%** of requests | Any non-200 response, or a 200 without the employee's balance row, counts as unexpected. A balance read has no legitimate reason to fail, so 1% is a tolerance for transient errors, not a budget for broken behaviour. |

## 3. Workload and method

| Item | Value |
|---|---|
| Tool | Grafana k6 OSS **v2.4.0** (Windows amd64, SHA-256 verified against the GitHub release digest) |
| Script | [`tests/team/perf/available_leave.js`](../../../tests/team/perf/available_leave.js) |
| Workloads | 1 virtual user, and 5 concurrent virtual users (`constant-vus`) |
| Per run | 10 s warm-up at the target user count, then **60 s measured steady state**. Only steady-state requests (tag `phase:steady`) count towards the limits |
| Pacing | Each user reads the balance once per second (`sleep(1)` think time). This is a realistic pace for a person in the leave screens, and it keeps 5 users (about 300 requests/min) under Horilla's own per-user API throttle of 600 requests/min (`horilla/settings/base.py`), so the test measures the application rather than the throttle |
| Authentication | JWT from `POST /api/auth/login/` in `setup()` (synthetic seed account `team_employee`) |
| Checks | HTTP 200 **and** a non-empty `results` list containing the balance row |
| Repetitions | Each workload run twice, back to back, on the same build, machine and data |

### Environment (same for all four runs)

From [`evidence/perf/environment.txt`](../evidence/perf/environment.txt):

| Item | Value |
|---|---|
| Build | `sqe-team` @ `2ceca1ee7` |
| Machine | Intel Core i7-1265U (10 cores / 12 threads), 31.4 GB RAM, Windows 11 Pro 10.0.26300 |
| Server | `manage.py runserver 127.0.0.1:8000 --noreload` (Django development server, threaded), Python 3.12.10, Django 5.2.19, `DEBUG=True` |
| Data | SQLite `TestDB.sqlite3` restored from the seeded snapshot (`scripts/team/reset.ps1`) before the runs; the operation is read-only, so all runs saw identical data |
| Client | k6 on the same machine (localhost), so there is no network latency |

## 4. Results

Raw output per run: `k6-<run>-console.txt` (k6 output), `k6-<run>-summary.json` (full k6 summary), `k6-<run>-steady.json` (steady-state figures) in [`docs/team/evidence/perf/`](../evidence/perf/).

| Run | Users | **p95 (ms)** | Median (ms) | Max (ms) | Requests in 60 s | **Requests/s** | **Unexpected failures** | p95 ≤ 500 ms | Failures < 1% |
|---|---|---|---|---|---|---|---|---|---|
| 1 VU, run 1 | 1 | **15.9** | 13.0 | 21.1 | 60 | **1.00** | **0.0%** | ✓ | ✓ |
| 1 VU, run 2 | 1 | **16.0** | 12.9 | 20.9 | 60 | **1.00** | **0.0%** | ✓ | ✓ |
| 5 VU, run 1 | 5 | **28.2** | 15.4 | 168.1 | 296 | **4.93** | **0.0%** | ✓ | ✓ |
| 5 VU, run 2 | 5 | **39.1** | 18.7 | 68.9 | 295 | **4.92** | **0.0%** | ✓ | ✓ |

k6 reported all thresholds passed (exit code 0) for every run.

## 5. Interpretation against the limits

- **Both limits are met in all four runs, with a large margin:** the worst p95 (39.1 ms) is under 8% of the 500 ms limit, and no request failed.
- **Repeatability:** the two 1-user runs are almost identical (15.9 vs 16.0 ms). The two 5-user runs differ more (28.2 vs 39.1 ms) because, with five users sharing one development server, small timing differences decide how often requests queue behind each other; both stay far below the limit.
- **Effect of concurrency:** going from 1 to 5 users raises the median only slightly (13 → 15–19 ms) but the p95 by about 2× (16 → 28–39 ms), and one 5-user request took 168 ms. That is the start of queuing in the single-process development server. It is still not close to a user-visible delay.
- **Throughput** grows linearly with users (1.00 → 4.93 requests/s), which is the expected result for a paced (closed) workload in which nobody waits on the server. It confirms that throughput was limited by the users' think time, not by the server.
- **EC-3 (release criterion): met.** Actual p95 at 5 users = 39.1 ms (worst run) vs target ≤ 500 ms; actual unexpected failures 0.0% vs target < 1%.

**Limitations:** the server is Django's development server with `DEBUG=True` on SQLite, and client and server share a machine. Production (gunicorn + PostgreSQL, `DEBUG=False`) is likely faster per request but would add network latency. The results show the application logic for this operation is far from the limit at the planned load; they are not a capacity test beyond 5 users, which `TEST_PLAN.md` places out of scope.

## 6. Failure-and-recovery test

**Script:** [`tests/team/recovery/test_allocation_approve_recovery.py`](../../../tests/team/recovery/test_allocation_approve_recovery.py), run by the CI gate's unit job.

**Operation:** `PUT /api/leave/allocation-approve/<id>/` (W1 approval), called through DRF's `APIClient` so it goes through Django's full request handling. In `LeaveAllocationApproveAPIView` it performs two writes in sequence: **(1)** credit the balance (`AvailableLeave.save`), **(2)** mark the request approved (`LeaveAllocationRequest.save`).

**Test double:** the dependency is the database. `mock.patch.object(Model, "save", …)` makes the chosen write raise `OperationalError("database is unavailable")`, the error a dropped or locked database connection gives. Removing the patch restores the dependency.

**Steps checked in each case:** (1) the database fails during the approval → the API answers HTTP 500; (2) persisted state after the failure (status, number of balance rows, balance); (3) the database is restored and the client retries; (4) final state: approved, credited **exactly once**, still one balance row.

| Case | After the failure (expected → observed) | After the retry (expected → observed) | Result |
|---|---|---|---|
| Database fails at the **1st write** (balance credit) | status `requested`, 1 row, balance 5 → **same** | `approved`, 1 row, balance 8 → **same** | **pass**: nothing half-applied, recovery clean |
| Database fails at the **2nd write** (status) | status `requested`, 1 row, balance **5** → observed **8** | `approved`, 1 row, balance **8** → observed **11** | **fail (REC-01)**: kept as `xfail(strict=True)` |
| Retry after a successful approval | n/a | second call refused (400), balance credited once | **pass**: no duplicate credit |
| Characterisation of REC-01 | balance 8 with status `requested` | retry credits again: balance 11 | passes, documenting the defect |

**Finding REC-01: allocation approval is not atomic (data integrity).**

| | |
|---|---|
| Observed | If the database becomes unavailable after the balance credit but before the status update, the credit stays committed while the request still says "requested". The retry passes the `status == "requested"` check and credits the balance again: a 3-day allocation gives **6** days. |
| Root cause | `LeaveAllocationApproveAPIView.put` performs two dependent writes without `transaction.atomic`, and `ATOMIC_REQUESTS` is not enabled in `horilla/settings/base.py`, so a failure between them cannot roll back the first. |
| Severity | **High**: silent over-crediting of leave entitlement after an infrastructure blip, with no error visible in the data afterwards. |
| Risk | **PR-01** (wrong balance changes), PR-06 (duplicate effect from a retry). |
| Fix | Wrap the approval (balance credit + status change) in `transaction.atomic()` (or enable `ATOMIC_REQUESTS`); also lock the row (`select_for_update`) so two concurrent approvals cannot both pass the status check. The `xfail(strict=True)` test turns into a failure once fixed, forcing the marker to be removed. |

The same two-write pattern exists in the leave approve/reject and allocation reject views; they should be fixed the same way.
