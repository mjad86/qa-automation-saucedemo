# QA Automation: Sauce Demo

![Tests](https://github.com/mjad86/qa-automation-saucedemo/actions/workflows/tests.yml/badge.svg)

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
- [x] Checkout flow
- [x] HTML test reports
- [x] Continuous integration with GitHub Actions
- [x] API tests (Postman and Python `requests`)

## API tests (requests + Pytest)

API tests against the public JSONPlaceholder REST API, kept in `tests/api/`.

| Test | Method | What it validates |
|------|--------|-------------------|
| test_get_single_post | GET | Status 200, response time, exact fields |
| test_get_all_posts | GET | List of 100 posts, structure of each item |
| test_create_post | POST | Status 201, response echoes sent data |
| test_update_post | PUT | Status 200, updated values returned |
| test_delete_post | DELETE | Status 200, empty body |
| test_get_non_existent_post | GET | Negative case: status 404 |

### How to run
```
pip install -r requirements.txt
pytest tests/api -v
```

JSONPlaceholder simulates write operations (POST, PUT, DELETE) and does not persist data.

## Selenium vs Playwright

The same five cart scenarios are automated with both tools
(`tests/test_cart.py` and `tests/playwright_tests/test_cart_playwright.py`).
These are my observations from building both.

### Waiting for the page
In Selenium, clicking the cart link does not mean the page has changed. My cart tests
were flaky because the code read the product list while the inventory page was still
loaded (6 products instead of 2), and sometimes raised `StaleElementReferenceException`.
The fix was explicit waits in `open_cart`: wait for the old element to go stale and
for the URL to contain `cart.html`.

In Playwright the same step is a click plus one assertion on the URL.
`expect(...)` retries until the condition is true or times out, and locators are
resolved again on every action, so stale element errors do not happen.

### Locators
The red T-shirt has an id with dots and parentheses. With Selenium `By.ID` this is
not a problem, but in a Playwright CSS selector `#add-to-cart-test.allthethings()...`
breaks, so I used `[id="..."]` instead.

### Failure information
Selenium: I added `message=` to the waits and a hook in `conftest.py` that saves a
screenshot on failure. Playwright's assertion errors already show what was expected,
what was found and the retries.

### Run time (5 cart tests, headless, 3 runs, my machine)
| Tool | Run 1 | Run 2 | Run 3 | Average |
|------|-------|-------|-------|---------|
| Selenium + Pytest | [65.33s] | [64.27s] | [60.45s] | [63.35s] |
| Playwright + Pytest | [8.08s] | [6.69s] | [5.92s] | [6.89s] |

Small sample on a single machine, including browser startup. Not a benchmark.

### Takeaway
Both tools work. Selenium needed more explicit synchronization code from me;
Playwright handled most of it by default. Knowing the explicit-wait approach
helped me understand what Playwright does automatically.

## Author

**Mauricio**: data analyst with a SQL background, moving into QA and test automation.
