from fastapi import FastAPI, Request
from database.connection import init_db
# from routes.views import router as views_router
from routes.views import router as order_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Blockhouse API",
        version="1.0.0",
        description="API's for orders",
        routes=app.routes,
    )
    openapi_schema["paths"]["/ws/orders"] = {
        "get": {
            "summary": "WebSocket connection",
            "description": """"
    Provides information about the WebSocket endpoint for real-time order updates.

    **WebSocket URL**: `ws://ec2-54-208-250-172.compute-1.amazonaws.com/ws/orders`

    **Behavior**:
    - Clients can connect to this endpoint to receive real-time updates about new orders.
    - Clients can send `"ping"` messages to keep the connection alive, and the server will respond with `"pong"`.
    - The server broadcasts new order details to all connected clients in JSON format.

    **Example Message**:
    ```json
    {
        "symbol": "AAPL",
        "price": 150.00,
        "quantity": 100,
        "order_type": "buy"
    }
    ```
    """,
            "responses": {
                "101": {
                    "description": "Switching Protocols - The client is switching protocols as requested by the server.",
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Initialize the database
init_db()

# Include routers
app.include_router(order_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/error")
async def error_page(request: Request):
    error_message = request.query_params.get("error", "An unknown error occurred.")
    return HTMLResponse(content=f"""
        <html>
            <body>
                <h1>Error</h1>
                <p>{error_message}</p>
                <a href="/">Go back to the homepage</a>
            </body>
        </html>
    """)
