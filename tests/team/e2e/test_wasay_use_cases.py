"""UC-WAS-01/02: approver use cases, every flow automated in the browser.

Specification: docs/team/WASAY_USE_CASES.md (Muhammad Wasay Tariq, 24I-3071).
Each test asserts what the screen shows and the postconditions through the
API: status, the requester's balance, and that the approver's (7) and an
unrelated outsider's (9) balances never change.
Runs on the isolated Area 2 live-server fixtures (tests/team/api/conftest.py).
"""

import asyncio
import re

import pytest
from playwright.async_api import expect

FLOWS = ("MAIN", "A1", "A2", "E1", "E2")
PASSWORDS = {"employee": ("team_employee", "TeamEmploy#2026"), "approver": ("team_approver", "TeamApprove#2026")}
REASON = "Team is short-staffed that week"


async def login(page, h, role):
    user, password = PASSWORDS[role]
    response = await page.goto(h.base + "/login/")
    assert response.status == 200
    await page.get_by_label("Username", exact=True).fill(user)
    await page.get_by_label("Password", exact=True).fill(password)
    form = page.locator("form").filter(has=page.locator('input[name="username"]'))
    await form.locator('button[type="submit"]').click()
    await page.wait_for_url(lambda url: "/login/" not in str(url))


async def dismiss_tour(page):
    # First-visit guided tour (driver.js); a keyboard user closes it with Escape.
    if await page.locator(".driver-popover").count():
        await page.keyboard.press("Escape")
        await expect(page.locator(".driver-overlay")).to_have_count(0)


async def eventually(check, timeout=10.0):
    """Poll a (synchronous) API read-back until it holds; returns the last value."""
    value = None
    for _ in range(int(timeout / 0.25)):
        value = check()
        if value:
            return value
        await asyncio.sleep(0.25)
    return value


async def answer_confirmation(page, accept):
    """Horilla replaces the native confirm() with its own dialog (Confirm / Cancel)."""
    dialog = page.get_by_role("dialog").filter(has_text=re.compile(r"approve", re.I))
    await expect(dialog.first).to_be_visible()
    await dialog.first.get_by_role("button", name="Confirm" if accept else "Cancel").click()


def others_unchanged(h):
    assert h.balance("approver") == (7.0, 0.0), "approver's own balance must not change"
    assert h.balance("outsider") == (9.0, 0.0), "unrelated employee's balance must not change"


# --- UC-WAS-01: approver decides an allocation request ---------------------------
async def open_allocation_requests(page, h):
    await page.goto(h.base + "/leave/leave-allocation-request-view/")
    await page.wait_for_load_state("networkidle")
    await dismiss_tour(page)
    tab = page.locator("[role=tab], .oh-tabs__tab").filter(has_text="Leave Allocation Requests").filter(has_not_text="My ")
    await tab.first.click()
    await page.wait_for_load_state("networkidle")


async def open_reject_form(page, route):
    await page.locator(f'[hx-get="{route}"]:visible').first.click()
    form = page.locator(f'form[hx-post="{route}"], form[action="{route}"]').first
    await expect(form).to_be_visible()
    return form


