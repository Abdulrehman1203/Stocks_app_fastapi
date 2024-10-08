from sqlalchemy import Column, ForeignKey, String, Float, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class Transaction(Base):
    """
    A model representing a stock transaction.
    """

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticker_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    transaction_type = Column(String(4), nullable=False, default='BUY')
    transaction_volume = Column(Float, nullable=False)
    transaction_price = Column(Float, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("Users")
    ticker = relationship("Stocks")

    class Config:
        from_attributes = True
