# Usability and Accessibility Evaluation (Area 3)

Carried out by Muhammad Wasay Tariq (24I-3071) as part of the Area 3 work taken over by team agreement. Brief §3: two automated Playwright task tests (one per workflow, one with a rejected value then a correction, one with keyboard navigation), Lighthouse (accessibility, best practices, SEO) and a full axe-core scan of each use case's key screen, every issue counted once with element, user impact and fix, then one screen fixed and both tools re-run before/after. All checks are automated against test accounts; no participants.

## 1. Setup

| Item | Value |
|---|---|
| App | Local Horilla 2.4.0 (`sqe-team` @ `2ceca1ee7`), `runserver`, database restored from the seeded snapshot before each phase |
| Account | Synthetic `team_employee` (logged in for every check) |
| Suite | [`tests/team/a11y/`](../../../tests/team/a11y/): Node, `@playwright/test` 1.65.1 (Chromium), `@axe-core/playwright` 4.14.1, `lighthouse` 13.6.0 |
| Key screens | W1: **Leave Allocation Requests** `/leave/leave-allocation-request-view/` (+ its create form). W2: **My Leave Requests** `/leave/user-request-view/` (+ its create form) |
| Evidence | [`docs/team/evidence/a11y/`](../evidence/a11y/): Playwright HTML reports and JSON results, axe JSON per screen, Lighthouse HTML+JSON per screen, each **before** and **after** the fix |

```powershell
powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1
.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
cd tests\team\a11y ; npm ci ; npx playwright install chromium
$env:PHASE="after"; $env:AXE_STRICT="1"; npx playwright test   # task tests + axe
$env:PHASE="after"; node lighthouse.mjs                          # Lighthouse, logged in
```

## 2. Automated task tests

| Test | Workflow | What it does | Result |
|---|---|---|---|
| [`w1-allocation-keyboard.spec.mjs`](../../../tests/team/a11y/tests/w1-allocation-keyboard.spec.mjs) | W1 | Opens "Create" on the allocation screen, **tabs through the form** from the dialog's first control and records which control has focus after each Tab; asserts the required fields and the submit button are reached **in order** (Leave Type → Requested Days → Description → Save); then fills every field and **submits with Enter on Save, using only the keyboard** (Select2 opened with Enter, option chosen by typing). Asserts the confirmation is shown and the record exists through the API (4 days, `requested`). | **pass** (before and after) |
| [`w2-leave-request-correction.spec.mjs`](../../../tests/team/a11y/tests/w2-leave-request-correction.spec.mjs) | W2 | Grants a 3-day balance (W1 through the API), opens "Create" on My Leave Requests, submits a **5-day request that BR-01 rejects**; asserts the error **"Does not have sufficient leave balance for the requested dates."** is shown and nothing was saved; **corrects** the end date to a 2-day request and asserts "Leave request created successfully" and exactly one saved request with the corrected dates. | **pass** (before and after) |

Observed tab order (W1): Leave Type (Select2) → Requested Days → Attachment → Description → "Save & add another" → Save. Required fields and Save come in the order the form shows them; the optional Attachment sits between two required fields, which matches its visual position.

**Usability findings from the task tests**

| ID | Finding | User impact | Proposed fix |
|---|---|---|---|
| UX-01 | Creating a **new** allocation request shows the confirmation **"Leave allocation request updated"** | The user is told something different from what happened and may think they edited an older request | Show "Leave allocation request created" on create (the create and update paths share one message) |
| UX-02 | A first-visit guided tour (driver.js) covers the page and blocks clicks until dismissed | First-time users must dismiss it before they can act; it does close with **Escape** (keyboard-accessible) | Keep Escape support; add a visible "Skip tour" control and do not show the tour on task screens opened from a link |
| UX-03 | The W2 rejection message explains **what** is wrong (insufficient balance) but not **by how much** | The user has to work out the allowed length themselves | Include the available days in the message, e.g. "You have 3 days available; this request needs 5" |

## 3. Baseline scans (before the fix)

| Screen | Lighthouse Accessibility | Best Practices | SEO | axe rules violated (nodes) | axe critical / serious |
|---|---|---|---|---|---|
| My Leave Requests (list) | **71** | 100 | 82 | 14 (74) | 2 / 7 |
| My Leave Requests (create form) | (part of the page above) | | | 1 (1) | 0 / 1 |
| Leave Allocation Requests (list) | **71** | 100 | 82 | 12 (47) | 2 / 6 |
| Leave Allocation Requests (create form) | (part of the page above) | | | 2 (3) | 0 / 2 |

### Issues found (each counted once)

Lighthouse's accessibility audits are axe-core rules, so an issue reported by both tools is listed once with "both".

