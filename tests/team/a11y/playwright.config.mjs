// Area 3 usability/accessibility suite. Needs Horilla running on the seeded
// snapshot at HORILLA_URL (default http://localhost:8000).
import { defineConfig } from "@playwright/test";

const PHASE = process.env.PHASE || "before";

export default defineConfig({
  testDir: "./tests",
  workers: 1, // the tests share one seeded database
  fullyParallel: false,
  timeout: 90_000,
  reporter: [
    ["list"],
    ["html", { outputFolder: `../../../docs/team/evidence/a11y/playwright-report-${PHASE}`, open: "never" }],
    ["json", { outputFile: `../../../docs/team/evidence/a11y/playwright-results-${PHASE}.json` }],
  ],
  use: {
    browserName: "chromium",
    viewport: { width: 1280, height: 800 },
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  outputDir: "./test-results",
});
