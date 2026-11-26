// W2 task test (brief §3): the employee first submits a value the business rule
// rejects (more days than the balance, BR-01), the error must explain what to
// correct, then the corrected request succeeds.
import { test, expect } from "@playwright/test";
import { login, openForm, pickSelect2, grantBalance, apiFor, balance, freshMonday, iso, addDays, RUN } from "../helpers.mjs";

test("W2: over-balance request is rejected with a clear error, then corrected", async ({ page, playwright }) => {
  await grantBalance(playwright, 3); // W1 setup through the API
  const api = await apiFor(playwright, "employee");
  const before = await balance(api);
  const start = freshMonday();
  const description = `Corrected leave ${RUN}`;

  await login(page, "employee");
  let form = await openForm(page, "leave");
  await pickSelect2(page, form, "leave_type_id", "Team Annual Leave");
  await form.locator('[name="start_date"]').fill(iso(start));
  // Rejected value: a 5-day request, more than the available balance.
  const tooLong = before + 2;
  await form.locator('[name="end_date"]').fill(iso(addDays(start, tooLong - 1)));
  await form.locator('[name="description"]').fill(description);
  await form.locator("#buttonID").click();

  // The error explains what is wrong (insufficient balance for these dates).
  form = page.locator('form[hx-post^="/leave/leave-request-create/"]');
  const error = page.getByText(/sufficient leave balance/i).first();
  await expect(error).toBeVisible();
  test.info().annotations.push({ type: "error shown", description: (await error.innerText()).trim() });
  // The list endpoint has no description field; the run's start date is unique.
  const onStart = async () => (await (await api.get("/api/leave/user-request/")).json()).results.filter((r) => r.start_date === iso(start));
  expect(await onStart(), "nothing saved after the rejection").toHaveLength(0);

  // Correct the value: a 2-day request within the balance.
  await form.locator('[name="end_date"]').fill(iso(addDays(start, 1)));
  await form.locator("#buttonID").click();
  await expect(page.getByText(/Leave request created successfully/i).first()).toBeVisible();

  const saved = await onStart();
  expect(saved).toHaveLength(1);
  expect(saved[0].end_date).toBe(iso(addDays(start, 1)));
  expect(saved[0].status).toBe("requested");
  await api.dispose();
});
