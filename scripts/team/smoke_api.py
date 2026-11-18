"""Smoke check that the leave API is reachable with the team seed accounts.
Usage: .venv/Scripts/python scripts/team/smoke_api.py  (server must be running on :8000)"""
import sys
import requests

BASE = "http://localhost:8000/api"
ACCOUNTS = {"employee": ("team_employee", "TeamEmploy#2026"), "approver": ("team_approver", "TeamApprove#2026")}


def token(role):
    u, p = ACCOUNTS[role]
    r = requests.post(f"{BASE}/auth/login/", json={"username": u, "password": p}, timeout=30)
    r.raise_for_status()
    body = r.json()
    return body.get("access") or body.get("access_token") or body.get("token")


ok = True
for role in ACCOUNTS:
    h = {"Authorization": f"Bearer {token(role)}"}
    r = requests.get(f"{BASE}/leave/available-leave/", headers=h, timeout=30)
    print(f"{role:9s} GET /leave/available-leave/ -> {r.status_code} {r.text[:160]}")
    ok &= r.status_code == 200
sys.exit(0 if ok else 1)
