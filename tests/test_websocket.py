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
    # Test WebSocket broadcast functionality
    with client.websocket_connect("/ws/orders") as websocket1, \
         client.websocket_connect("/ws/orders") as websocket2:
        
        # Send a new order to the server (simulate a new order creation)
        response = client.post(
            "/orders",
            json={"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"},
        )
        assert response.status_code == 200
        
        # Verify that both WebSocket clients receive the new order
        data1 = websocket1.receive_text()
        data2 = websocket2.receive_text()
        
        # Parse the received data as JSON
        import json
        order1 = json.loads(data1)
        order2 = json.loads(data2)
        
        # Verify the order details
        assert order1 == {"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"}
        assert order2 == {"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"}