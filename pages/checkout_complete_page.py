from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutCompletePage:
    TIMEOUT = 10

    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def __init__(self, driver):
        self.driver = driver

    def get_confirmation_text(self):
        header = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.COMPLETE_HEADER),
            message="No apareció el mensaje de confirmación de la compra",
        )
        return header.text