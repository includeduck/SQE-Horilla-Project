"""Minimal Python Playwright setup reusing the isolated Area 2 HTTP fixtures."""

import importlib.util
import importlib.metadata
import os
from pathlib import Path

import pytest_asyncio
from playwright.async_api import async_playwright

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("area2_browser_fixtures", TEAM / "api/conftest.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
for name in ("area2_seed", "area2_http", "runtime_cases", "c_context", "leave_http"):
    globals()[name] = getattr(shared, name)


def pytest_terminal_summary(terminalreporter):
    for name in ("Django", "djangorestframework", "pytest", "pytest-django", "requests", "playwright", "pytest-asyncio"):
        terminalreporter.write_line(name + "=" + importlib.metadata.version(name))


@pytest_asyncio.fixture
async def ray_page(leave_http, request):
    # Django's synchronous DB fixtures finish before this event loop begins.
    # Browser operations use Playwright's async API; ORM corroboration in the
    # tests uses sync_to_async. No Django async-safety guard is disabled.
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 1050}, locale="en-US")
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        page.set_default_timeout(20000)
        page.set_default_navigation_timeout(30000)
        assert leave_http.base.startswith("http://localhost:") or leave_http.base.startswith("http://127.0.0.1:")
        yield page
        print("BROWSER_FINAL_URL", page.url)
        print("BROWSER_VISIBLE_TEXT", (await page.locator("body").inner_text())[:2500])
        folder = Path(os.environ.get("AREA2_BROWSER_EVIDENCE", str(TEAM / "browser-results")))
        folder.mkdir(parents=True, exist_ok=True)
        name = request.node.name.replace("[", "-").replace("]", "").replace(":", "-")
        await page.screenshot(path=str(folder / (name + ".png")), full_page=True)
        await context.tracing.stop(path=str(folder / (name + ".zip")))
        await context.close()
        await browser.close()
