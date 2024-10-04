from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from database.db import Base
import enum


class TransactionType(enum.Enum):
    buy = "buy"
    sell = "sell"


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("USERS.id"))
    ticker_id = Column(Integer, ForeignKey("stocks.id"))
    transaction_type = Column(Enum(TransactionType))  # Using Enum for transaction types
    transaction_volume = Column(Integer)
    transaction_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    stock = relationship("Stock")
