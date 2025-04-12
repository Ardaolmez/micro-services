from flask import Blueprint, request, jsonify
import requests

confirm_routes = Blueprint('confirm_routes', __name__)

BOOKING_SERVICE_URL = "http://booking:5003/booking"
INTERNAL_SECRET = "supersecret123"

@confirm_routes.route('/confirm', methods=['POST'])
def confirm_pickup():
    data = request.json
    order_id = data.get("order_id")

    if not order_id:
        return jsonify({"error": "Missing order_id"}), 400

    # Step 1: Get booking info from Booking Service
    try:
        res = requests.get(f"{BOOKING_SERVICE_URL}/{order_id}")  # ✅ FIXED
        res.raise_for_status()
        booking = res.json()
    except requests.exceptions.RequestException:
        return jsonify({"error": "The order_id is not valid"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from Booking Service"}), 502

    driver_name = booking.get("driver_name")
    if not driver_name:
        return jsonify({"error": "Driver name missing from booking"}), 500

    # Step 2: Make driver available again
    headers = {"X-Internal-Key": INTERNAL_SECRET}
    driver_update = {"name": driver_name, "new_available": True}
    res = requests.put("http://driver:5001/driver", json=driver_update, headers=headers)

    if res.status_code != 200:
        return jsonify({"warning": "Driver update failed", "driver": driver_name}), 200

    return jsonify({
        "message": "Pickup confirmed",
        "order_id": order_id,
        "driver": driver_name,
        "driver_status": "Available"
    }), 200

