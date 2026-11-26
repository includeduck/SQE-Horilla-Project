// Full axe-core scan (brief §3) of each workflow's key screens: the listing
// page and the open create form. Results are written as JSON evidence under
// docs/team/evidence/a11y/axe-<PHASE>/ (PHASE=before|after).
// With AXE_STRICT=1 the fixed screen (list + form) must have no critical/serious violations.
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs";
import path from "node:path";
import { login, openScreen, openForm } from "../helpers.mjs";

const PHASE = process.env.PHASE || "before";
const OUT = path.resolve("../../../docs/team/evidence/a11y", `axe-${PHASE}`);
// The screen fixed in this project (see ACCESSIBILITY_TESTING.md).
const FIXED_SCREENS = ["leave-request-list", "leave-request-form"]; // "My Leave Requests" and its form

const SCREENS = [
  { id: "allocation-list", kind: "allocation", form: false },
  { id: "allocation-form", kind: "allocation", form: true },
  { id: "leave-request-list", kind: "leave", form: false },
  { id: "leave-request-form", kind: "leave", form: true },
];

for (const screen of SCREENS) {
  test(`axe: ${screen.id}`, async ({ page }) => {
    await login(page, "employee");
    if (screen.form) await openForm(page, screen.kind);
    else await openScreen(page, screen.kind);
    const builder = new AxeBuilder({ page });
    if (screen.form) builder.include(".oh-modal--show, #genericModal"); // the open form dialog
    const results = await builder.analyze();
    fs.mkdirSync(OUT, { recursive: true });
    fs.writeFileSync(path.join(OUT, `${screen.id}.json`), JSON.stringify(results, null, 2));
    const summary = results.violations.map((v) => `${v.impact} ${v.id} (${v.nodes.length})`);
    test.info().annotations.push({ type: "violations", description: summary.join("; ") || "none" });
    if (process.env.AXE_STRICT && FIXED_SCREENS.includes(screen.id)) {
      const severe = results.violations.filter((v) => ["critical", "serious"].includes(v.impact));
      expect(severe.map((v) => v.id)).toEqual([]);
    }
  });
}
