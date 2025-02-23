from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Request, Form
from database.connection import get_db_cursor
from models.order import Order
from customsocket.manager import manager  # Import the shared manager instance
import json
from fastapi.responses import HTMLResponse, RedirectResponse
from chameleon import PageTemplateFile
import re

router = APIRouter()

@router.get("/", response_class=HTMLResponse, summary="Render the Home Page", description="This endpoint loads and renders the `index.pt` template, which contains the homepage content.")
async def homepage(request: Request):
    """
    Render the Home Page.

    This endpoint loads and renders the `index.pt` template, which contains the homepage content.

    Returns:
        HTMLResponse: The rendered HTML page for the homepage.

    Raises:
        HTTPException: If the template file is not found, a 404 status code is returned.
        HTTPException: If there is an unexpected error, a 500 status code is returned with the error details.
    """
    try:
        
        # Load and render the template
        template = PageTemplateFile("templates/index.pt")
        content = template()
        return HTMLResponse(content=content)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Homepage template not found.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Create Order form route
@router.get("/create-order", response_class=HTMLResponse, summary="Render the Create Order form page", description="This endpoint loads and renders the `create_order.pt` template, which contains a form for creating a new order.")
async def create_order_form(request: Request):
    """
    Render the Create Order form page.

    This endpoint loads and renders the `create_order.pt` template, which contains a form for creating a new order.

    Returns:
        HTMLResponse: The rendered HTML page containing the Create Order form.

    Raises:
        HTTPException: If the template file is not found, a 404 status code is returned.
        HTTPException: If there is an unexpected error, a 500 status code is returned with the error details.
    """
    try:
        # Load and render the template
        template = PageTemplateFile("templates/create_order.pt")
        content = template()
        return HTMLResponse(content=content)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Create Order template not found.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Submit Order route (handles form submission)
@router.post("/submit-order", summary="Create a new order", description="Create a new order with the provided details.")
async def submit_order(
    symbol: str = Form(..., description="The stock symbol (e.g., AAPL).", example="AAPL"),
    price: float = Form(..., description="The price per unit.", example=150.00),
    quantity: int = Form(..., description="The number of units.", example=100),
    order_type: str = Form(..., description="The type of order (buy/sell).", example="buy"),
):
    """
    Create a new order with the following details:
    - **symbol**: The stock symbol (e.g., AAPL).
    - **price**: The price per unit.
    - **quantity**: The number of units.
    - **order_type**: The type of order (buy/sell).
    """
    try:
        validate_input(symbol, price, quantity, order_type)
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (symbol, price, quantity, order_type)
                VALUES (?, ?, ?, ?)
            """, (symbol, price, quantity, order_type))
        
        # Broadcast the new order to all WebSocket clients
        new_order = {
            "symbol": symbol,
            "price": price,
            "quantity": quantity,
            "order_type": order_type,
        }
        await manager.broadcast(json.dumps(new_order))
        
        return RedirectResponse(url="/view-orders", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# View Orders route
@router.get("/view-orders", response_class=HTMLResponse, summary="Render the view orders page", description="This endpoint queries the database for all orders and renders them using the `view_orders.pt` template.")
async def view_orders(request: Request):
    """
    Render the view orders page.

    This endpoint queries the database for all orders and renders them using the `view_orders.pt` template.

    Returns:
        HTMLResponse: The rendered HTML page displaying all orders.

    Raises:
        HTTPException: If the template file is not found, a 404 status code is returned.
        HTTPException: If there is a database or rendering error, a 500 status code is returned with the error details.
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
            orders = cursor.fetchall()
        template = PageTemplateFile("templates/view_orders.pt")
        content = template(orders=orders)
        return HTMLResponse(content=content)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Create Order template not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/orders", response_model=list[Order], summary="Retrieve all orders from the database", description="This endpoint queries the database for all orders and returns them as a list of `Order` objects.")
async def get_orders():
    """
    Retrieve all orders from the database.

    This endpoint queries the database for all orders and returns them as a list of `Order` objects.

    Returns:
        List[Order]: A list of orders, where each order contains the following fields:
            - symbol (str): The trading symbol of the asset.
            - price (float): The price at which the order was executed.
            - quantity (int): The quantity of the asset traded.
            - order_type (str): The type of order, either "buy" or "sell".

    Raises:
        HTTPException: If there is a database error, a 500 status code is returned with the error details.
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
            orders = cursor.fetchall()
            
        return [{"symbol": order[0], "price": order[1], "quantity": order[2], "order_type": order[3]} for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# WebSocket endpoint for real-time updates
@router.websocket("/ws/orders")
async def websocket_orders(websocket: WebSocket):
    
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            data = await websocket.receive_text()
            # Optionally handle incoming messages from the client
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

def validate_input(symbol: str, price: float, quantity: int, order_type: str):
    """
    Validates the input fields for creating a new order.

    This function checks the following:
    - The `symbol` must contain only uppercase English alphabets (A-Z) and be 5 characters or less.
    - The `price` must be a positive number greater than 0.
    - The `quantity` must be a positive integer greater than 0.
    - The `order_type` must be either "buy" or "sell".

    Args:
        symbol (str): The trading symbol of the asset.
        price (float): The price at which the order should be executed.
        quantity (int): The quantity of the asset to be traded.
        order_type (str): The type of order, either "buy" or "sell".

    Raises:
        ValueError: If any of the input fields fail validation, a descriptive error message is raised.

    Example:
        >>> validate_input("AAPL", 150.00, 100, "buy")
        # No error raised

        >>> validate_input("aapl", 150.00, 100, "buy")
        ValueError: Symbol must be in uppercase.

        >>> validate_input("AAPL123", 150.00, 100, "buy")
        ValueError: Symbol must be 5 characters or less.

        >>> validate_input("AAPL", -10.00, 100, "buy")
        ValueError: Price must be greater than 0.

        >>> validate_input("AAPL", 150.00, -100, "buy")
        ValueError: Quantity must be greater than 0.

        >>> validate_input("AAPL", 150.00, 100, "invalid")
        ValueError: Order type must be either 'buy' or 'sell'.
    """
    # Validate symbol
    if not re.match(r"^[A-Z]+$", symbol):  # Only English alphabets allowed
        raise ValueError("Symbol must contain only English alphabets (A-Z).")

    if not symbol.isupper():
        raise ValueError("Symbol must be in uppercase.")
    if len(symbol) > 5:
        raise ValueError("Symbol must be 5 characters or less.")
    
    # Validate price
    if price <= 0:
        raise ValueError("Price must be greater than 0.")

    # Validate quantity
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    # Validate order_type
    if order_type not in ["buy", "sell"]:
        raise ValueError("Order type must be either 'buy' or 'sell'.")