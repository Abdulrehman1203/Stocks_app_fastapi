# tasks.py
from celery import Celery
from sqlalchemy.orm import sessionmaker
from database.db import engine
from models.stock import Stocks

celery = Celery('tasks', broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

celery.conf.update(
    task_time_limit=3
)


@celery.task
def fetch_all_stocks():
    db = SessionLocal()
    try:
        stocks = db.query(Stocks).all()
        print(f"Fetched {len(stocks)} stocks")
        return [{"ticker": stock.ticker, "stock_name": stock.stock_name, "stock_price": stock.stock_price} for stock in
                stocks]
    finally:
        db.close()
