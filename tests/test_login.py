import pytest

from pages.login_page import LoginPage


def test_login_with_valid_user(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    assert "/inventory.html" in driver.current_url


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong_password", "do not match"),
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked_out", "wrong_password", "empty_fields", "empty_password"],
)
def test_login_rejected(driver, username, password, expected_error):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert expected_error in login_page.get_error_text()
    assert "/inventory.html" not in driver.current_url