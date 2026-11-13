import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def driver():
    # Se ejecuta ANTES de cada prueba: abre Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 'yield' entrega el navegador a la prueba y pausa aquí
    yield driver

    # PARTE DELICADA: esto se ejecuta DESPUÉS de la prueba,
    # aunque la prueba haya fallado. Así nunca quedan navegadores abiertos.
    driver.quit()


@pytest.fixture
def inventory_page(driver):
    # Precondición de las pruebas del carrito: usuario ya logueado.
    # Esta fixture usa la fixture "driver": Pytest las encadena solo.
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    return InventoryPage(driver)