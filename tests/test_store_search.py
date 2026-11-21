import pytest

from pages.store_home_page import StoreHomePage

SEARCH_TERM = "Jacket"


@pytest.fixture
def store_home_page(driver):
    page = StoreHomePage(driver)
    page.open()
    return page


def test_search_with_enter_returns_results(store_home_page):
    titles = store_home_page.search_with_enter(SEARCH_TERM)

    assert any(SEARCH_TERM.lower() in title.lower() for title in titles)


def test_search_with_magnifier_returns_results(store_home_page):
    titles = store_home_page.search_with_magnifier(SEARCH_TERM)

    assert any(SEARCH_TERM.lower() in title.lower() for title in titles)


# raises=AssertionError: solo cuenta como fallo esperado si falla la
# VERIFICACIÓN; un localizador roto saldría como error real.
# strict=True: si el sitio cambia y la prueba pasa, la suite avisa.
@pytest.mark.xfail(
    raises=AssertionError,
    strict=True,
    reason="BUG-004 (usabilidad): el enlace 'Search' del menú descarta el texto escrito",
)
def test_search_with_menu_link_returns_results(store_home_page):
    titles = store_home_page.search_with_menu_link(SEARCH_TERM)

    assert any(SEARCH_TERM.lower() in title.lower() for title in titles)