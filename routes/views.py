from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from chameleon import PageTemplateFile
from database.connection import get_db_cursor
from customsocket.manager import manager  # Import the shared manager instance
import json

router = APIRouter()

# Homepage route
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    template = PageTemplateFile("templates/index.pt")
    content = template()
    return HTMLResponse(content=content)

# Create Order form route
@router.get("/create-order", response_class=HTMLResponse)
async def create_order_form(request: Request):
    template = PageTemplateFile("templates/create_order.pt")
    content = template()
    return HTMLResponse(content=content)

# Submit Order route (handles form submission)
@router.post("/submit-order")
async def submit_order(
    symbol: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    order_type: str = Form(...),
):
    try:
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
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# View Orders route
@router.get("/view-orders", response_class=HTMLResponse)
async def view_orders(request: Request):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
            orders = cursor.fetchall()
        print("Orders from database:", orders)
        template = PageTemplateFile("templates/view_orders.pt")
        content = template(orders=orders)
        return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
