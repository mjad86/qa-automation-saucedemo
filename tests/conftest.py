import os
import re
from datetime import datetime
from pathlib import Path

import pytest_html
import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    # Preferencias que apagan el aviso de contraseñas filtradas
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)

    headless = os.getenv("HEADLESS") == "1"
    if headless:
        options.add_argument("--headless=new")
        # Sin ventana, "maximizar" no existe: fijamos un tamaño explícito
        options.add_argument("--window-size=1920,1080")
        # Estos dos evitan fallos típicos de Chrome dentro de servidores Linux
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    if not headless:
        driver.maximize_window()

    yield driver

    driver.quit()

@pytest.fixture
def inventory_page(driver):
    # Precondición de las pruebas del carrito: usuario ya logueado.
    # Esta fixture usa la fixture "driver": Pytest las encadena solo.
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    return InventoryPage(driver)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    #  Se captura AQUÍ porque el navegador todavía está abierto: la fixture lo cierra después.
    if report.when in ("setup", "call") and report.failed:
        driver = item.funcargs.get("driver")
        if driver is None:
            return

        # Los nombres traen corchetes que no sirven en un nombre
        # de archivo. Los cambiamos por guiones bajos.
        safe_name = re.sub(r"[^\w\-]", "_", item.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1) Guardar la captura como archivo en la carpeta screenshots/
        folder = Path("screenshots")
        folder.mkdir(exist_ok=True)
        driver.save_screenshot(str(folder / f"{safe_name}_{timestamp}.png"))

        # 2) Adjuntarla también dentro del reporte HTML
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(driver.get_screenshot_as_base64()))
        report.extras = extras