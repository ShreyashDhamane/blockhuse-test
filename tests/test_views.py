from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_homepage():
    # Test the homepage
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_view_orders():
    # Test the view orders page
    response = client.get("/view-orders")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]