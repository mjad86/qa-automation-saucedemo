from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StoreHomePage:
    URL = "https://sauce-demo.myshopify.com/"
    TIMEOUT = 10

    SEARCH_INPUT = (By.ID, "search-field")
    # La lupa: <input type="submit" id="search-submit">, sin texto
    SEARCH_MAGNIFIER = (By.ID, "search-submit")
    # El enlace "Search" del menú superior. Es el primer enlace con ese texto
    # en la portada (VERIFICAR si algún día aparece otro antes en la página)
    SEARCH_MENU_LINK = (By.LINK_TEXT, "Search")
    # Los títulos son <h3> dentro de la cuadrícula de productos
    RESULT_TITLES = (By.CSS_SELECTOR, "section.product-grid h3")
    # Cubre los dos mensajes que puede mostrar el sitio sin resultados
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), 'No search results')"
        " or contains(text(), 'No search performed')]",
    )

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def _type_search_term(self, term):
        search_input = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT),
            message="No apareció el campo de búsqueda",
        )
        search_input.send_keys(term)
        return search_input

    def search_with_enter(self, term):
        search_input = self._type_search_term(term)
        old_url = self.driver.current_url
        search_input.send_keys(Keys.ENTER)
        return self._read_results_after_navigation(old_url)

    def search_with_magnifier(self, term):
        return self._search_by_clicking(term, self.SEARCH_MAGNIFIER)

    def search_with_menu_link(self, term):
        return self._search_by_clicking(term, self.SEARCH_MENU_LINK)

    def _search_by_clicking(self, term, locator):
        # PARTE DELICADA: ambas formas comparten el mismo recorrido y solo
        # cambia QUÉ se pulsa. Un método interno evita duplicar el código.
        self._type_search_term(term)
        old_url = self.driver.current_url
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(locator),
            message=f"El control {locator} no estaba disponible",
        ).click()
        return self._read_results_after_navigation(old_url)

    def _titles_loaded(self, driver):
        # True cuando hay títulos Y todos tienen texto visible.
        # Los productos aparecen con una animación: mientras son
        # transparentes, Selenium devuelve texto vacío.
        titles = driver.find_elements(*self.RESULT_TITLES)
        return bool(titles) and all(t.text.strip() for t in titles)

    def _read_results_after_navigation(self, old_url):
        # PARTE DELICADA, paso 1: esperar a SALIR de la página anterior.
        # Sin esto podríamos leer los productos de la portada.
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.url_changes(old_url),
            message="La búsqueda no navegó a la página de resultados",
        )
        # Paso 2: esperar títulos con texto, o el mensaje de "sin resultados"
        WebDriverWait(self.driver, self.TIMEOUT).until(
            lambda d: self._titles_loaded(d)
            or d.find_elements(*self.NO_RESULTS_MESSAGE),
            message="La página de búsqueda no mostró resultados ni mensaje",
        )
        return [t.text for t in self.driver.find_elements(*self.RESULT_TITLES)]