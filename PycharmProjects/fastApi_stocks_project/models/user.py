from sqlalchemy import Column, Integer, String
from database.db import Base


class User(Base):
    __tablename__ = 'USERS'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String)
    balance = Column(Integer)

    def __repr__(self):
        return f"<User(username={self.username})>"
