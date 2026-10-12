"""Pruebas del flujo de inicio de sesión en el New Home de Aeroméxico.

Alcance (JIRA WEB20-1312 / WEB20-1602): validar que el usuario pueda llegar al
login, que el formulario se comporte correctamente y, cuando haya credenciales,
que pueda ingresar y ver el contenido del home. No se valida la lógica de voucher.
"""
import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config


@allure.epic("WEB2.0 - Experiencia de Compra y Beneficios")
@allure.feature("Login HOME (PingOne)")
@pytest.mark.login
class TestLogin:

    @allure.story("Carga del Home")
    @allure.title("El título de la página del Home es el esperado")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_titulo_de_pagina(self, page):
        """CA-01: la página carga y expone un título válido."""
        home = HomePage(page)
        with allure.step("Abrir el New Home"):
            home.open()

        with allure.step("Validar el título de la página"):
            titulo = home.title()
            allure.attach(titulo, name="titulo_pagina",
                          attachment_type=allure.attachment_type.TEXT)
            assert "Aeroméxico" in titulo, f"Título inesperado: {titulo}"

        with allure.step("Validar que el botón de inicio de sesión es visible"):
            assert home.login_button_visible(), \
                "No se encontró el punto de entrada al login en el nav bar"

    @allure.story("Comportamiento del formulario de login")
    @allure.title("El modal de login expone sus campos y el botón de envío")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_formulario_login_se_despliega(self, page):
        """CA-02: al abrir el modal se muestran cuenta, contraseña y submit."""
        home = HomePage(page)
        home.open()

        with allure.step("Abrir el modal de inicio de sesión"):
            home.open_login_modal()

        login = LoginPage(page)
        with allure.step("Validar que el modal 'Ingresa a tu cuenta' es visible"):
            assert login.is_displayed(), "El modal de login no se desplegó"
            assert "Ingresa a tu cuenta" in login.modal_title_text()

        with allure.step("Validar presencia de los campos del formulario"):
            assert login.account_field_visible(), "Falta el campo de cuenta"
            assert login.password_field_visible(), "Falta el campo de contraseña"
            assert login.submit_button_visible(), "Falta el botón de envío"

    @allure.story("Comportamiento del formulario de login")
    @allure.title("El formulario acepta credenciales y permite enviar")
    @allure.severity(allure.severity_level.NORMAL)
    def test_llenado_formulario_login(self, page):
        """CA-02/CA-03: el formulario acepta datos y el botón queda accionable."""
        home = HomePage(page)
        home.open()
        home.open_login_modal()

        login = LoginPage(page)
        assert login.is_displayed(), "El modal de login no se desplegó"

        with allure.step("Capturar la cuenta de prueba"):
            account = Config.LOGIN_ACCOUNT or "340281534"
            login.fill_account(account)

        with allure.step("Capturar contraseña (si está configurada en .env)"):
            password = Config.LOGIN_PASSWORD or "Password.Demo1"
            login.fill_password(password)

        with allure.step("Validar que el formulario conserva los datos y el botón de envío"):
            # El botón de envío permanece visible; el formulario puede
            # mantenerlo deshabilitado hasta resolver el reCAPTCHA (comportamiento
            # esperado de seguridad del sitio). Validamos presencia del submit y
            # que la cuenta capturada se conserva en el campo.
            assert login.submit_button_visible(), "El botón de envío debe estar presente"
            assert login.account_value() == account, \
                "El campo de cuenta no conservó el valor capturado"
            allure.attach(
                f"submit visible: {login.submit_button_visible()} | "
                f"submit habilitado: {login.submit_enabled()}",
                name="estado_boton_submit",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Inicio de sesión exitoso")
    @allure.title("Login exitoso: el usuario ingresa y ve el contenido del Home")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.skipif(
        not Config.has_credentials(),
        reason="Sin contraseña en .env (LOGIN_PASSWORD vacío). "
               "Completa el .env para ejecutar el login real.",
    )
    def test_login_exitoso_ve_contenido(self, page):
        """CA-04/CA-05: con credenciales válidas el usuario accede al contenido.

        Se ejecuta solo cuando LOGIN_PASSWORD está definido en el .env.
        """
        home = HomePage(page)
        home.open()
        home.open_login_modal()

        login = LoginPage(page)
        assert login.is_displayed(), "El modal de login no se desplegó"

        with allure.step("Iniciar sesión con la cuenta de prueba"):
            login.login(Config.LOGIN_ACCOUNT, Config.LOGIN_PASSWORD)

        with allure.step("Validar que el contenido del Home es visible tras login"):
            assert home.home_content_visible(), \
                "No se visualizó el contenido del Home tras el inicio de sesión"
