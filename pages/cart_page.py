from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.checkout_info_page import CheckoutInfoPage


class CartPage:
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_URL_PART = "cart.html"
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def get_product_names(self):
        # Esperamos por la DIRECCIÓN y no por el título: el título puede cambiar
        # de texto (o existir en otra página), la dirección del carrito no.
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.url_contains(self.CART_URL_PART),
            message="El carrito no terminó de cargar",
        )
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]

    def proceed_to_checkout(self):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON),
            message="El botón Checkout no estaba disponible en el carrito",
        ).click()
        return CheckoutInfoPage(self.driver)