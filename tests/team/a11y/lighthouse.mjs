// Lighthouse (accessibility, best practices, SEO) on each workflow's key screen
// while logged in (brief §3). Logs in with Playwright to get a real session
// cookie, then runs Lighthouse in Playwright's Chromium with that cookie.
//
//   PHASE=before node lighthouse.mjs      (or PHASE=after)
// Output: docs/team/evidence/a11y/lighthouse-<PHASE>/<screen>.report.{html,json}
import { chromium } from "@playwright/test";
import lighthouse from "lighthouse";
import fs from "node:fs";
import path from "node:path";
import { BASE, login } from "./helpers.mjs";

const PHASE = process.env.PHASE || "before";
const OUT = path.resolve("../../../docs/team/evidence/a11y", `lighthouse-${PHASE}`);
const SCREENS = {
  "allocation-requests": "/leave/leave-allocation-request-view/",
  "my-leave-requests": "/leave/user-request-view/",
};

const browser = await chromium.launch();
const page = await browser.newPage();
await login(page, "employee");
const cookies = await page.context().cookies();
await browser.close();
const cookieHeader = cookies.map((c) => `${c.name}=${c.value}`).join("; ");

// Lighthouse drives Playwright's own Chromium through the DevTools port.
const PORT = 9333;
const chrome = await chromium.launch({ args: [`--remote-debugging-port=${PORT}`] });
fs.mkdirSync(OUT, { recursive: true });
const summary = {};
try {
  for (const [name, route] of Object.entries(SCREENS)) {
    const result = await lighthouse(BASE + route, {
      port: PORT,
      output: ["html", "json"],
      onlyCategories: ["accessibility", "best-practices", "seo"],
      extraHeaders: { Cookie: cookieHeader },
      formFactor: "desktop",
      screenEmulation: { mobile: false, width: 1350, height: 940, deviceScaleFactor: 1, disabled: false },
      logLevel: "error",
    });
    const [html, json] = result.report;
    fs.writeFileSync(path.join(OUT, `${name}.report.html`), html);
    fs.writeFileSync(path.join(OUT, `${name}.report.json`), json);
    const lhr = result.lhr;
    if (new URL(lhr.finalDisplayedUrl).pathname.startsWith("/login")) throw new Error(`${name}: not logged in`);
    const failing = Object.values(lhr.audits)
      .filter((a) => a.score !== null && a.score < 1 && a.scoreDisplayMode !== "informative" && a.scoreDisplayMode !== "manual")
      .map((a) => a.id);
    summary[name] = {
      url: lhr.finalDisplayedUrl,
      accessibility: Math.round(lhr.categories.accessibility.score * 100),
      best_practices: Math.round(lhr.categories["best-practices"].score * 100),
      seo: Math.round(lhr.categories.seo.score * 100),
      failing_audits: failing,
    };
    console.log(name, JSON.stringify(summary[name]));
  }
} finally {
  await chrome.close();
}
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 2));
