from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"


def test_login_with_valid_user(driver): 
    # 1. Abrir la página
    driver.get(BASE_URL)

    # 2. Escribir usuario y contraseña
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    # 3. Hacer clic en Login
    driver.find_element(By.ID, "login-button").click()

    # 4. Verificar el resultado esperado
    assert "/inventory.html" in driver.current_url

def test_login_with_locked_out_user(driver):
    # 1. Abrir la página
    driver.get(BASE_URL)

    # 2. Escribir usuario bloqueado y contraseña
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    # 3. Hacer clic en Login
    driver.find_element(By.ID, "login-button").click()

    # 4. Verificar el resultado esperado
    error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "locked out" in error.text
    assert "/inventory.html" not in driver.current_url