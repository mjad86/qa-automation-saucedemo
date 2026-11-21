import pytest

BACKPACK = "Sauce Labs Backpack"


def test_complete_purchase_with_valid_data(inventory_page):
    inventory_page.add_product_to_cart(BACKPACK)
    cart_page = inventory_page.open_cart()
    info_page = cart_page.proceed_to_checkout()

    overview_page = info_page.submit("Mauricio", "Perez", "6001")
    assert BACKPACK in overview_page.get_product_names()

    complete_page = overview_page.finish()
    assert "Thank you for your order" in complete_page.get_confirmation_text()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Perez", "6001", "First Name is required"),
        ("Mauricio", "", "6001", "Last Name is required"),
        ("Mauricio", "Perez", "", "Postal Code is required"),
    ],
    ids=["empty_first_name", "empty_last_name", "empty_postal_code"],
)
def test_checkout_info_rejected(
    inventory_page, first_name, last_name, postal_code, expected_error
):
    inventory_page.add_product_to_cart(BACKPACK)
    info_page = inventory_page.open_cart().proceed_to_checkout()

    info_page.submit(first_name, last_name, postal_code)

    assert expected_error in info_page.get_error_text()