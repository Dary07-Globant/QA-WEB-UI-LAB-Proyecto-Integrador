"""Carga la configuración del proyecto desde variables de entorno (.env)."""
import os
from dotenv import load_dotenv

# Carga el archivo .env ubicado en la raíz del proyecto
load_dotenv()


class Config:
    """Configuración centralizada leída desde el entorno."""

    BASE_URL: str = os.getenv("BASE_URL", "https://dev.amlab7.com/new/es-mx")
    LOGIN_ACCOUNT: str = os.getenv("LOGIN_ACCOUNT", "")
    LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD", "")
    BROWSER: str = os.getenv("BROWSER", "chromium")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

    @classmethod
    def has_credentials(cls) -> bool:
        """Indica si hay credenciales completas para el login real."""
        return bool(cls.LOGIN_ACCOUNT and cls.LOGIN_PASSWORD)
