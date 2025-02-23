from fastapi import APIRouter, HTTPException
from database.connection import get_db_cursor
from models.order import Order

router = APIRouter()

# POST /orders - Submit a new order
@router.post("/orders")
async def create_order(order: Order):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (symbol, price, quantity, order_type)
                VALUES (?, ?, ?, ?)
            """, (order.symbol, order.price, order.quantity, order.order_type))
        return {"message": "Order created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# GET /orders - Retrieve all orders
@router.get("/orders", response_model=list[Order])
async def get_orders():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
            orders = cursor.fetchall()
        return [{"symbol": order[0], "price": order[1], "quantity": order[2], "order_type": order[3]} for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")