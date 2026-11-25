from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.cart_page import CartPage


class InventoryPage:
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CART_URL_PART = "cart.html"
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        # Los botones tienen un id con el nombre del producto en minúsculas
        # y guiones: "Sauce Labs Backpack" -> "add-to-cart-sauce-labs-backpack"
        slug = product_name.lower().replace(" ", "-")

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, f"add-to-cart-{slug}"))
        ).click()

        # Tras el clic, el botón "Add to cart" se transforma en "Remove". Esperamos ese cambio para saber que la
        # acción terminó antes de que la prueba verifique nada. (relacionado al BUG-006 de la prueba manual)
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, f"remove-{slug}"))
        )

    def get_cart_count(self):
        # cuando el carrito está vacío, el contador NO existe
        # en la página. find_element fallaría; find_elements (plural) devuelve
        # una lista vacía, y de ahí inferimos 0.
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        # PARTE DELICADA: hacer clic NO significa que la página ya cambió.
        # Guardamos un producto del inventario ANTES del clic; cuando ese elemento
        # desaparece de la página (stale), sabemos que el inventario ya no está.
        inventory_item = self.driver.find_element(*self.ITEM_NAMES)

        self.driver.find_element(*self.CART_LINK).click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.staleness_of(inventory_item),
            message="El inventario no desapareció tras abrir el carrito",
        )
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.url_contains(self.CART_URL_PART),
            message="No se llegó a la página del carrito",
        )

        # Navegar a otra página devuelve el Page Object de esa página
        return CartPage(self.driver)