| ID | Issue (rule) | Found by | Element(s) | User impact | Proposed fix |
|---|---|---|---|---|---|
| A11Y-01 | Page has no language (`html-has-lang`) | both | `<html>` | Screen readers guess the language and may mispronounce everything | `<html lang="{{ request.LANGUAGE_CODE }}">` |
| A11Y-02 | Buttons without a name (`button-name`), **critical** | both | notifications bell button; "close notifications" button | Screen-reader users hear only "button" and cannot tell what it does | `aria-label` on both buttons |
| A11Y-03 | Low colour contrast (`color-contrast`) | both | white on brand red `#E54F38` (3.81:1): Save/Create buttons, active sidebar item; brand red text on white/grey (breadcrumb, "Select"); grey hints `#9CA3AF` (2.53:1); version text `#999` (2.84:1); attendance clock green on green (2.03:1) | Low-vision users and anyone in bright light cannot read buttons and hints (WCAG 1.4.3 needs 4.5:1) | Use the theme's darker token `--primary-800` `#AC3B2A` (6.15:1 / 5.69:1) and darker greys/green |
| A11Y-04 | Icons announced as unnamed images (`role-img-alt`) | axe | 13 Ionicons (`<ion-icon role="img">`) on the list | Screen readers announce "image" many times with no meaning | Mark decorative icons `aria-hidden="true"` |
| A11Y-05 | Select2 controls without a name (`aria-input-field-name`, `label`), **critical** | both | filter Select2 box and its search field | The filter's purpose is not announced | Give the Select2 elements the label of the underlying `<select>` |
| A11Y-06 | Row checkboxes labelled only by a tooltip (`label-title-only`) | axe | "Select All" / "Select Row" checkboxes | Tooltip text is not reliably announced; touch users never see it | `aria-label` from the title |
| A11Y-07 | Link without a name (`link-name`) | both | Dashboard link in the sidebar (its text is `aria-hidden`) | Announced as an empty link | `aria-label="Dashboard"` on the link |
| A11Y-08 | Link nested inside a button (`nested-interactive`); small tap target (`target-size`) | axe; Lighthouse | theme-toggle `<button>` containing an `<a>` | Two focus stops for one control; the inner link is a tiny target | Remove the inner link; the button carries the name |
| A11Y-09 | No main landmark (`landmark-one-main`, `region`) | both | page body | Screen-reader users cannot jump to the main content | `role="main"` on the content container |
| A11Y-10 | No level-one heading (`page-has-heading-one`) | axe | page | Harder to understand page structure | Make the page title an `<h1>` |
| A11Y-11 | Heading level skipped (`heading-order`) | both | balance card `<h5>` | Heading navigation is confusing | Use the next level (`<h2>`/`<h3>`) |
| A11Y-12 | Alt text repeats visible text (`image-redundant-alt`), minor | axe | "Filter" / "Actions" icons | Text read twice | `alt=""` on those icons |
| A11Y-13 | Dialog without a name (`aria-dialog-name`) | axe | allocation create dialog `#objectCreateModal` | Dialog announced without a title | Point `aria-labelledby` at an existing heading |
| BP-01 | Missing source maps (`valid-source-maps`) | Lighthouse | minified jQuery UI, Chart.js, moment | Developers cannot debug production scripts (no user impact) | Ship `.map` files or unminified sources |
| SEO-01 | No meta description; links not crawlable (`meta-description`, `crawlable-anchors`) | Lighthouse | `<head>`; links with `href="#"`/JS only | None for a logged-in internal app (pages are not indexed) | Accepted: out of scope for an authenticated HR app |

## 4. Fixed screen: My Leave Requests

**Screen fixed:** W2's key screen, **My Leave Requests** (`/leave/user-request-view/`) and its create form. Most issues came from Horilla's shared page layout, so the fix was made in the MIS's own templates:

| Fix | Issues | Change |
|---|---|---|
| `lang` attribute, `role="main"` | A11Y-01, A11Y-09 | `horilla_theme/templates/index.html` |
| Button and link names; no link inside the theme button | A11Y-02, A11Y-07, A11Y-08 | `horilla_theme/templates/horilla_theme/components/header.html`, `.../sidebar/top_menu.html` |
| Contrast (theme token `--primary-800`, darker greys/green) | A11Y-03 | new `horilla_theme/templates/horilla_theme/components/a11y_fixes.html` (CSS) |
| Names for runtime-generated widgets: Ionicons hidden as decorative, Select2 labelled from its `<select>`, title-only checkboxes get `aria-label`; re-applied after each HTMX swap | A11Y-04, A11Y-05, A11Y-06 | same partial (small script; these elements are generated by third-party libraries at runtime) |

Left for later (moderate/minor, structural): A11Y-10, A11Y-11, A11Y-12; A11Y-13 is on the allocation dialog, not the fixed screen.

## 5. Before and after

| Screen | Lighthouse Accessibility | axe rules (nodes) | axe critical / serious |
|---|---|---|---|
| **My Leave Requests (list)**, fixed | **71 → 99** | 14 (74) → **4 (9)** | 2 / 7 → **0 / 0** |
| **My Leave Requests (form)**, fixed | (same page) | 1 (1) → **0 (0)** | 0 / 1 → **0 / 0** |
| Leave Allocation Requests (list) | 71 → 92 (shares the fixed layout) | 12 (47) → 4 (8) | 2 / 6 → 0 / 1 |
| Leave Allocation Requests (form) | (same page) | 2 (3) → 2 (2) | 0 / 2 → 0 / 2 |

Best Practices stayed at 100 and SEO at 82 on both screens (BP-01 and SEO-01 not addressed). The remaining items on the fixed screen are 3 moderate (`heading-order`, `page-has-heading-one`, `region` ×5) and 1 minor (`image-redundant-alt`). On the allocation screen, the remaining serious issues are the dialog name (A11Y-13), the contrast of its "Save & add another" button and tab buttons, and the icon-only row action buttons; they were outside the fixed screen.

**Exit criterion EC-5 (0 critical/serious axe violations on the fixed screen): met.** It is enforced by `AXE_STRICT=1` in `axe-scan.spec.mjs`, which fails the run if a critical or serious violation reappears on either part of the fixed screen. The task tests passed unchanged after the fix (the theme toggle, notifications and forms still work), and the appearance is unchanged apart from the darker red ([`my-leave-requests-after.png`](../evidence/a11y/my-leave-requests-after.png)).

## 6. Links to the risk register

PR-11 (accessibility barriers on the leave forms) was rated Low (L3 × I2). The evidence supports the rating for the forms themselves (the create forms had 1–2 issues) but shows the shared layout around them was in worse shape (two critical issues on every page). The fixed screen now meets EC-5; residual risk is in the moderate structural items and on screens outside the selected workflows.
