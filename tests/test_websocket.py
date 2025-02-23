from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_websocket_connection():
    # Test WebSocket connection and message handling
    with client.websocket_connect("/ws/orders") as websocket:
        # Send a message to the WebSocket server
        websocket.send_text("ping")
        
        # Receive a response from the WebSocket server
        data = websocket.receive_text()
        assert data == "pong"

def test_websocket_broadcast():
    """
    Test WebSocket broadcast functionality.
    """
    # Connect two WebSocket clients
    with client.websocket_connect("/ws/orders") as websocket1, \
         client.websocket_connect("/ws/orders") as websocket2:

        # Send a new order to the server (simulate a new order creation)
        response = client.post(
            "/submit-order",  # Correct endpoint for creating orders
            data={"symbol": "AAPL", "price": "150.0", "quantity": "10", "order_type": "buy"},  # Use `data` for form-encoded data
        )
        assert response.status_code == 200  # Ensure the order was created successfully

        # Verify that both WebSocket clients receive the new order
        data1 = websocket1.receive_json()
        data2 = websocket2.receive_json()

        assert data1 == {"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"}
        assert data2 == {"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"}