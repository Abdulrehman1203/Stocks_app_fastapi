from sqlalchemy import Column, String, Float, Integer
from database.db import Base
from sqlalchemy.orm import relationship



class Stocks(Base):
    """
    A model representing a stock with id, ticker, price, and name.
    """

    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), unique=True, nullable=False)
    stock_price = Column(Float, nullable=False)
    stock_name = Column(String(40))

    class Config:
        from_attributes = True

