# Script de conveniencia: ejecuta las pruebas y genera + abre el reporte Allure.
# Uso:  .\run_tests.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

# 1) Activar entorno virtual
& "$root\.venv\Scripts\python.exe" -m pytest tests/

# 2) Configurar Java portátil (jdk4py) para Allure
$env:JAVA_HOME = "$root\.venv\Lib\site-packages\jdk4py\java-runtime"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

# 3) Generar el reporte HTML
allure generate allure-results -o allure-report --clean

# 4) Abrir el reporte en el navegador
allure open allure-report
