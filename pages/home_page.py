"""Page Object del New Home de Aeroméxico (https://dev.amlab7.com/new/es-mx).

Expone el punto de entrada al login y la verificación de contenido del home.
Todos los locators usan data-testid, capturados de la página real.
"""
from pages.base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    """New Home - Booker."""

    # --- Locators (data-testid reales) ---
    BTN_LOGIN = "home-header-session-login"      # Botón "Iniciar sesión" (nav bar)
    PASSENGERS_INPUT = "booker-passengers-input"  # Widget del booker (contenido del home)

    # --- Acciones ---
    def open(self) -> "HomePage":
        """Navega al New Home y prepara la vista (nav bar + cookies).

        El nav bar se renderiza por JS y puede tardar ~10s en una carga en frío,
        por eso esperamos explícitamente a que el botón de login sea visible.
        """
        self.goto(Config.BASE_URL)
        self.by_testid(self.BTN_LOGIN).wait_for(state="visible", timeout=45000)
        self._accept_cookies()
        return self

    def _accept_cookies(self) -> None:
        """Cierra el banner de cookies si está presente (no bloquea si no aparece)."""
        try:
            boton = self.page.get_by_role("button", name="Aceptar")
            boton.wait_for(state="visible", timeout=5000)
            boton.click()
        except Exception:
            pass

    def open_login_modal(self) -> None:
        """Abre el modal de inicio de sesión desde el nav bar."""
        self.click_testid(self.BTN_LOGIN)

    # --- Consultas de negocio ---
    def login_button_visible(self) -> bool:
        """El punto de entrada al login está presente (usuario NO logueado)."""
        return self.is_visible(self.BTN_LOGIN)

    def home_content_visible(self) -> bool:
        """El contenido principal del home (booker) está disponible."""
        return self.is_visible(self.PASSENGERS_INPUT)
