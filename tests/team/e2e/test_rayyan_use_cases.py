"""UC-RAY-01/02: ten individually attributed browser flows with HTTP/ORM readback."""

import re
from datetime import date, timedelta

import pytest
from playwright.sync_api import expect

FLOWS = ("MAIN", "A1", "A2", "E1", "E2")


def login(page, h):
    response = page.goto(h.base + "/login/")
    assert response.status == 200
    page.get_by_label("Username", exact=True).fill("team_employee")
    page.get_by_label("Password", exact=True).fill("TeamEmploy#2026")
    page.get_by_role("button", name="Secure Sign-in").click()
    page.wait_for_url(lambda url: "/login/" not in str(url))


def open_form(page, h, kind):
    listing = "/leave/leave-allocation-request-view/" if kind == "allocation" else "/leave/user-request-view/"
    route = "/leave/leave-allocation-request-create/" if kind == "allocation" else "/leave/leave-request-create/"
    response = page.goto(h.base + listing)
    assert response.status == 200
    page.locator(f'[hx-get="{route}"]').first.click()
    form = page.locator(f'form[hx-post^="{route}"]')
    expect(form).to_be_visible()
    expect(form.locator('[name="description"]')).to_be_visible()
    return form, route


def select_field(form, name, value):
    # Select2 wraps native selects. This changes the real browser form control
    # and dispatches its normal change event; target writes still use the UI.
    form.locator(f'select[name="{name}"]').select_option(str(value), force=True)
    expect(form.locator(f'select[name="{name}"]')).to_have_value(str(value))


def submit(page, form, route):
    # The leave template provides a visible Save proxy, while allocation uses
    # a normal submit button. Both execute the application's own HTMX handlers.
    button = form.locator("button:visible").filter(has_text=re.compile(r"^Save$"))
    if button.count() == 0:
        button = form.locator('button[type="submit"]:visible').first
    else:
        button = button.first
    with page.expect_response(lambda response: route in response.url and response.request.method == "POST") as posted:
        button.click()
    assert posted.value.status == 200


def visible_error(page):
    errors = page.locator(".errorlist, .oh-input__error, .invalid-feedback")
    expect(errors.first).to_be_visible()
    text = " ".join(errors.all_text_contents())
    assert text.strip()
    return text


@pytest.mark.parametrize("flow", FLOWS, ids=lambda value: "UC-RAY-01-" + value)
def test_rayyan_allocation_request(ray_page, leave_http, flow, record_property):
    from leave.models import LeaveAllocationRequest

    page, h = ray_page, leave_http
    case_id = "UC-RAY-01-" + flow
    record_property("case_id", case_id)
    record_property("contributor", "Syed Muhammad Rayyan Hassan / 24I-3000")
    login(page, h)
    form, route = open_form(page, h, "allocation")
    select_field(form, "leave_type_id", h.context["leave_type"].pk)
    select_field(form, "employee_id", h.context["employee"].pk)
    form.locator('[name="requested_days"]').fill("5")
    description = "Synthetic " + case_id
    form.locator('[name="description"]').fill("" if flow == "A2" else description)
    if flow == "A1":
        form.locator('[name="attachment"]').set_input_files({"name": "synthetic.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4 synthetic fixture"})
    if flow == "E1":
        select_field(form, "leave_type_id", "")
    if flow == "E2":
        form.locator('[name="requested_days"]').fill("")
    before = h.snapshot()
    submit(page, form, route)
    if flow in {"A2", "E1", "E2"}:
        assert "required" in visible_error(page).lower()
        assert h.snapshot() == before
        assert LeaveAllocationRequest.objects.count() == 0
        if flow != "A2":
            return
        form = page.locator(f'form[hx-post^="{route}"]')
        form.locator('[name="description"]').fill(description)
        submit(page, form, route)
    expect(page.locator(".oh-alert--success, .oh-alert.success").first).to_be_visible()
    assert len(h.allocations()) == 1
    row = h.allocations()[0]
    detail = h.allocation_detail(row["id"])
    assert detail["description"] == description and detail["status"] == "requested"
    assert detail["employee_id"]["id"] == h.context["employee"].pk
    assert float(detail["requested_days"]) == 5
    assert h.balance() == (0.0, 0.0)
    stored = LeaveAllocationRequest.objects.get(pk=row["id"])
    assert stored.employee_id_id == h.context["employee"].pk
    if flow == "A1":
        assert stored.attachment and detail["attachment"]
        with stored.attachment.open("rb") as source:
            assert source.read() == b"%PDF-1.4 synthetic fixture"


@pytest.mark.parametrize("flow", FLOWS, ids=lambda value: "UC-RAY-02-" + value)
def test_rayyan_leave_request(ray_page, leave_http, flow, record_property):
    from leave.models import LeaveRequest

    page, h = ray_page, leave_http
    case_id = "UC-RAY-02-" + flow
    record_property("case_id", case_id)
    record_property("contributor", "Syed Muhammad Rayyan Hassan / 24I-3000")
    h.grant(5)  # W1 setup through the existing real HTTP helper; W2 write is UI.
    login(page, h)
    form, route = open_form(page, h, "leave")
    select_field(form, "leave_type_id", h.context["leave_type"].pk)
    anchor = date.fromisoformat(h.baseline("leave")["start_date"])
    duration = 6 if flow in {"A2", "E1"} else 1 if flow == "A1" else 3
    end = anchor - timedelta(days=1) if flow == "E2" else anchor + timedelta(days=duration - 1)
    form.locator('[name="start_date"]').fill(anchor.isoformat())
    form.locator('[name="end_date"]').fill(end.isoformat())
    breakdown = "first_half" if flow == "A1" else "full_day"
    for field in ("start_date_breakdown", "end_date_breakdown"):
        select_field(form, field, breakdown)
    description = "Synthetic " + case_id
    form.locator('[name="description"]').fill(description)
    before = h.snapshot()
    submit(page, form, route)
    if flow in {"A2", "E1", "E2"}:
        text = visible_error(page).lower()
        assert ("balance" in text or "enough" in text) if flow != "E2" else ("date" in text)
        assert h.snapshot() == before
        assert LeaveRequest.objects.count() == 0
        if flow != "A2":
            return
        form = page.locator(f'form[hx-post^="{route}"]')
        form.locator('[name="end_date"]').fill((anchor + timedelta(days=2)).isoformat())
        submit(page, form, route)
    expect(page.locator(".oh-alert--success, .oh-alert.success").first).to_be_visible()
    assert len(h.leaves()) == 1
    detail = h.leave_detail(h.leaves()[0]["id"])
    assert detail["description"] == description and detail["status"] == "requested"
    assert float(detail["requested_days"]) == (0.5 if flow == "A1" else 3.0)
    assert h.balance() == (5.0, 0.0)
    stored = LeaveRequest.objects.get(pk=detail["id"])
    assert stored.employee_id_id == h.context["employee"].pk
    assert stored.created_by_id == h.context["employee"].pk
