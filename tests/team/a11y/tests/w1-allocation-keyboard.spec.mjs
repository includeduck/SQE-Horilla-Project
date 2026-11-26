// W1 task test with keyboard navigation (brief §3).
// The employee requests a leave allocation using only the keyboard inside the
// form: focus must reach the required fields and the submit button in order,
// and the keyboard must be able to submit the form.
import { test, expect } from "@playwright/test";
import { login, openForm, apiFor, RUN } from "../helpers.mjs";

test("W1: employee requests an allocation using only the keyboard", async ({ page, playwright }) => {
  await login(page, "employee");
  const form = await openForm(page, "allocation");
  const description = `Keyboard allocation ${RUN}`;

  // Start on the modal's first control (Close) and tab through the form,
  // recording which control holds focus after each Tab.
  await form.locator("button.oh-modal__close--custom").focus();
  const order = [];
  const focusedName = () =>
    page.evaluate(() => {
      const el = document.activeElement;
      if (el.classList.contains("select2-selection")) return "select2:" + el.getAttribute("aria-labelledby");
      if (el.tagName === "BUTTON") return "button:" + (el.name || el.innerText.trim());
      return el.name || el.tagName;
    });
  for (let i = 0; i < 7; i++) {
    await page.keyboard.press("Tab");
    order.push(await focusedName());
  }
  test.info().annotations.push({ type: "tab order", description: order.join(" -> ") });

  // Required fields and the submit button are reached, in this order.
  const idx = (pred) => order.findIndex(pred);
  const leaveType = idx((n) => n.includes("select2-id_leave_type_id"));
  const days = idx((n) => n === "requested_days");
  const desc = idx((n) => n === "description");
  const save = idx((n) => /^button:Save$/i.test(n));
  expect(leaveType, `tab order: ${order}`).toBeGreaterThanOrEqual(0);
  expect(days).toBeGreaterThan(leaveType);
  expect(desc).toBeGreaterThan(days);
  expect(save).toBeGreaterThan(desc);

  // Fill the form with the keyboard only.
  await form.locator("button.oh-modal__close--custom").focus(); // same start point
  await page.keyboard.press("Tab"); // leave type (Select2)
  await expect(form.locator(".select2-selection").first()).toBeFocused();
  await page.keyboard.press("Enter"); // open the list
  await page.keyboard.type("Team Annual");
  await page.keyboard.press("Enter"); // choose
  await expect(form.locator("#select2-id_leave_type_id-container")).toContainText("Team Annual Leave");
  await page.keyboard.press("Tab");
  await expect(form.locator('[name="requested_days"]')).toBeFocused();
  await page.keyboard.type("4");
  await page.keyboard.press("Tab"); // attachment (optional)
  await page.keyboard.press("Tab");
  await expect(form.locator('[name="description"]')).toBeFocused();
  await page.keyboard.type(description);
  await page.keyboard.press("Tab"); // "Save & add another"
  await page.keyboard.press("Tab");
  await expect(form.locator("button.oh-btn--secondary[type=submit]")).toBeFocused();
  await page.keyboard.press("Enter"); // submit with the keyboard

  // Confirmation shown, and the record really exists. Horilla's toast reads
  // "Leave allocation request updated" even for a new request (usability
  // finding UX-01 in ACCESSIBILITY_TESTING.md), so either wording is accepted.
  const toast = page.getByText(/Leave allocation request (created|updated)/i).first();
  await expect(toast).toBeVisible();
  test.info().annotations.push({ type: "confirmation shown", description: (await toast.innerText()).trim() });
  const api = await apiFor(playwright, "employee");
  const mine = (await (await api.get("/api/leave/user-allocation-request/")).json()).results;
  const row = mine.find((r) => r.description === description);
  expect(row, "allocation saved").toBeTruthy();
  expect(Number(row.requested_days)).toBe(4);
  expect(row.status).toBe("requested");
  await api.dispose();
});
