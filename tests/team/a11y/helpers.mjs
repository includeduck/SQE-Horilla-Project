// Shared helpers for the Area 3 usability/accessibility suite.
// Runs against a live Horilla on the seeded snapshot (scripts/team/reset.ps1).
import { expect } from "@playwright/test";

export const BASE = process.env.HORILLA_URL || "http://localhost:8000";
// Synthetic seed accounts (scripts/team/seed_team.py).
export const ACCOUNTS = {
  employee: ["team_employee", "TeamEmploy#2026"],
  approver: ["team_approver", "TeamApprove#2026"],
};
export const SCREENS = {
  allocation: { listing: "/leave/leave-allocation-request-view/", route: "/leave/leave-allocation-request-create/" },
  leave: { listing: "/leave/user-request-view/", route: "/leave/leave-request-create/" },
};
export const RUN = process.env.GITHUB_RUN_ID || String(Date.now());

export async function login(page, role) {
  const [user, pass] = ACCOUNTS[role];
  await page.goto(`${BASE}/login/`);
  await page.getByLabel("Username", { exact: true }).fill(user);
  await page.getByLabel("Password", { exact: true }).fill(pass);
  await Promise.all([page.waitForURL((u) => !u.pathname.startsWith("/login")), page.locator("form button[type=submit]").click()]);
}

// Horilla shows a first-visit guided tour (driver.js) that covers the page.
// A keyboard user closes it with Escape, so the tests do the same.
export async function dismissTour(page) {
  if (await page.locator(".driver-popover").count()) {
    await page.keyboard.press("Escape");
    await expect(page.locator(".driver-overlay")).toHaveCount(0);
  }
}

export async function openScreen(page, kind) {
  await page.goto(BASE + SCREENS[kind].listing);
  await page.waitForLoadState("networkidle");
  await dismissTour(page);
}

export async function openForm(page, kind) {
  const { route } = SCREENS[kind];
  await openScreen(page, kind);
  await page.locator(`[hx-get^="${route}"]:visible`).first().click();
  const form = page.locator(`form[hx-post^="${route}"]`);
  await expect(form).toBeVisible();
  await page.waitForLoadState("networkidle");
  return form;
}

// Select2 replaces native <select>s; choose an option the way a user does.
export async function pickSelect2(page, form, name, optionText) {
  await form.locator(`#select2-id_${name}-container`).click();
  await page.locator(".select2-results__option", { hasText: optionText }).first().click();
  await expect(form.locator(`#select2-id_${name}-container`)).toContainText(optionText);
}

export async function apiFor(playwright, role) {
  const anon = await playwright.request.newContext({ baseURL: BASE });
  const [username, password] = ACCOUNTS[role];
  const res = await anon.post("/api/auth/login/", { data: { username, password } });
  expect(res.ok()).toBeTruthy();
  const { access } = await res.json();
  await anon.dispose();
  return playwright.request.newContext({ baseURL: BASE, extraHTTPHeaders: { Authorization: `Bearer ${access}` } });
}

export async function leaveTypeId(api) {
  const rows = (await (await api.get("/api/leave/available-leave/")).json()).results;
  return rows.find((r) => r.leave_type_id.name === "Team Annual Leave").leave_type_id.id;
}

export async function balance(api) {
  const rows = (await (await api.get("/api/leave/available-leave/")).json()).results;
  return rows.find((r) => r.leave_type_id.name === "Team Annual Leave").available_days;
}

// W1 through the API (setup for W2): employee requests `days`, approver approves.
export async function grantBalance(playwright, days) {
  const emp = await apiFor(playwright, "employee");
  const appr = await apiFor(playwright, "approver");
  const description = `a11y setup ${RUN} ${Math.random()}`;
  const created = await emp.post("/api/leave/user-allocation-request/", {
    data: { leave_type_id: await leaveTypeId(emp), requested_days: days, description },
  });
  expect(created.ok()).toBeTruthy();
  const mine = (await (await emp.get("/api/leave/user-allocation-request/")).json()).results;
  const id = mine.find((r) => r.description === description).id;
  expect((await appr.put(`/api/leave/allocation-approve/${id}/`, { data: {} })).ok()).toBeTruthy();
  await emp.dispose();
  await appr.dispose();
}

// A Monday in 2031+ that changes per run, so repeated runs never overlap.
export function freshMonday() {
  const d = new Date(Date.UTC(2031, 0, 6));
  d.setUTCDate(d.getUTCDate() + 7 * (Math.floor(Date.now() / 60000) % 400));
  return d;
}
export const iso = (d) => d.toISOString().slice(0, 10);
export const addDays = (d, n) => new Date(d.getTime() + n * 86400000);
