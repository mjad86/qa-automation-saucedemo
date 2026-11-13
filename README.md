# QA Automation: Sauce Demo

UI test automation framework built with **Python, Pytest and Selenium**, following the **Page Object Model** pattern. It automates the login flow of the [Swag Labs demo store](https://www.saucedemo.com/).

This project is the automation counterpart of my manual QA work: [qa-portfolio-saucedemo](https://github.com/mjad86/qa-portfolio-saucedemo).

## Tech stack

| Tool | Purpose |
|---|---|
| Python | Programming language |
| Pytest | Test runner, fixtures and parametrization |
| Selenium WebDriver | Browser automation (Chrome) |

## Project structure

```
qa-automation-saucedemo/
├── pages/
│   └── login_page.py      # Page Object: locators and actions for the login page
├── tests/
│   ├── conftest.py        # Shared fixtures (browser setup and teardown)
│   └── test_login.py      # Login test cases
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Project dependencies
└── README.md
```

## Design decisions

- **Page Object Model:** locators and page actions live in one class per page, so a UI change means editing a single file instead of every test.
- **Fixtures:** the browser is opened before each test and always closed afterwards, even when the test fails, so no browser windows are left behind.
- **Explicit waits:** elements are awaited with `WebDriverWait` instead of fixed sleeps, which keeps tests stable and avoids flaky results.
- **Parametrized tests:** negative login scenarios share a single test function fed by a data table, so adding a scenario means adding one row.
- **Assertions in tests, not in pages:** page objects only interact with the page; verification stays in the test.

## Test coverage

| Test | Scenario | Expected result |
|---|---|---|
| `test_login_with_valid_user` | Login with `standard_user` | User lands on the inventory page |
| `test_login_rejected[locked_out]` | Login with a locked out user | Error message, no access |
| `test_login_rejected[wrong_password]` | Valid user, wrong password | Error message, no access |
| `test_login_rejected[empty_fields]` | Both fields empty | "Username is required" error |
| `test_login_rejected[empty_password]` | Password empty | "Password is required" error |

## Getting started

### Prerequisites

- Python 3 (developed with 3.15)
- Google Chrome (Selenium downloads the matching driver automatically)

### Setup

```bash
git clone https://github.com/mjad86/qa-automation-saucedemo.git
cd qa-automation-saucedemo

py -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

On macOS or Linux, use `python3 -m venv .venv` and `source .venv/bin/activate` instead.

### Run the tests

```bash
pytest -v
```

Run a single test by name:

```bash
pytest -v -k "valid_user"
```

## Roadmap

- [x] Login tests with Page Object Model
- [x] Parametrized negative scenarios
- [x] Inventory and cart flow (add to cart, verify counter)
- [ ] Checkout flow
- [ ] HTML test reports
- [ ] Continuous integration with GitHub Actions
- [ ] API tests (Postman and Python `requests`)

## Author

**Mauricio**: data analyst with a SQL background, moving into QA and test automation.
