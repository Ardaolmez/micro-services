from flask import Blueprint, request, jsonify
import requests, json
from models import db, BookingItem

booking_routes = Blueprint('booking_routes', __name__)

MENU_SERVICE_URL = "http://menu:5002/menu"
DRIVER_SERVICE_URL = "http://driver:5001/driver"
INTERNAL_SECRET = "supersecret123"

@booking_routes.route('/booking', methods=['POST'])
def preview_booking():
    data = request.json
    items = data.get("items", [])
    order_preview = []
    total = 0.0

    # Fetch all menu items once
    res = requests.get(MENU_SERVICE_URL)
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch menu items"}), 502

    menu_items = res.json()

    for item in items:
        menu_item = next((m for m in menu_items if m["id"] == item["item_id"]), None)
        if not menu_item:
            return jsonify({"error": "Invalid item ID", "item_id": item["item_id"]}), 400

        subtotal = menu_item['price'] * item['quantity']
        order_preview.append({
            "item": menu_item['name'],
            "price": menu_item['price'],
            "quantity": item['quantity'],
            "total": subtotal
        })
        total += subtotal

    return jsonify({
        "order_preview": order_preview,
        "total": round(total, 2),
        "message": "Do you want to confirm this order? Send to /booking/confirm"
    }), 200


@booking_routes.route('/booking/confirm', methods=['POST'])
def confirm_booking():
    data = request.json
    items = data.get("items", [])
    total = 0.0
    resolved_items = []

    # Fetch all menu items once
    res = requests.get(MENU_SERVICE_URL)
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch menu items"}), 502

    menu_items = res.json()

    for item in items:
        menu_item = next((m for m in menu_items if m["id"] == item["item_id"]), None)
        if not menu_item:
            return jsonify({"error": "Invalid item ID", "item_id": item["item_id"]}), 400

        subtotal = menu_item['price'] * item['quantity']
        resolved_items.append({
            "id": item['item_id'],
            "name": menu_item['name'],
            "price": menu_item['price'],
            "quantity": item['quantity'],
            "total": subtotal
        })
        total += subtotal

    # Fetch all drivers
    headers = {"X-Internal-Key": INTERNAL_SECRET}
    res = requests.get(DRIVER_SERVICE_URL, headers=headers)
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch drivers"}), 502

    drivers = res.json()
    available = [d for d in drivers if d['available']]
    if not available:
        return jsonify({"error": "No drivers available"}), 503

    driver = available[0]
    driver_update = {"name": driver['name'], "new_available": False}
    requests.put(DRIVER_SERVICE_URL, json=driver_update, headers=headers)

    booking = BookingItem(
        items=json.dumps(resolved_items),
        total=round(total, 2),
        driver_name=driver['name']
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Order confirmed",
        "order": booking.as_dict()
    }), 201

@booking_routes.route('/booking/<int:order_id>', methods=['GET'])
def get_booking(order_id):
    booking = BookingItem.query.get(order_id)
    if not booking:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(booking.as_dict()), 200