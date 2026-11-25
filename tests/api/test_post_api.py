import requests

# Never call an API without a timeout: a stuck request would freeze the whole run
TIMEOUT_SECONDS = 10

# Same threshold as the Postman tests
MAX_RESPONSE_SECONDS = 2

EXPECTED_POST_FIELDS = {"userId", "id", "title", "body"}
TOTAL_POSTS = 100


def test_get_single_post(base_url):
    response = requests.get(f"{base_url}/posts/1", timeout=TIMEOUT_SECONDS)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < MAX_RESPONSE_SECONDS

    body = response.json()
    assert body["id"] == 1  # we asked for post 1, so it must be post 1
    assert set(body.keys()) == EXPECTED_POST_FIELDS


def test_get_all_posts(base_url):
    response = requests.get(f"{base_url}/posts", timeout=TIMEOUT_SECONDS)

    assert response.status_code == 200

    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == TOTAL_POSTS
    assert set(posts[0].keys()) == EXPECTED_POST_FIELDS


def test_create_post(base_url):
    payload = {
        "title": "QA test post",
        "body": "Created from Pytest",
        "userId": 1,
    }

    response = requests.post(f"{base_url}/posts", json=payload, timeout=TIMEOUT_SECONDS)

    # A POST that creates a resource must return 201, not 200
    assert response.status_code == 201

    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


def test_get_non_existent_post(base_url):
    response = requests.get(f"{base_url}/posts/9999", timeout=TIMEOUT_SECONDS)

    # Negative case: the API must fail correctly, with a 404
    assert response.status_code == 404
    assert response.json() == {}

def test_update_post(base_url):
    payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated from Pytest",
        "userId": 1,
    }

    response = requests.put(f"{base_url}/posts/1", json=payload, timeout=TIMEOUT_SECONDS)

    assert response.status_code == 200

    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["id"] == 1  # we updated post 1, we did not create a new one


def test_delete_post(base_url):
    response = requests.delete(f"{base_url}/posts/1", timeout=TIMEOUT_SECONDS)

    # This API returns 200 with an empty object. Many real APIs return 204 instead.
    assert response.status_code == 200
    assert response.json() == {}