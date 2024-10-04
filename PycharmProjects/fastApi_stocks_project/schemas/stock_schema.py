from pydantic import BaseModel


class StockCreate(BaseModel):
    ticker: str
    price: float


class StockResponse(BaseModel):
    id: int
    ticker: str
    price: float

    class Config:
        from_attributes = True

