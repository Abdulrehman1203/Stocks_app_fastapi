from sqlalchemy import Column, String, Float, Integer
from database.db import Base


class Users(Base):
    """
    A model representing a stock with ticker, price, and name.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(70), unique=True)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float)

    class Config:
        from_attributes = True
