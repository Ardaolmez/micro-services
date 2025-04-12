from flask import Blueprint, request, jsonify
from models import db, AdminItem
import requests

admin_routes = Blueprint('admin_routes', __name__)
INTERNAL_SECRET = "supersecret123"
DRIVER_SERVICE_URL = 'http://driver:5001'
MENU_SERVICE_URL = 'http://menu:5002'

# --- LOCAL: Admin DB ---
@admin_routes.route('/admin', methods=['POST'])
def create_admin():
    data = request.json
    admin = AdminItem(name=data['name'], password=data['password'])
    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin added", "admin": {"id": admin.id, "name": admin.name}})

@admin_routes.route('/admin', methods=['GET'])
def get_admins():
    admins = AdminItem.query.all()
    return jsonify([{"id": a.id, "name": a.name} for a in admins])

# --- Driver Routes ---
@admin_routes.route('/admin/driver', methods=['POST'])
def add_driver():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response=requests.post(f'{DRIVER_SERVICE_URL}/driver', json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Driver Service unreachable"}), 503

@admin_routes.route('/admin/driver', methods=['GET'])
def get_drivers():
    try:
        response = requests.get(f'{DRIVER_SERVICE_URL}/driver')
        if 'application/json' in response.headers.get('Content-Type', ''):
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"error": "Driver Service returned non-JSON"}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
    
@admin_routes.route('/admin/driver', methods=['PUT'])
def update_driver():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response = requests.put(f'{DRIVER_SERVICE_URL}/driver', json=data, headers=headers)

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"message": "Driver updated", "raw_response": response.text}), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Driver Service unreachable"}), 503


@admin_routes.route('/admin/driver', methods=['DELETE'])
def delete_driver():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response = requests.delete(f'{DRIVER_SERVICE_URL}/driver', json=data, headers=headers)

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"message": "Driver deleted", "raw_response": response.text}), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Driver Service unreachable"}), 503



# --- Menu Routes ---
@admin_routes.route('/admin/menu', methods=['POST'])
def add_menu_item():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response=requests.post(f'{MENU_SERVICE_URL}/menu', json=data, headers=headers)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Menu Service unreachable"}), 503

@admin_routes.route('/admin/menu', methods=['GET'])
def get_menu():
    try:
        response = requests.get(f'{MENU_SERVICE_URL}/menu')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Menu Service unreachable"}), 503
    
@admin_routes.route('/admin/menu', methods=['DELETE'])
def delete_menu_item():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response = requests.delete(f'{MENU_SERVICE_URL}/menu', json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Menu Service unreachable"}), 503
    
@admin_routes.route('/admin/menu', methods=['PUT'])
def update_menu_item():
    data = request.json
    headers = {"X-Internal-Key": INTERNAL_SECRET}

    try:
        response = requests.put(f'{MENU_SERVICE_URL}/menu', json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Menu Service unreachable"}), 503
