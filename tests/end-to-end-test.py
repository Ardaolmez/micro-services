import requests

ADMIN_URL = "http://localhost:5000"
MENU_URL = "http://localhost:5002"
DRIVER_URL = "http://localhost:5001"
BOOKING_URL = "http://localhost:5003"
CONFIRM_URL = "http://localhost:5004"

INTERNAL_SECRET = "supersecret123"


def test_full_order_flow():
    # Step 1: Add Menu Item via Admin
    menu_res = requests.post(
        f"{ADMIN_URL}/admin/menu",
        json={"name": "Taco", "price": 7.5},
        headers={"X-Internal-Key": INTERNAL_SECRET}
    )
    assert menu_res.status_code == 200
    item_id = menu_res.json()["item"]["id"]

    # Step 2: Add Driver via Admin
    driver_res = requests.post(
        f"{ADMIN_URL}/admin/driver",
        json={"name": "Test"},
        headers={"X-Internal-Key": INTERNAL_SECRET}
    )
    assert driver_res.status_code == 200

    # Step 3: Preview Booking
    preview_res = requests.post(
        f"{BOOKING_URL}/booking",
        json={"items": [{"item_id": item_id, "quantity": 1}]}
    )
    assert preview_res.status_code == 200

    # Step 4: Confirm Booking
    confirm_res = requests.post(
        f"{BOOKING_URL}/booking/confirm",
        json={"items": [{"item_id": item_id, "quantity": 1}]},
        headers={"X-Internal-Key": INTERNAL_SECRET}
    )
    assert confirm_res.status_code == 201
    booking_data = confirm_res.json()["order"]
    assert "id" in booking_data
    order_id = booking_data["id"]

    # Step 5: Confirm Pickup
    pickup_res = requests.post(
        f"{CONFIRM_URL}/confirm",
        json={"order_id": order_id},
        headers={"X-Internal-Key": INTERNAL_SECRET}
    )
    assert pickup_res.status_code == 200
    assert pickup_res.json()["driver_status"] == "Available"
