from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage:
    TIMEOUT = 10

    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        self.driver = driver

    def get_product_names(self):
        # Esperamos a que haya al menos un producto visible antes de leer
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.ITEM_NAMES),
            message="El resumen de la compra no mostró productos",
        )
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]

    def finish(self):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.FINISH_BUTTON),
            message="El botón Finish no estaba disponible",
        ).click()
        return CheckoutCompletePage(self.driver)