from fastapi.testclient import TestClient
from main import app  # Replace `main` with the actual module name where your FastAPI app is defined

# Create a test client
client = TestClient(app)

def test_create_order():
    """
    Test creating a new order.
    """
    # Test creating a new order with form data
    response = client.post(
        "/submit-order",
        data={"symbol": "AAPL", "price": "150.0", "quantity": "10", "order_type": "buy"},
    )
    # Check if the response status code is 303 (Redirect) or 200 (Success)
    assert response.status_code in [200, 303]

def test_get_orders():
    """
    Test retrieving all orders.
    """
    # Test retrieving all orders
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)