from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    buy = 'buy'
    sell = 'sell'


class TransactionCreate(BaseModel):
    user_id: int
    ticker_id: int
    transaction_type: TransactionType  # Use the Enum here
    transaction_volume: int


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    ticker_id: int
    transaction_type: TransactionType  # Use the Enum here
    transaction_volume: int
    transaction_price: float
    created_at: datetime

    class Config:
        from_attributes = True  # No need to change this part
