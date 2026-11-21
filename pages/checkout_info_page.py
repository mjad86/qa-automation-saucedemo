from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInfoPage:
    TIMEOUT = 10

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    def submit(self, first_name, last_name, postal_code):
        # Esperamos a que el formulario esté listo antes de escribir
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT),
            message="El formulario de datos del comprador no apareció",
        )
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

        # PARTE DELICADA: este método devuelve la página de resumen, pero
        # si los datos son inválidos el sitio NO avanza y se queda aquí.
        # Crear el objeto no navega a ningún lado: solo es un "envoltorio".
        # Las pruebas negativas simplemente ignoran lo que devuelve.
        return CheckoutOverviewPage(self.driver)

    def get_error_text(self):
        error = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE),
            message="No apareció el mensaje de error del formulario",
        )
        return error.text