import pytest
import requests

# Update if you use different ports
ADMIN_URL = "http://localhost:5000"
MENU_URL = "http://localhost:5002"
DRIVER_URL = "http://localhost:5001"
BOOKING_URL = "http://localhost:5003"
CONFIRM_URL = "http://localhost:5004"

INTERNAL_SECRET = "supersecret123"

@pytest.fixture
def test_driver():
    payload = {"name": "TestDriver", "available": True}
    headers = {"X-Internal-Key": INTERNAL_SECRET}
    res = requests.post(f"{ADMIN_URL}/admin/driver", json=payload, headers=headers)
    assert res.status_code == 200
    return res.json()["driver"]

@pytest.fixture
def test_menu_item():
    payload = {"name": "Pizza", "price": 9.99}
    headers = {"X-Internal-Key": INTERNAL_SECRET}
    res = requests.post(f"{ADMIN_URL}/admin/menu", json=payload, headers=headers)
    assert res.status_code == 200
    return res.json()["item"]

def test_admin_can_add_driver(test_driver):
    assert "id" in test_driver
    assert test_driver["name"] == "TestDriver"

def test_admin_can_add_menu(test_menu_item):
    assert "id" in test_menu_item
    assert test_menu_item["name"] == "Pizza"

def test_booking_interacts_with_driver(test_menu_item, test_driver):
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    items = [{"item_id": test_menu_item["id"], "quantity": 1}]
    preview_res = requests.post(f"{BOOKING_URL}/booking", json={"items": items})
    assert preview_res.status_code == 200

    confirm_res = requests.post(f"{BOOKING_URL}/booking/confirm", json={"items": items}, headers=headers)
    assert confirm_res.status_code == 200
    assert confirm_res.json()["order"]["driver_name"] == test_driver["name"]

def test_confirm_sets_driver_available(test_menu_item, test_driver):
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    items = [{"item_id": test_menu_item["id"], "quantity": 1}]
    confirm_order = requests.post(f"{BOOKING_URL}/booking/confirm", json={"items": items},headers=headers)
    assert confirm_order.status_code == 200

    order_id = confirm_order.json()["order"]["id"]
    res = requests.post(f"{CONFIRM_URL}/confirm", json={"order_id": order_id})
    assert res.status_code == 200
    assert res.json()["driver_status"] == "Available"
