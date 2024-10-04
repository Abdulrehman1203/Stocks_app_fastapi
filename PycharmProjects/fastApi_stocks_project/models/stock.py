from sqlalchemy import Column, Integer, String, Float
from database.db import Base


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), unique=True, index=True)
    price = Column(Float)

    def __repr__(self):
        return f"<Stock(ticker={self.ticker})>"
