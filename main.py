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

