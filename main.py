from fastapi import FastAPI, Request
from database.connection import init_db
from routes.orders import router as orders_router
from routes.views import router as views_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()

# Initialize the database
init_db()

# Include routers
app.include_router(orders_router)
app.include_router(views_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "detail": str(exc)},
    )

# from pydantic import BaseModel
# from typing import List
# import sqlite3
# from fastapi import FastAPI, Request, HTTPException, Form
# from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from chameleon import PageTemplateFile
# import os

# app = FastAPI()

# # Serve static files from the "static" directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # SQLite database setup
# conn = sqlite3.connect('orders.db', check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS orders
#                   (id INTEGER PRIMARY KEY, symbol TEXT, price FLOAT, quantity INTEGER, order_type TEXT)''')
# conn.commit()

# # Pydantic model for order.
# class Order(BaseModel):
#     symbol: str
#     price: float
#     quantity: int
#     order_type: str

# # POST /orders - Submit a new order
# @app.post("/orders")
# async def create_order(order: Order):
#     cursor.execute("INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
#                    (order.symbol, order.price, order.quantity, order.order_type))
#     conn.commit()
#     return {"message": "Order created successfully"}

# # GET /orders - Retrieve all orders
# @app.get("/orders", response_model=List[Order])
# async def get_orders():
#     cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
#     orders = cursor.fetchall()
#     return [{"symbol": order[0], "price": order[1], "quantity": order[2], "order_type": order[3]} for order in orders]

# @app.get("/", response_class=HTMLResponse)
# async def homepage(request: Request):
#     template = PageTemplateFile("templates/index.pt")
#     content = template()
#     return HTMLResponse(content=content)

# # Submit Order route (handles form submission)
# @app.post("/submit-order")
# async def submit_order(
#     symbol: str = Form(...),
#     price: float = Form(...),
#     quantity: int = Form(...),
#     order_type: str = Form(...),
# ):
#     try:
#         # Insert the order into the database
#         cursor.execute("""
#             INSERT INTO orders (symbol, price, quantity, order_type)
#             VALUES (?, ?, ?, ?)
#         """, (symbol, price, quantity, order_type))
#         conn.commit()
        
#         # Redirect to the view orders page after successful submission
#         return RedirectResponse(url="/view-orders", status_code=303)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Create Order route
# @app.get("/create-order", response_class=HTMLResponse)
# async def create_order(request: Request):
#     template = PageTemplateFile("templates/create_order.pt")
#     content = template()
#     return HTMLResponse(content=content)

# # View Orders route
# @app.get("/view-orders", response_class=HTMLResponse)
# async def view_orders(request: Request):
#     cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
#     orders = cursor.fetchall()
#     template = PageTemplateFile("templates/view_orders.pt")
#     content = template(orders=orders)
#     return HTMLResponse(content=content)