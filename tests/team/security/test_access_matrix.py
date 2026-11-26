"""Access-control checks for the two workflows, automated with Playwright.

Brief §4: verify at least four access decisions across the two roles, at least
one allowed and one denied, recording role, action, expected result, observed
result and evidence.

Runs against a live Horilla started from the seeded snapshot
(scripts/team/reset.ps1, then manage.py runserver). Optionally routes all
browser and API traffic through OWASP ZAP for the passive scan:

    set ZAP_PROXY=http://localhost:8090      (optional)
    python -m pytest -c tests/team/security/pytest.ini tests/team/security -v

Accounts are the synthetic seed accounts from scripts/team/seed_team.py.
Results: docs/team/evidence/security/access-matrix-results.json + screenshots.
"""

import json
import os
from datetime import date, timedelta
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

BASE = os.environ.get("HORILLA_URL", "http://localhost:8000")
ZAP = os.environ.get("ZAP_PROXY")
EVIDENCE = Path(__file__).resolve().parents[3] / "docs/team/evidence/security"
ACCOUNTS = {"Employee": ("team_employee", "TeamEmploy#2026"), "Leave Approver": ("team_approver", "TeamApprove#2026")}
RESULTS = []
RUN = os.environ.get("GITHUB_RUN_ID") or __import__("datetime").datetime.now().strftime("%Y%m%d%H%M%S")
# A far-future working week so the requests never hit past-date or holiday rules.
START = date(2031, 3, 3)


def proxy():
    # "<-loopback>" makes Chromium send localhost traffic through the proxy too.
    return {"server": ZAP, "bypass": "<-loopback>"} if ZAP else None


@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(pw):
    b = pw.chromium.launch(proxy=proxy())
    yield b
    b.close()


@pytest.fixture(scope="session")
def api(pw):
    """One Playwright API context per role, authenticated with the app's JWT login."""
    contexts = {}
    for role, (user, pwd) in ACCOUNTS.items():
        anon = pw.request.new_context(base_url=BASE, proxy=proxy())
        resp = anon.post("/api/auth/login/", data={"username": user, "password": pwd})
        assert resp.ok, f"login failed for {role}: {resp.status}"
        token = resp.json()["access"]
        anon.dispose()
        contexts[role] = pw.request.new_context(
            base_url=BASE, proxy=proxy(), extra_http_headers={"Authorization": f"Bearer {token}"}
        )
    yield contexts
    for c in contexts.values():
        c.dispose()


def login(browser, role):
    ctx = browser.new_context()
    page = ctx.new_page()
    user, pwd = ACCOUNTS[role]
    page.goto(f"{BASE}/login/")
    page.fill("input[name='username']", user)
    page.fill("input[name='password']", pwd)
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    assert "/login" not in page.url, f"{role} login failed"
    return ctx, page


def leave_type_id(api):
    rows = api["Employee"].get("/api/leave/available-leave/").json()["results"]
    return next(r["leave_type_id"]["id"] for r in rows if r["leave_type_id"]["name"] == "Team Annual Leave")


def record(ad, role, action, expected, observed, evidence, passed):
    RESULTS.append({"id": ad, "role": role, "action": action, "expected": expected,
                    "observed": observed, "evidence": evidence, "result": "pass" if passed else "FAIL"})
    assert passed, f"{ad}: expected {expected}, observed {observed}"


def shot(page, name):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(EVIDENCE / f"{name}.png"), full_page=True)
    return f"docs/team/evidence/security/{name}.png"


def created_allocation(api, role, description):
    """The allocation-create endpoint answers an empty 200 (no id), so look the
    new record up by its unique description in the caller's own list."""
    rows = api[role].get("/api/leave/user-allocation-request/").json()["results"]
    return next(r["id"] for r in rows if r["description"] == description)


@pytest.fixture(scope="session")
def allocation(api):
    """W1 data: the employee files a 3-day allocation request (status 'requested')."""
    lt = leave_type_id(api)
    desc = f"Security check allocation {RUN}"
    resp = api["Employee"].post("/api/leave/user-allocation-request/",
                                data={"leave_type_id": lt, "requested_days": 3, "description": desc})
    assert resp.status in (200, 201), resp.text()
    return created_allocation(api, "Employee", desc)


def allocation_status(api, pk):
    return api["Leave Approver"].get(f"/api/leave/allocation-request/{pk}/").json()["status"]


def balance(api):
    rows = api["Employee"].get("/api/leave/available-leave/").json()["results"]
    return next(r["available_days"] for r in rows if r["leave_type_id"]["name"] == "Team Annual Leave")


# --- AD-1 Employee views own leave page: ALLOWED -------------------------------
def test_ad1_employee_views_own_leave_page(browser):
    ctx, page = login(browser, "Employee")
    resp = page.goto(f"{BASE}/leave/user-request-view/")
    page.wait_for_load_state("networkidle")
    ok = resp.status == 200 and page.get_by_text("Team Annual Leave").first.is_visible()
    ev = shot(page, "AD-1-employee-own-leave-page")
    ctx.close()
    record("AD-1", "Employee", "Open own 'My Leave' page /leave/user-request-view/", "allowed: 200 and own balance shown",
           f"HTTP {resp.status}, balance card visible={ok}", ev, ok)


