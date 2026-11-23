# Setup, Run, Seed and Reset (reproducible baseline)

Upstream: https://github.com/horilla-opensource/horilla, branch `2.0`, baseline commit `6c15617b8297b7a6775daa6c29aefcc48b1eb29f`.
Verified on Windows 11 (PowerShell) on 2026-11-18.

## Area 2 checkpoint, 23 November 2026

The current execution environment has Python 3.14.7 with pip only in `.venv`.
It does not reproduce the older verified environment described below. Scoped
test dependency installation could not resolve pytest; Django, Requests,
formal OpenAPI validation and Ruff remain unavailable. Docker Desktop startup
was requested, but engine access remained unavailable. See
[Phase B status](reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md) for actual evidence.

The standard-library generator can run independently using commands in
[`tests/team/README.md`](../../tests/team/README.md). Its HTTP consumer requires
the unchanged application requirements and scoped test tools. Use its explicit
Area 2 pytest configuration and disposable database settings; do not reset an
unverified personal/team database to repair this runtime.

## Tool versions (baseline)

| Tool | Version |
|---|---|
| Python | 3.12.10 (Horilla supports 3.12–3.14; 3.12 chosen for tool compatibility) |
| Django / DRF | 5.2.19 / 3.18.3 |
| Database | SQLite (`TestDB.sqlite3` in repo root, git-ignored) |
| Node / npm | 24.16.0 / 11.13.0 (for Playwright later) |
| Java | 25.0.3 (for SonarQube scanner / ZAP later) |
| Docker | 29.7.2 (optional; upstream `docker compose up` also works) |
| Git | 2.54.0 |

## 1. Install (once)

```powershell
git clone https://github.com/horilla-opensource/horilla.git
cd horilla
git checkout 6c15617b8297b7a6775daa6c29aefcc48b1eb29f   # baseline (or our team branch)
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Create `.env` in the repo root (git-ignored) from the template: `Copy-Item docs\team\env.example .env`, then set a new `SECRET_KEY`. Contents:

```ini
DJANGO_SETTINGS_MODULE=horilla.settings
SECRET_KEY=<generate: python -c "import secrets;print(secrets.token_urlsafe(50))">
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
TIME_ZONE=Asia/Karachi
SECURE_SSL_REDIRECT=False
```

Do **not** set `DB_NAME` to a relative path: Django resolves it against the current working directory, so starting the server from another folder silently opens an empty database. Leaving `DATABASE_URL`/`DB_*` unset uses the default absolute path `<repo>/TestDB.sqlite3`.

## 2. Create DB and seed test data

```powershell
powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1
```

Stop the dev server first (Windows locks the SQLite file). The first run deletes `TestDB.sqlite3`, runs `migrate` (slow: 10+ minutes, hundreds of migrations), runs `scripts/team/seed_team.py`, and saves the result to `tests/team/.baseline.sqlite3` (git-ignored). Later runs just copy that snapshot back in seconds. Use `-Rebuild` after pulling new migrations or editing the seed.

The seed creates (idempotently):

| Record | Purpose |
|---|---|
| Company "SQE Test Co" | Owner company for all team data |
| `team_admin` (superuser) | Setup only; not used for rule tests (superuser skips some validation) |
| `team_approver` | Role "Leave Approver": leave approve/reject permissions, reporting manager of `team_employee` |
| `team_employee` | Role "Employee": normal user |
| Leave type "Team Annual Leave" | Paid, limit 10 days, no carry-forward, approval required, no attachment |
| `AvailableLeave(team_employee, Team Annual Leave)` = 0 days | **Starting condition for W1** |

Passwords are synthetic test values documented in `scripts/team/seed_team.py`.

Optional: add Horilla's full synthetic demo dataset first with `reset.ps1 -Rebuild -Demo` (runs `manage.py load_demo_data --flush --no-input`).

## 3. Start the application

```powershell
.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
```

- Browser UI: http://localhost:8000/ (log in with a seed account; "My Leave" is at `/leave/user-request-view/`)
- API docs (DEBUG only): http://localhost:8000/api/swagger/
- API auth: `POST /api/auth/login/` with `{"username","password"}` returns a JWT; send `Authorization: Bearer <access>`.

## 4. Smoke check

With the server running:

```powershell
.\.venv\Scripts\python scripts\team\smoke_api.py
```

Expected: both seed accounts get `200` from `GET /api/leave/available-leave/`; the employee sees "Team Annual Leave" with `available_days: 0.0`.

## 5. Reset between test runs

Stop the server, run step 2 again (restores the snapshot), restart the server. It always returns the system to the same starting state.

## Known environment notes

- `mutmut` needs a POSIX `fork()`, so mutation runs should use WSL or the GitHub Actions Linux runner, not native Windows.
- The upstream `leave/tests/` suite exists but **does not count** for marks; team tests live in `tests/team/`.
