import re

from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"


def login(page: Page, username: str, password: str):
    page.goto(LOGIN_URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_with_valid_credentials(page: Page):
    login(page, VALID_USER, PASSWORD)

    # Playwright's expect() retries until the condition is true or times out
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    expect(page.locator('[data-test="title"]')).to_have_text("Products")


def test_login_with_locked_out_user(page: Page):
    login(page, LOCKED_USER, PASSWORD)

    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("locked out")