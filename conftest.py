"""Fixtures compartidas de Playwright + Allure para toda la suite."""
import allure
import pytest
from playwright.sync_api import sync_playwright, Page

from utils.config import Config


@pytest.fixture(scope="session")
def playwright_instance():
    """Arranca y detiene Playwright una vez por sesión de pruebas."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture()
def browser(playwright_instance):
    """Lanza el navegador configurado (chromium/firefox/webkit)."""
    browser_type = getattr(playwright_instance, Config.BROWSER)
    browser = browser_type.launch(headless=Config.HEADLESS)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser):
    """Crea un contexto aislado por test (cookies/almacenamiento limpios)."""
    context = browser.new_context(
        viewport={"width": 1366, "height": 900},
        locale="es-MX",
    )
    yield context
    context.close()


@pytest.fixture()
def page(context) -> Page:
    """Entrega una página nueva por test."""
    page = context.new_page()
    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adjunta screenshot a Allure cuando un test falla."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="screenshot_fallo",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
