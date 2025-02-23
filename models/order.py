from pydantic import BaseModel

class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str