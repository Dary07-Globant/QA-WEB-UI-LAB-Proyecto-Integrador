"""Clase base del Page Object Model.

Centraliza las interacciones de bajo nivel con Playwright para que las
páginas concretas solo expongan métodos de negocio y locators por data-testid.
"""
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Métodos reutilizables para todas las páginas."""

    def __init__(self, page: Page):
        self.page = page

    # --- Localización por data-testid (estándar del proyecto) ---
    def by_testid(self, testid: str) -> Locator:
        """Devuelve un locator a partir de un atributo data-testid."""
        return self.page.locator(f"[data-testid='{testid}']")

    # --- Acciones ---
    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def click_testid(self, testid: str) -> None:
        self.by_testid(testid).click()

    def fill_testid(self, testid: str, value: str) -> None:
        locator = self.by_testid(testid)
        locator.wait_for(state="visible")
        locator.fill(value)

    # --- Consultas / aserciones de apoyo ---
    def title(self) -> str:
        return self.page.title()

    def is_visible(self, testid: str, timeout: int = 10000) -> bool:
        try:
            self.by_testid(testid).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def expect_visible(self, testid: str) -> None:
        expect(self.by_testid(testid)).to_be_visible()
