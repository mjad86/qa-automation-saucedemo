from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")

    def __init__(self, driver):
        self.driver = driver

    def get_product_names(self):
        # esperamos a que el título de la página sea visible. Así sabemos que el carrito ya cargó antes de leer los productos.
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )
        # LISTA de elementos.
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]