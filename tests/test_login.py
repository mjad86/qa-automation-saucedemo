from selenium.webdriver.common.by import By

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