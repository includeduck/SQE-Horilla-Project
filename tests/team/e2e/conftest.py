"""Minimal Python Playwright setup reusing the isolated Area 2 HTTP fixtures."""

import importlib.util
import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("area2_browser_fixtures", TEAM / "api/conftest.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
for name in ("area2_seed", "area2_http", "runtime_cases", "c_context", "leave_http"):
    globals()[name] = getattr(shared, name)


@pytest.fixture(scope="session")
def chromium_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def ray_page(chromium_browser, leave_http, request):
    context = chromium_browser.new_context(viewport={"width": 1440, "height": 1050}, locale="en-US")
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.set_default_timeout(20000)
    page.set_default_navigation_timeout(30000)
    # Browser tests target only the disposable loopback Django live server.
    assert leave_http.base.startswith("http://localhost:") or leave_http.base.startswith("http://127.0.0.1:")
    yield page
    folder = Path(os.environ.get("AREA2_BROWSER_EVIDENCE", str(TEAM / "browser-results")))
    folder.mkdir(parents=True, exist_ok=True)
    name = request.node.name.replace("[", "-").replace("]", "").replace(":", "-")
    page.screenshot(path=str(folder / (name + ".png")), full_page=True)
    context.tracing.stop(path=str(folder / (name + ".zip")))
    context.close()
