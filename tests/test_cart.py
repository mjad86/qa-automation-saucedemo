# Constantes: el nombre de cada producto se escribe UNA sola vez.
# Así un error de tipeo se corrige en un lugar y no en cada prueba.
BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
T_SHIRT_RED = "Test.allTheThings() T-Shirt (Red)"


def test_add_one_product_updates_cart_badge(inventory_page):
    inventory_page.add_product_to_cart(BACKPACK)

    assert inventory_page.get_cart_count() == 1


def test_one_added_product_appears_in_cart(inventory_page):
    inventory_page.add_product_to_cart(BACKPACK)
    cart_page = inventory_page.open_cart()

    assert BACKPACK in cart_page.get_product_names()


def test_add_two_products_updates_cart_badge(inventory_page):
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.add_product_to_cart(BIKE_LIGHT)

    assert inventory_page.get_cart_count() == 2


def test_two_added_products_appear_in_cart(inventory_page):
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.add_product_to_cart(BIKE_LIGHT)
    cart_page = inventory_page.open_cart()

    # PARTE DELICADA: comparamos las listas completas, ordenadas.
    # Esto verifica que estén EXACTAMENTE estos dos productos,
    # sin importar el orden y sin que sobre ninguno.
    product_names = cart_page.get_product_names()
    assert sorted(product_names) == sorted([BACKPACK, BIKE_LIGHT])

def test_add_product_with_special_characters_appears_in_cart(inventory_page):
    inventory_page.add_product_to_cart(T_SHIRT_RED)
    cart_page = inventory_page.open_cart()

    assert T_SHIRT_RED in cart_page.get_product_names()