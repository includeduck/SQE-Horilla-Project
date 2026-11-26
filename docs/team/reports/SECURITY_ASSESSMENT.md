# Defensive Security Assessment (Area 3, security)

Carried out by Muhammad Wasay Tariq (24I-3071) as part of the Area 3 work taken over by team agreement. Brief §4: routes and data of both workflows, access matrix with ≥4 automated Playwright decisions across the two roles, OWASP ZAP passive scan while the workflows run, review of ≥2 security controls corroborated by source/configuration, and an open-source dependency audit. All testing used the team's local copy, synthetic seed data and test accounts; nothing was actively attacked.

## 1. Setup

| Item | Value |
|---|---|
| Target | Local Horilla 2.4.0 (`sqe-team` @ `2ceca1e`, including the PR #8 fixes), `manage.py runserver` on `http://localhost:8000`, database restored from the seeded snapshot (`scripts/team/reset.ps1`) before each run |
| Accounts | Synthetic seed accounts: `team_employee` (Employee) and `team_approver` (Leave Approver, reporting manager of the employee) |
| Playwright | 1.65.2, Chromium, Python sync API: [`tests/team/security/test_access_matrix.py`](../../../tests/team/security/test_access_matrix.py) |
| OWASP ZAP | 2.17.0 cross-platform (SHA-256 verified against the GitHub release digest), daemon on `127.0.0.1:8090`, **passive scanning only**; all browser and API traffic of the Playwright run was proxied through it (`<-loopback>` bypass rule so localhost is proxied) |
| Dependency audit | pip-audit 2.10.1 on the project virtualenv (Python 3.12) |
| Date | 2026-11-26 |

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1
.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
# optional proxy: ZAP daemon on 8090
$env:ZAP_PROXY="http://127.0.0.1:8090"
.\.venv\Scripts\python -m pytest -c tests\team\security\pytest.ini tests\team\security -v
.\.venv\Scripts\python -m pip_audit --format json -o docs\team\evidence\security\pip-audit.json
```

## 2. Routes and data in the two workflows

| Workflow | Route (method) | Data read / changed | Access check in source |
|---|---|---|---|
| W1 | `POST /api/leave/user-allocation-request/` | creates `LeaveAllocationRequest` (own) | authenticated; employee taken from the token |
| W1 | `GET/PUT/DELETE /api/leave/user-allocation-request/<id>/` | own allocation request | `get_allocation_request`: owner only, else `PermissionDenied` (fixed in #5) |
| W1 | `PUT /api/leave/allocation-approve/<id>/`, `allocation-reject/<id>/` | allocation status; `AvailableLeave.available_days` | `@approver_permission_required(..., "leave.change_leaveallocationrequest")`: not own request; designated approver, permission or manager |
| W1 | `GET /leave/leave-allocation-request-approve/<id>/` (web) | allocation status; balance | `@leave_allocation_reject_permission`: `delete_leaveallocationrequest` permission or reporting manager |
| W2 | `POST /api/leave/user-request/` | creates `LeaveRequest` (own) | authenticated |
| W2 | `PUT /api/leave/approve/<id>/`, `reject/<id>/`, `cancel/<id>/` | leave status; balance (deduct/refund) | `@approver_permission_required(..., "leave.change_leaverequest")` |
| W2 | `GET /leave/user-request-view/`, `/leave/user-request-one/<id>/` (web) | own requests and balance | login required; detail view checks ownership |
| Both | `GET /api/leave/available-leave/` | own `AvailableLeave` rows (shared record) | authenticated; filtered to the caller |
| Both | `POST /api/auth/login/`, `POST /login/` | JWT / session cookie | credentials; `django-axes` lockout |

## 3. Access matrix

Expected decisions from the source (✓ allowed, ✗ denied). Rows marked **AD-n** are verified automatically by Playwright.

| Action | Employee | Leave Approver |
|---|---|---|
| View own leave page and balance | ✓ **AD-1** | ✓ |
| Create own allocation / leave request | ✓ | ✓ |
| Approve **own** allocation request (web) | ✗ **AD-2** | ✗ (own request) |
| Approve a reportee's allocation request (web) | n/a | ✓ **AD-3** |
| Approve **own** leave request (API) | ✗ **AD-4** | ✗ (own request) |
| Approve a reportee's leave request (API) | n/a | ✓ **AD-5** |
| Edit/delete **another person's** allocation request (API) | ✗ **AD-6** | ✗ |

### Automated results (run through ZAP, 2026-11-26)

| ID | Role | Action | Expected | Observed | Evidence | Result |
|---|---|---|---|---|---|---|
| AD-1 | Employee | Open `/leave/user-request-view/` | allowed: 200, own balance shown | HTTP 200, "Team Annual Leave" card visible | `AD-1-employee-own-leave-page.png` | pass |
| AD-2 | Employee | `GET /leave/leave-allocation-request-approve/<id>/` on own request | denied: status stays `requested`, balance unchanged | redirected to dashboard with "You don't have permission."; status requested→requested, balance 0→0 | `AD-2-employee-approve-own-allocation.png` | pass |
| AD-3 | Leave Approver | same URL for the reportee's request | allowed: `approved`, balance +3 | HTTP 200, status approved, balance 0→3 | `AD-3-approver-approves-allocation.png` | pass |
| AD-4 | Employee | `PUT /api/leave/approve/<id>/` on own request | denied: 403, status `requested`, balance unchanged | HTTP 403 "You cannot approve or reject your own request.", balance 3→3 | `AD-4-response.json` | pass |
| AD-5 | Leave Approver | `PUT /api/leave/approve/<id>/` on reportee's request | allowed: 200, `approved`, balance −2 | HTTP 200, status approved, balance 3→1 | `AD-5-response.json` | pass |
| AD-6 | Employee | `DELETE /api/leave/user-allocation-request/<id>/` on the approver's request | denied: 403, record still exists | HTTP 403 "Access Denied..", record exists | `AD-6-response.json` | pass |

All files are in [`docs/team/evidence/security/`](../evidence/security/); machine-readable rows in `access-matrix-results.json`. Every decision also checks the **persisted state** (status and balance read back through the API), not only the HTTP code: AD-2 is a denial that answers HTTP 200 with a redirect, which a status-code check alone would misread.

## 4. OWASP ZAP passive scan

ZAP passively inspected **397 requests/responses** produced by the six access tests (both workflows, both roles, web and API). Full reports: [`zap-passive-report.html`](../evidence/security/zap-passive-report.html), [`zap-passive-report.json`](../evidence/security/zap-passive-report.json).

| ZAP alert (plugin) | ZAP risk | Where | Triage |
|---|---|---|---|
| Vulnerable JS Library (10003) | High | `static/build/js/moment.js`, `static/cdn/ajax/scripts/moment-with-locales.min.js`: moment.js **2.29.1** (CVE-2022-31129, CVE-2022-24785) | **SEC-03**, valid |
| CSP Header Not Set (10038) | Medium | all HTML pages | **SEC-02**, valid (not set in production config either) |
| Sub Resource Integrity Attribute Missing (90003) | Medium | `/my-dashboard/`: `apexcharts@7.8.0` from `cdn.jsdelivr.net` without `integrity` | **SEC-04**, valid |
| Cross-Domain JavaScript Source File Inclusion (10017) | Low | same CDN scripts | part of SEC-04 |
| Cookie No HttpOnly Flag (10010) | Low | `csrftoken` | accepted: Django's CSRF cookie must be readable by JavaScript for HTMX/AJAX requests (`CSRF_COOKIE_HTTPONLY=False` is the default); the session cookie *is* HttpOnly (§5) |
| X-Content-Type-Options Missing (10021) | Low | static and HTML responses | development only: `SECURE_CONTENT_TYPE_NOSNIFF=True` is applied in production mode (`horilla/settings/security.py`) |
| Server Leaks Version (10036) | Low | `WSGIServer/0.2 CPython/3.12.10` | development server only; production runs behind gunicorn/nginx |
| Sensitive Information in URL (10024) | Info | `/settings/get-date-format/?csrfmiddlewaretoken=…` | **SEC-07**, CSRF token sent in a GET query string |
| Potential XSS via user-controlled attribute (10031) | Info | `/my-dashboard/api/monthly-summary/?month=` | not confirmed passively; noted for Area 2 negative tests |
| Session management / authentication request identified, suspicious comments, modern web app | Info | various | informational |

## 5. Security controls reviewed

### C-1 Session cookie attributes: verified

| Attribute | Observed (`POST /login/` response) | Source / configuration | Assessment |
|---|---|---|---|
| `sessionid` HttpOnly | present | Django default `SESSION_COOKIE_HTTPONLY=True` | ✓ script cannot read the session |
| `sessionid` SameSite | `Lax` | Django default | ✓ not sent on cross-site POST/subresource requests (but see SEC-01: sent on top-level GET navigation) |
| `sessionid` lifetime | `Max-Age=43200` (12 h) | `SESSION_COOKIE_AGE` default 12 h (`horilla/settings/base.py:692`) | ✓ bounded session |
| `sessionid` / `csrftoken` Secure | **absent** locally | `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` set when `DEBUG=False` or `HORILLA_ENV=production` (`horilla/settings/security.py:78-79`) | ✓ in production; expected to be absent on local HTTP |
| Framing | `X-Frame-Options: SAMEORIGIN` | `horilla/settings/base.py:315` | ✓ clickjacking protection |
| Referrer / COOP | `Referrer-Policy: same-origin`, `Cross-Origin-Opener-Policy: same-origin` | Django security middleware | ✓ |

### C-2 Role and ownership checks: verified, one weakness

- API approve/reject use `approver_permission_required` (`horilla_api/api_decorators/base/decorators.py`): it refuses a user's **own** request first ("You cannot approve or reject your own request"), then allows designated approvers, holders of the change permission, or the employee's manager. AD-4 and AD-5 confirm both sides.
- Web allocation approve uses `leave_allocation_reject_permission` (`leave/decorators.py:77`): `delete_leaveallocationrequest` permission or the employee's **reporting manager**. AD-2 and AD-3 confirm both sides.
- Ownership of allocation requests: `get_allocation_request` raises `PermissionDenied` for a non-owner (fix for #5). AD-6 confirms; the unit test `test_non_owner_denied` covers it too.
- **Weakness (SEC-01):** the web approve action changes state on a plain **GET**, so the CSRF protection (which only covers unsafe methods) does not apply.

### C-3 CSRF protection on state changes: weakness found (SEC-01)

Django's `CsrfViewMiddleware` protects POST/PUT/DELETE. `leave_allocation_request_approve` (`leave/views.py:4629`) has no method restriction and approves on GET; AD-3 approved through a plain `page.goto(...)`. Because `sessionid` is `SameSite=Lax`, the browser **does** send it on a top-level GET navigation from another site, so a link like `<a href="https://horilla.example/leave/leave-allocation-request-approve/42/">` clicked by a logged-in manager approves request 42 without their intent.

## 6. Dependency audit

pip-audit checked **178 installed packages** (list with exact versions: [`audited-packages.txt`](../evidence/security/audited-packages.txt); raw result [`pip-audit.json`](../evidence/security/pip-audit.json)). One package could not be audited: `en-core-web-sm` (spaCy model wheel installed from a GitHub URL, not on PyPI). The JavaScript libraries were checked by ZAP's Retire.js-based rule (SEC-03).

| Component | Advisory | Evidence | Likely impact on this system | Recommended correction |
|---|---|---|---|---|
| `pdfkit` 1.0.0 | PYSEC-2026-2860 / CVE-2025-26240 / GHSA-9g3x-6x24-vf9f, no fixed version | pip-audit; used in `base/methods.py::generate_pdf` and payroll export | `from_string` with `enable-local-file-access` can run injected script and read local files. **Not used by the leave workflows.** Upstream already added a compensating control: rendered HTML is XSS-checked before pdfkit (`base/methods.py:1487`) | Keep the XSS guard; drop `enable-local-file-access` where possible, or replace wkhtmltopdf/pdfkit (unmaintained) with WeasyPrint |
| `svglib` 1.5.1 (transitive, via `xhtml2pdf`) | CVE-2026-132275 / GHSA-555j-qj3j-c8jv, fixed in 2.3.1 | pip-audit | Unbounded `<use>` expansion: a ~1.4 KB SVG can exhaust CPU/memory (DoS) when PDFs are rendered from SVG. Not reached by the leave workflows | Pin `svglib>=2.3.1` in `requirements.txt` |
| moment.js 2.29.1 (static JS) | CVE-2022-31129 (ReDoS in RFC 2822 parsing), CVE-2022-24785 (path traversal, Node only) | ZAP 10003 on two static files | Client-side ReDoS on very long date strings; path traversal does not apply in the browser | Update the bundled files to moment 2.30.1 |

## 7. Findings summary (linked to the risk register)

| ID | Finding | Root cause | Severity | Risk | Fix |
|---|---|---|---|---|---|
| SEC-01 (#38) | Web allocation approval changes state on GET (CSRF bypass) | View has no method restriction; approval implemented as a link | **Medium** | PR-03, PR-01 | Require POST (`@require_POST`) and send the CSRF token from the button (HTMX `hx-post`) |
| SEC-02 (#39) | No Content-Security-Policy on any page | No CSP middleware or header configured, production included | Medium | PR-03 | Add a CSP (e.g. `django-csp`) with `script-src 'self'` plus the needed CDN hosts/hashes |
| SEC-03 (#40) | Vulnerable moment.js 2.29.1 bundled | Vendored static file not updated | Medium | PR-09 | Upgrade to 2.30.1 |
| SEC-04 (#41) | CDN scripts loaded without Subresource Integrity | `<script src="https://cdn.jsdelivr.net/…">` without `integrity`/`crossorigin` | Medium | PR-09 | Add SRI hashes or self-host the scripts |
| SEC-05 (#42) | `pdfkit` 1.0.0 advisory, no upstream fix | Unmaintained library with local file access enabled | Low (not in our workflows; compensating XSS guard) | PR-09 | Replace pdfkit, or disable local file access |
| SEC-06 (#43) | `svglib` 1.5.1 DoS advisory | Unpinned transitive dependency | Low | PR-09 | Pin `svglib>=2.3.1` |
| SEC-07 (#44) | CSRF token sent in a GET query string | Front-end request to `/settings/get-date-format/` serialises the form including the token | Low | PR-03 | Send the token in the `X-CSRFToken` header, not the URL |

**Verified controls (no finding):** session cookie HttpOnly + SameSite + bounded lifetime; Secure flags and nosniff in production mode; X-Frame-Options; self-approval refused (API and web); manager/permission checks on approval; ownership check on allocation requests (#5 fix holds); lockout on login (django-axes).

**Observation for Area 2 (endpoint weakness, not security):** `POST /api/leave/user-allocation-request/` answers an empty `200` with no id or body, so a client cannot identify the record it created (the security test has to look it up by description), while the leave-request endpoint correctly returns `201` with the record.
