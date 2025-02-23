from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from database.connection import get_db_cursor
from models.order import Order
from customsocket.manager import manager  # Import the shared manager instance
import json

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
        
        # Broadcast the new order to all WebSocket clients
        new_order = {
            "symbol": order.symbol,
            "price": order.price,
            "quantity": order.quantity,
            "order_type": order.order_type,
        }
        await manager.broadcast(json.dumps(new_order))
        
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
