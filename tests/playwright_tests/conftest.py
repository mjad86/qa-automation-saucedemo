import re

import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def logged_in_page(page: Page):
    # Precondition for the cart tests: user already logged in.
    # It uses Playwright's built-in "page" fixture; pytest chains them by name.
    page.goto(LOGIN_URL)
    page.locator('[data-test="username"]').fill(VALID_USER)
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()

    # Wait until we are really on the inventory page before the test starts
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    return page