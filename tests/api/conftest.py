import pytest

# Single place to change the API address if it ever moves
BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL