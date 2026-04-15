import pytest
from demo_ecommerce.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client


# ── PAGE LOAD TESTS ─────────────────────────────────────────────────────────

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_home_alias_page_loads(client):
    response = client.get("/home")
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_signup_page_loads(client):
    response = client.get("/signup")
    assert response.status_code == 200

def test_cart_page_loads(client):
    response = client.get("/cart")
    assert response.status_code == 200

def test_checkout_page_loads(client):
    response = client.get("/checkout")
    assert response.status_code in [200, 302]

def test_contact_page_loads(client):
    response = client.get("/contact")
    assert response.status_code == 200

def test_product_page_valid_id(client):
    response = client.get("/product/1")
    assert response.status_code == 200


# ── LOGIN TESTS ─────────────────────────────────────────────────────────────

def test_login_valid_credentials(client):
    response = client.post("/login", data={
        "username": "user@test.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert b"Login Success" in response.data

def test_login_wrong_password(client):
    response = client.post("/login", data={
        "username": "user@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 200
    assert b"Login Failed" in response.data

def test_login_empty_email(client):
    response = client.post("/login", data={"username": "", "password": "1234"})
    assert response.status_code == 200
    assert b"required" in response.data.lower()

def test_login_invalid_email_format(client):
    response = client.post("/login", data={"username": "notanemail", "password": "1234"})
    assert response.status_code == 200
    assert b"valid email" in response.data.lower()


# ── SIGNUP TESTS ─────────────────────────────────────────────────────────────

def test_signup_valid(client):
    response = client.post("/signup", data={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secure123",
        "confirm_password": "secure123"
    })
    assert response.status_code == 200
    assert b"Account created" in response.data

def test_signup_password_mismatch(client):
    response = client.post("/signup", data={
        "name": "John",
        "email": "john@example.com",
        "password": "abc123",
        "confirm_password": "xyz789"
    })
    assert response.status_code == 200
    assert b"do not match" in response.data.lower()

def test_signup_short_password(client):
    response = client.post("/signup", data={
        "name": "John",
        "email": "john@example.com",
        "password": "ab",
        "confirm_password": "ab"
    })
    assert response.status_code == 200
    assert b"6 characters" in response.data.lower()


# ── SEARCH TESTS ─────────────────────────────────────────────────────────────

def test_search_with_results(client):
    response = client.get("/search?q=MacBook")
    assert response.status_code == 200

def test_search_no_results(client):
    response = client.get("/search?q=ZZZNotExisting")
    assert response.status_code == 200

def test_search_empty_query(client):
    response = client.get("/search?q=")
    assert response.status_code == 200

def test_search_no_param(client):
    response = client.get("/search")
    assert response.status_code == 200


# ── CART TESTS ───────────────────────────────────────────────────────────────

def test_cart_add_valid_product(client):
    response = client.post("/cart/add", data={"product_id": 1, "quantity": 1},
                           follow_redirects=True)
    assert response.status_code == 200

def test_cart_add_invalid_product(client):
    response = client.post("/cart/add", data={"product_id": 9999, "quantity": 1},
                           follow_redirects=True)
    assert response.status_code == 200

def test_cart_remove_item(client):
    # Add first, then remove
    client.post("/cart/add", data={"product_id": 1, "quantity": 1})
    response = client.post("/cart/remove", data={"product_id": 1},
                           follow_redirects=True)
    assert response.status_code == 200


# ── PRODUCT TESTS ─────────────────────────────────────────────────────────────

def test_product_invalid_id_returns_404(client):
    response = client.get("/product/9999")
    assert response.status_code == 404

def test_all_products_accessible(client):
    for pid in range(1, 9):
        response = client.get(f"/product/{pid}")
        assert response.status_code == 200


# ── CONTACT TESTS ─────────────────────────────────────────────────────────────

def test_contact_valid_submission(client):
    response = client.post("/contact", data={
        "name": "Alice",
        "email": "alice@example.com",
        "message": "Hello, I need help."
    })
    assert response.status_code == 200
    assert b"sent" in response.data.lower()

def test_contact_missing_name(client):
    response = client.post("/contact", data={
        "name": "",
        "email": "test@test.com",
        "message": "Test"
    })
    assert response.status_code == 200
    assert b"required" in response.data.lower()