@pytest.mark.asyncio
@pytest.mark.parametrize("flow", FLOWS, ids=lambda f: "UC-WAS-01-" + f)
async def test_uc_was_01_allocation_decision(ray_page, leave_http, flow, record_property):
    page, h = ray_page, leave_http
    record_property("case_id", "UC-WAS-01-" + flow)
    record_property("contributor", "Muhammad Wasay Tariq / 24I-3071")
    body = h.baseline("allocation")
    body["requested_days"] = 3
    pk = h.create_allocation(body)  # P1: requested, 3 days
    status = lambda: h.allocation_detail(pk)["status"]  # noqa: E731
    approve = f'a[href="/leave/leave-allocation-request-approve/{pk}/"]'
    reject_route = f"/leave/leave-allocation-request-reject/{pk}/"

    if flow == "E2":
        # The employee opens the approve link for their own request.
        await login(page, h, "employee")
        await page.goto(h.base + f"/leave/leave-allocation-request-approve/{pk}/")
        await dismiss_tour(page)
        await expect(page.get_by_text(re.compile(r"don.t have (the )?permission", re.I)).first).to_be_visible()
        assert status() == "requested" and h.balance() == (0.0, 0.0)
        others_unchanged(h)
        return

    await login(page, h, "approver")
    await open_allocation_requests(page, h)
    await expect(page.locator(approve).first).to_be_visible()

    if flow in ("MAIN", "A2"):
        if flow == "A2":
            # Change of mind: dismiss the confirmation; nothing happens.
            await page.locator(approve).first.click()
            await answer_confirmation(page, accept=False)
            await asyncio.sleep(1)
            assert status() == "requested" and h.balance() == (0.0, 0.0)
        await page.locator(approve).first.click()
        await answer_confirmation(page, accept=True)
        await expect(page.get_by_text("Leave allocation request approved successfully").first).to_be_visible()
        assert await eventually(lambda: status() == "approved")
        assert h.balance() == (3.0, 0.0), "employee credited exactly 3 days"
    elif flow == "A1":
        form = await open_reject_form(page, reject_route)
        await form.locator('textarea[name="reason"]').fill(REASON)
        await form.locator('button[type="submit"], input[type="submit"]').first.click()
        await expect(page.get_by_text("Leave allocation request rejected successfully").first).to_be_visible()
        assert await eventually(lambda: status() == "rejected")
        assert h.allocation_detail(pk).get("reject_reason", REASON) == REASON
        assert h.balance() == (0.0, 0.0)
    elif flow == "E1":
        form = await open_reject_form(page, reject_route)
        reason = form.locator('textarea[name="reason"]')
        await form.locator('button[type="submit"], input[type="submit"]').first.click()
        assert await reason.evaluate("e => !e.validity.valid && e.validity.valueMissing")
        await asyncio.sleep(1)
        assert status() == "requested" and h.balance() == (0.0, 0.0)
    others_unchanged(h)


# --- UC-WAS-02: approver decides a leave request -----------------------------------
async def open_leave_requests(page, h):
    await page.goto(h.base + "/leave/request-view/")
    await page.wait_for_load_state("networkidle")
    await dismiss_tour(page)


@pytest.mark.asyncio
@pytest.mark.parametrize("flow", FLOWS, ids=lambda f: "UC-WAS-02-" + f)
async def test_uc_was_02_leave_decision(ray_page, leave_http, flow, record_property):
    page, h = ray_page, leave_http
    record_property("case_id", "UC-WAS-02-" + flow)
    record_property("contributor", "Muhammad Wasay Tariq / 24I-3071")
    h.grant(5)  # P1: employee balance 5 (W1 through the API)
    pk = h.create_leave()  # P2: requested leave
    days = float(h.leave_detail(pk)["requested_days"])
    assert 0 < days < 5
    status = lambda: h.leave_detail(pk)["status"]  # noqa: E731
    approve = f'[hx-get="/leave/request-approve/{pk}/"]'
    reject_route = f"/leave/request-cancel/{pk}/"

    if flow == "E2":
        await login(page, h, "employee")
        await page.goto(h.base + f"/leave/request-approve/{pk}/")
        await dismiss_tour(page)
        await expect(page.get_by_text(re.compile(r"permission|cannot approve your own", re.I)).first).to_be_visible()
        assert status() == "requested" and h.balance() == (5.0, 0.0)
        others_unchanged(h)
        return

    if flow == "A2":
        h.approve_leave(pk)  # an earlier approval
        assert h.balance() == (5.0 - days, 0.0)

    await login(page, h, "approver")
    await open_leave_requests(page, h)

    if flow == "MAIN":
        await page.locator(approve).first.click()
        await answer_confirmation(page, accept=True)
        await expect(page.get_by_text(re.compile(r"Leave request approved successfully", re.I)).first).to_be_visible()
        assert await eventually(lambda: status() == "approved")
        assert h.balance() == (5.0 - days, 0.0), "requester debited exactly the requested days"
    elif flow in ("A1", "A2"):
        form = await open_reject_form(page, reject_route)
        await form.locator('textarea[name="reason"]').fill(REASON)
        await form.locator('button[type="submit"], input[type="submit"]').first.click()
        await expect(page.get_by_text(re.compile(r"Leave request rejected successfully", re.I)).first).to_be_visible()
        assert await eventually(lambda: status() == "rejected")
        assert h.leave_detail(pk).get("reject_reason", REASON) == REASON
        assert h.balance() == (5.0, 0.0), "rejection leaves / refunds the requester's full balance"
    elif flow == "E1":
        form = await open_reject_form(page, reject_route)
        reason = form.locator('textarea[name="reason"]')
        await form.locator('button[type="submit"], input[type="submit"]').first.click()
        assert await reason.evaluate("e => !e.validity.valid && e.validity.valueMissing")
        await asyncio.sleep(1)
        assert status() == "requested" and h.balance() == (5.0, 0.0)
    others_unchanged(h)
