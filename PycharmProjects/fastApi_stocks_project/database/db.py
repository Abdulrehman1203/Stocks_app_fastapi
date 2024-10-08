from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config.config import settings
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Allow the session to be used in the endpoint
    finally:
        db.close()
