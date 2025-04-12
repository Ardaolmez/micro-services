from flask import Blueprint, request, jsonify
from models import DriverItem, db

driver_routes = Blueprint('driver_routes', __name__)

@driver_routes.route('/driver', methods=['POST'])
def add_driver():
        if request.headers.get("X-Internal-Key") != "supersecret123":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.json
        name = data.get('name')
        available = data.get('available', True)  # 👈 this uses the default

        if not name:
            return jsonify({"error": "Missing driver name"}), 400

        driver = DriverItem(name=name, available=available)
        db.session.add(driver)
        db.session.commit()

        return jsonify({"message": "Driver added", "driver": {"id": driver.id, "name": driver.name}})

@driver_routes.route('/driver', methods=['GET'])
def get_driver():
    drivers = DriverItem.query.all()
    return jsonify([
        {"id": d.id, "name": d.name, "available": d.available}
        for d in drivers
    ]), 200
@driver_routes.route('/driver', methods=['DELETE'])
def delete_menu():
    if request.headers.get("X-Internal-Key") != "supersecret123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item_name = data.get('name')

    if not item_name:
        return jsonify({"error": "Missing item name"}), 400

    # Find and delete item
    item = DriverItem.query.filter_by(name=item_name).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": f"Item '{item_name}' deleted"}), 200
@driver_routes.route('/driver', methods=['PUT'])
def update_menu():
    # Security check
    if request.headers.get("X-Internal-Key") != "supersecret123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    driver_name = data.get('name')           
    if not driver_name:
        return jsonify({"error": "Missing 'name' field"}), 400

    # Find item
    driver = DriverItem.query.filter_by(name=driver_name).first()
    if not driver:
        return jsonify({"error": "Item not found"}), 404
    new_name = data.get('new_name', driver.name)  # 👈 this uses the default
    new_available = data.get('new_available',driver.available)     

    # Update fields if provided
    if new_name:
        driver.name = new_name
    if new_available is not None:
        driver.available = new_available

    db.session.commit()

    return jsonify({
        "message": "Item updated",
        "item": {"id": driver.id, "name": driver.name, "available": driver.available}
    }), 200
