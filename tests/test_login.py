from pages.login_page import LoginPage


def test_login_with_valid_user(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    assert "/inventory.html" in driver.current_url


def test_login_with_locked_out_user(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")

    assert "locked out" in login_page.get_error_text()
    assert "/inventory.html" not in driver.current_url