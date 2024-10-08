from pydantic import BaseModel


class StockCreate(BaseModel):
    ticker: str
    stock_name: str
    stock_price: float


class StockResponse(StockCreate):
    id: int

    class Config:
        from_attributes = True
