import pytest
import requests

def test_add_admin():
    response = requests.post("http://localhost:5000/admin", json={"name": "Arda", "password": "1998"})
    assert response.status_code == 200
    print(response.text)
    
def test_menu_add_item():
    headers = {"X-Internal-Key": "supersecret123"}
    response = requests.post("http://localhost:5002/menu", json={"name": "Test Burger", "price": 9.99},headers=headers)
    assert  response.status_code == 200
    assert "name" in response.json()
    print(response.text)

def test_driver_add():
    headers = {"X-Internal-Key": "supersecret123"}
    response = requests.post("http://localhost:5001/driver", json={"name": "Arda"})
    assert response.status_code == 200
    print(response.text)
