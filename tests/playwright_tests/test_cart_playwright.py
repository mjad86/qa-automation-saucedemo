import re

from playwright.sync_api import Page, expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
T_SHIRT_RED = "Test.allTheThings() T-Shirt (Red)"

CART_LINK = '[data-test="shopping-cart-link"]'
CART_BADGE = '[data-test="shopping-cart-badge"]'
ITEM_NAMES = ".inventory_item_name"


def add_product_to_cart(page: Page, product_name: str):
    # Same idea as in the Selenium page object:
    # "Sauce Labs Backpack" -> "sauce-labs-backpack"
    slug = product_name.lower().replace(" ", "-")

    # DELICATE PART: we use [id="..."] and not "#..." on purpose. Some ids contain
    # characters like "." "(" ")" (the red T-shirt), and in CSS those mean something
    # else, so "#add-to-cart-test.allthethings()..." would not find the button.
    page.locator(f'[id="add-to-cart-{slug}"]').click()

    # The button turns into "Remove" once the product is in the cart
    expect(page.locator(f'[id="remove-{slug}"]')).to_be_visible()


def open_cart(page: Page):
    page.locator(CART_LINK).click()
    expect(page).to_have_url(re.compile(r"cart\.html"))


def test_add_one_product_updates_cart_badge(logged_in_page: Page):
    add_product_to_cart(logged_in_page, BACKPACK)

    expect(logged_in_page.locator(CART_BADGE)).to_have_text("1")


def test_one_added_product_appears_in_cart(logged_in_page: Page):
    add_product_to_cart(logged_in_page, BACKPACK)
    open_cart(logged_in_page)

    # Exact list: only the product we added, nothing else
    expect(logged_in_page.locator(ITEM_NAMES)).to_have_text([BACKPACK])


def test_add_two_products_updates_cart_badge(logged_in_page: Page):
    add_product_to_cart(logged_in_page, BACKPACK)
    add_product_to_cart(logged_in_page, BIKE_LIGHT)

    expect(logged_in_page.locator(CART_BADGE)).to_have_text("2")


def test_two_added_products_appear_in_cart(logged_in_page: Page):
    add_product_to_cart(logged_in_page, BACKPACK)
    add_product_to_cart(logged_in_page, BIKE_LIGHT)
    open_cart(logged_in_page)

    names = logged_in_page.locator(ITEM_NAMES)

    # First wait until exactly 2 items are on the page, then read them.
    # all_text_contents() does NOT wait by itself, so the count check goes first.
    expect(names).to_have_count(2)
    assert sorted(names.all_text_contents()) == sorted([BACKPACK, BIKE_LIGHT])


def test_add_product_with_special_characters_appears_in_cart(logged_in_page: Page):
    add_product_to_cart(logged_in_page, T_SHIRT_RED)
    open_cart(logged_in_page)

    expect(logged_in_page.locator(ITEM_NAMES)).to_have_text([T_SHIRT_RED])