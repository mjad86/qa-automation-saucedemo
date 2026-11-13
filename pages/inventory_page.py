from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.cart_page import CartPage


class InventoryPage:
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        # Los botones tienen un id con el nombre del producto en minúsculas
        # y guiones: "Sauce Labs Backpack" -> "add-to-cart-sauce-labs-backpack"
        slug = product_name.lower().replace(" ", "-")

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, f"add-to-cart-{slug}"))
        ).click()

        # Tras el clic, el botón "Add to cart" se transforma en "Remove". Esperamos ese cambio para saber que la
        # acción terminó antes de que la prueba verifique nada. (relacionado al BUG-006 de la prueba manual)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, f"remove-{slug}"))
        )

    def get_cart_count(self):
        # cuando el carrito está vacío, el contador NO existe
        # en la página. find_element fallaría; find_elements (plural) devuelve
        # una lista vacía, y de ahí inferimos 0.
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.driver.find_element(*self.CART_LINK).click()
        # Navegar a otra página devuelve el Page Object de esa página
        return CartPage(self.driver)