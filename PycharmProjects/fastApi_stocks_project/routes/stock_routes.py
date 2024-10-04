from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.stock import Stock
from schemas.stock_schema import StockCreate, StockResponse

router = APIRouter()


# Add a new stock
@router.post("/stock/", response_model=StockResponse)
def add_stock(stock_data: StockCreate, db: Session = Depends(get_db)):
    existing_stock = db.query(Stock).filter(Stock.ticker == stock_data.ticker).first()
    if existing_stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock already exists")

    new_stock = Stock(ticker=stock_data.ticker, price=stock_data.price)
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


# Get stock details by ticker
@router.get("/stock/{ticker}/", response_model=StockResponse)
def get_stock(ticker: str, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.ticker == ticker).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock


# Update stock price
@router.put("/stock/{ticker}/", response_model=StockResponse)
def update_stock_price(ticker: str, price: float, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.ticker == ticker).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

    stock.price = price
    db.commit()
    db.refresh(stock)
    return stock
