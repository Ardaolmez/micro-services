# routes.py
from flask import Blueprint, request, jsonify
from models import MenuItem, db

menu_routes = Blueprint('menu_routes', __name__)

@menu_routes.route('/menu', methods=['POST'])
def add_menu():
    if request.headers.get("X-Internal-Key") != "supersecret123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item = MenuItem(name=data['name'], price=data['price'])
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item added", "item": {"id": item.id, "name": item.name, "price": item.price}})

@menu_routes.route('/menu', methods=['DELETE'])
def delete_menu():
    if request.headers.get("X-Internal-Key") != "supersecret123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item_name = data.get('name')

    if not item_name:
        return jsonify({"error": "Missing item name"}), 400

    # Find and delete item
    item = MenuItem.query.filter_by(name=item_name).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": f"Item '{item_name}' deleted"}), 200
@menu_routes.route('/menu', methods=['PUT'])
def update_menu():
    # Security check
    if request.headers.get("X-Internal-Key") != "supersecret123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item_name = data.get('name')           # Current name of the item
    if not item_name:
        return jsonify({"error": "Missing 'name' field"}), 400

    # Find item
    item = MenuItem.query.filter_by(name=item_name).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    new_name = data.get('new_name',item.name)        # New name (optional)
    new_price = data.get('new_price',item.price)      # New price (optional)

    # Update fields if provided
    if new_name:
        item.name = new_name
    if new_price is not None:
        item.price = new_price

    db.session.commit()

    return jsonify({
        "message": "Item updated",
        "item": {"id": item.id, "name": item.name, "price": item.price}
    }), 200

@menu_routes.route('/menu', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([{"id": i.id, "name": i.name, "price": i.price} 
                    for i in items]), 200
