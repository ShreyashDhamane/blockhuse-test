from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# SQLite database setup
conn = sqlite3.connect('orders.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                  (id INTEGER PRIMARY KEY, symbol TEXT, price FLOAT, quantity INTEGER, order_type TEXT)''')
conn.commit()

# Pydantic model for order
class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

# POST /orders - Submit a new order
@app.post("/orders")
async def create_order(order: Order):
    cursor.execute("INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
                   (order.symbol, order.price, order.quantity, order.order_type))
    conn.commit()
    return {"message": "Order created successfully"}

# GET /orders - Retrieve all orders
@app.get("/orders", response_model=List[Order])
async def get_orders():
    cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
    orders = cursor.fetchall()
    return [{"symbol": order[0], "price": order[1], "quantity": order[2], "order_type": order[3]} for order in orders]