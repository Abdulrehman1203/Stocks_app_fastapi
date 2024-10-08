from pydantic import BaseModel, Field
from datetime import datetime


class Transaction_create(BaseModel):
    username: str
    ticker: str
    transaction_volume: int
    transaction_type: str


class TransactionResponse(BaseModel):
    id: int
    transaction_volume: float
    transaction_type: str
    transaction_price: float
    created_time: datetime
    username: str
    ticker: str

    class Config:
        from_attributes = True
