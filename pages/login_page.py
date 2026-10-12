"""Page Object del formulario de inicio de sesión (modal).

Representa el modal "Ingresa a tu cuenta" que se abre desde el nav bar del Home.
Locators capturados de la página real por data-testid.

Nota de automatización: el formulario incluye un widget reCAPTCHA
(data-testid='login-form-recaptcha'). En un login real contra el ambiente,
el reto puede impedir la autenticación automatizada; por eso el método
submit() se expone de forma independiente y el test valida el COMPORTAMIENTO
del formulario (presencia, llenado y envío), no la sesión del backend.
"""
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Modal de inicio de sesión."""

    # --- Locators (data-testid reales) ---
    MODAL_TITLE = "login-tabs-title"              # h1 "Ingresa a tu cuenta"
    TAB_LOGIN = "login-tabs-tab-login"            # Pestaña "Iniciar sesión"
    TAB_REGISTER = "login-tabs-tab-register"      # Pestaña "Inscríbete"
    INPUT_ACCOUNT = "login-form-input-account-1"  # Número de cuenta
    INPUT_PASSWORD = "login-form-input-password-2"  # Contraseña
    BTN_SUBMIT = "login-form-button-submit"       # Botón "Iniciar sesión"
    RECAPTCHA = "login-form-recaptcha"            # Widget reCAPTCHA

    # --- Consultas de estado ---
    def is_displayed(self) -> bool:
        """El modal de login está visible."""
        return self.is_visible(self.MODAL_TITLE)

    def modal_title_text(self) -> str:
        """Texto del encabezado del modal."""
        return self.by_testid(self.MODAL_TITLE).inner_text().strip()

    def account_field_visible(self) -> bool:
        return self.is_visible(self.INPUT_ACCOUNT)

    def password_field_visible(self) -> bool:
        return self.is_visible(self.INPUT_PASSWORD)

    def submit_button_visible(self) -> bool:
        return self.is_visible(self.BTN_SUBMIT)

    def submit_enabled(self) -> bool:
        return self.by_testid(self.BTN_SUBMIT).is_enabled()

    def account_value(self) -> str:
        """Valor actual del campo de número de cuenta."""
        return self.by_testid(self.INPUT_ACCOUNT).input_value()

    # --- Acciones ---
    def fill_account(self, account: str) -> None:
        self.fill_testid(self.INPUT_ACCOUNT, account)

    def fill_password(self, password: str) -> None:
        self.fill_testid(self.INPUT_PASSWORD, password)

    def submit(self) -> None:
        self.click_testid(self.BTN_SUBMIT)

    def login(self, account: str, password: str) -> None:
        """Flujo completo de llenado + envío del formulario."""
        self.fill_account(account)
        self.fill_password(password)
        self.submit()
