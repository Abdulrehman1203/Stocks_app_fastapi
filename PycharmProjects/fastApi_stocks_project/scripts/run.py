from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from common.authentication import verify_password, create_access_token
from database.db import get_db
from models.users import Users
from routes import user_routes, stock_routes, transaction_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(stock_routes.router)
app.include_router(transaction_routes.router)


