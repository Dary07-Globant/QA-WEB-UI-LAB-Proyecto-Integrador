# qa-web-ui-lab

Proyecto de automatización **Web UI** con **Playwright + Python + Page Object Model (POM) + Allure**.

Aplicación bajo prueba: **New Home de Aeroméxico** — `https://dev.amlab7.com/new/es-mx`
Alcance: **flujo de inicio de sesión** (JIRA WEB20-1312 / WEB20-1602). No valida la lógica de voucher.

---

## Estructura del proyecto (POM)

```
qa-web-ui-lab/
├── pages/                     # Page Object Model (una clase por página)
│   ├── base_page.py           # Clase base: acciones comunes y locators por data-testid
│   ├── home_page.py           # New Home: nav bar, apertura del login, contenido
│   └── login_page.py          # Modal de login: campos, submit, reCAPTCHA
├── tests/
│   └── test_login.py          # Pruebas con aserciones de negocio
├── utils/
│   └── config.py              # Lee configuración/credenciales desde .env
├── conftest.py                # Fixtures de Playwright + captura de screenshot en fallos
├── pytest.ini                 # Config de pytest + salida Allure
├── requirements.txt           # Dependencias Python
├── .env                       # Credenciales (NO versionar) — completa LOGIN_PASSWORD
├── .env.example               # Plantilla de variables de entorno
├── run_tests.ps1              # Ejecuta tests + genera y abre el reporte Allure
├── allure-results/            # Resultados crudos (generados por pytest)
└── allure-report/             # Reporte HTML (generado por allure)
```

### Rol de cada archivo

| Archivo | Rol |
|---------|-----|
| `pages/base_page.py` | Encapsula Playwright: `by_testid`, `click_testid`, `fill_testid`, `title`, esperas. Las páginas heredan de aquí. |
| `pages/home_page.py` | Representa el Home. Abre la página, acepta cookies, espera el nav bar y abre el modal de login. |
| `pages/login_page.py` | Representa el modal de login. Locators `data-testid` reales: cuenta, contraseña, submit, reCAPTCHA. Métodos de acción (`login`, `fill_account`...). |
| `tests/test_login.py` | Casos de prueba con aserciones de negocio (título, despliegue del formulario, llenado, login real). |
| `utils/config.py` | Centraliza `BASE_URL`, credenciales, navegador y modo headless desde `.env`. |
| `conftest.py` | Fixtures `browser/context/page` y hook que adjunta screenshot a Allure si un test falla. |

---

## Instalación (ya realizada)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium firefox webkit
```

## Comandos clave

**Ejecutar las pruebas:**
```powershell
.\.venv\Scripts\python.exe -m pytest tests/
```

**Ejecutar solo las pruebas de humo (smoke):**
```powershell
.\.venv\Scripts\python.exe -m pytest -m smoke
```

**Generar el reporte Allure** (usa el JDK portátil incluido en el venv):
```powershell
$env:JAVA_HOME = "$PWD\.venv\Lib\site-packages\jdk4py\java-runtime"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
allure generate allure-results -o allure-report --clean
allure open allure-report
```

**Todo en uno:**
```powershell
.\run_tests.ps1
```

---

## Credenciales

El `.env` ya contiene la cuenta de prueba `LOGIN_ACCOUNT=340281534`.
**Falta completar `LOGIN_PASSWORD`** en el archivo `.env`. Mientras esté vacío, la
prueba de login real (`test_login_exitoso_ve_contenido`) se **omite (skip)**
automáticamente; las pruebas de comportamiento del formulario sí se ejecutan.

## Nota sobre reCAPTCHA

El formulario de login del sitio incluye un widget **reCAPTCHA**
(`data-testid='login-form-recaptcha'`) que puede dejar el botón de envío
deshabilitado hasta resolver el reto. Por eso las pruebas validan el
**comportamiento del formulario** (presencia de campos, llenado, botón visible)
y el login real queda condicionado a credenciales + resolución del reto.