# --- AD-2 Employee approves own allocation request (web): DENIED ---------------
def test_ad2_employee_cannot_approve_own_allocation(browser, api, allocation):
    before_status, before_balance = allocation_status(api, allocation), balance(api)
    ctx, page = login(browser, "Employee")
    resp = page.goto(f"{BASE}/leave/leave-allocation-request-approve/{allocation}/")
    page.wait_for_load_state("networkidle")
    ev = shot(page, "AD-2-employee-approve-own-allocation")
    ctx.close()
    after_status, after_balance = allocation_status(api, allocation), balance(api)
    ok = after_status == "requested" and after_balance == before_balance
    record("AD-2", "Employee", f"GET /leave/leave-allocation-request-approve/{allocation}/ (own request)",
           "denied: status stays 'requested', balance unchanged",
           f"HTTP {resp.status}, status {before_status}->{after_status}, balance {before_balance}->{after_balance}", ev, ok)


# --- AD-3 Approver approves the employee's allocation (web): ALLOWED -----------
def test_ad3_approver_approves_employee_allocation(browser, api, allocation):
    before = balance(api)
    ctx, page = login(browser, "Leave Approver")
    resp = page.goto(f"{BASE}/leave/leave-allocation-request-approve/{allocation}/")
    page.wait_for_load_state("networkidle")
    ev = shot(page, "AD-3-approver-approves-allocation")
    ctx.close()
    status, after = allocation_status(api, allocation), balance(api)
    ok = status == "approved" and after == before + 3
    record("AD-3", "Leave Approver", f"GET /leave/leave-allocation-request-approve/{allocation}/ (reportee's request)",
           "allowed: status 'approved', balance +3", f"HTTP {resp.status}, status {status}, balance {before}->{after}", ev, ok)


@pytest.fixture(scope="session")
def leave_request(api, allocation):
    """W2 data: after AD-3 the employee has days; files a 2-day leave request."""
    lt = leave_type_id(api)
    resp = api["Employee"].post("/api/leave/user-request/", data={
        "leave_type_id": lt, "start_date": START.isoformat(), "end_date": (START + timedelta(1)).isoformat(),
        "start_date_breakdown": "full_day", "end_date_breakdown": "full_day", "description": f"Security check leave {RUN}"})
    assert resp.status in (200, 201), resp.text()
    return resp.json()["id"]


def leave_status(api, pk):
    return api["Employee"].get(f"/api/leave/user-request/{pk}/").json()["status"]


# --- AD-4 Employee approves own leave request (API): DENIED --------------------
def test_ad4_employee_cannot_approve_own_leave(api, leave_request):
    before = balance(api)
    resp = api["Employee"].put(f"/api/leave/approve/{leave_request}/", data={})
    status, after = leave_status(api, leave_request), balance(api)
    ok = resp.status == 403 and status == "requested" and after == before
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "AD-4-response.json").write_text(json.dumps({"status": resp.status, "body": resp.text()}, indent=2))
    record("AD-4", "Employee", f"PUT /api/leave/approve/{leave_request}/ (own request)",
           "denied: 403, status 'requested', balance unchanged",
           f"HTTP {resp.status} {resp.text()[:80]}, status {status}, balance {before}->{after}",
           "docs/team/evidence/security/AD-4-response.json", ok)


# --- AD-5 Approver approves the employee's leave (API): ALLOWED ----------------
def test_ad5_approver_approves_employee_leave(api, leave_request):
    before = balance(api)
    resp = api["Leave Approver"].put(f"/api/leave/approve/{leave_request}/", data={})
    status, after = leave_status(api, leave_request), balance(api)
    ok = resp.status == 200 and status == "approved" and after == before - 2
    (EVIDENCE / "AD-5-response.json").write_text(json.dumps({"status": resp.status, "body": resp.text()}, indent=2))
    record("AD-5", "Leave Approver", f"PUT /api/leave/approve/{leave_request}/ (reportee's request)",
           "allowed: 200, status 'approved', balance -2", f"HTTP {resp.status}, status {status}, balance {before}->{after}",
           "docs/team/evidence/security/AD-5-response.json", ok)


# --- AD-6 Employee deletes another person's allocation (API): DENIED -----------
def test_ad6_employee_cannot_delete_others_allocation(api):
    lt = leave_type_id(api)
    desc = f"Approver own allocation {RUN}"
    own = api["Leave Approver"].post("/api/leave/user-allocation-request/",
                                     data={"leave_type_id": lt, "requested_days": 1, "description": desc})
    assert own.status in (200, 201), own.text()
    pk = created_allocation(api, "Leave Approver", desc)
    resp = api["Employee"].delete(f"/api/leave/user-allocation-request/{pk}/")
    still_there = api["Leave Approver"].get(f"/api/leave/allocation-request/{pk}/").status == 200
    ok = resp.status == 403 and still_there
    (EVIDENCE / "AD-6-response.json").write_text(json.dumps({"status": resp.status, "body": resp.text()}, indent=2))
    record("AD-6", "Employee", f"DELETE /api/leave/user-allocation-request/{pk}/ (approver's request)",
           "denied: 403, record still exists", f"HTTP {resp.status} {resp.text()[:80]}, record exists={still_there}",
           "docs/team/evidence/security/AD-6-response.json", ok)


@pytest.fixture(scope="session", autouse=True)
def write_results():
    yield
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "access-matrix-results.json").write_text(
        json.dumps({"base_url": BASE, "zap_proxy": ZAP, "decisions": RESULTS}, indent=2))
