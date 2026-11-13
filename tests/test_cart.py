def test_add_product_updates_cart_badge(inventory_page):
    inventory_page.add_product_to_cart("Sauce Labs Backpack")

    assert inventory_page.get_cart_count() == 1


def test_added_product_appears_in_cart(inventory_page):
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    cart_page = inventory_page.open_cart()

    assert "Sauce Labs Backpack" in cart_page.get_product_names()