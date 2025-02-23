from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Literal

class Order(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=5, description="The trading symbol of the asset")
    price: float = Field(..., gt=0, description="The price at which the order should be executed")
    quantity: int = Field(..., gt=0, description="The quantity of the asset to be traded")
    order_type: Literal["buy", "sell"] = Field(..., description="The type of order, either 'buy' or 'sell'")

    @field_validator('symbol')
    def symbol_must_be_uppercase(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError('Symbol must be in uppercase')
        return v

    @field_validator('price')
    def price_must_be_greater_then_0(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Price must have exactly two decimal places')
        return v

    @field_validator('quantity')
    def quantity_must_be_greater_then_0(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Quantity must be a greater than 0')
        return v