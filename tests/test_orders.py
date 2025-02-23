from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_create_order():
    # Test creating a new order
    response = client.post(
        "/orders",
        json={"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Order created successfully"}

def test_get_orders():
    # Test retrieving all orders
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)