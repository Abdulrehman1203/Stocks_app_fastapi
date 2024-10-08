from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from common.authentication import get_current_user
from database.db import get_db
from middleware.logs import logger
from models.transaction import Transaction
from models.stock import Stocks
from models.users import Users
from schemas.transaction_schema import Transaction_create, TransactionResponse
from datetime import datetime

router = APIRouter()


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
        transaction: Transaction_create,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    """
    Creates a new transaction (buy/sell stocks), checks balance, updates accordingly.
    """
    if transaction.transaction_volume <= 0:
        raise HTTPException(status_code=404, detail="Volume must be greater than 0")

    if transaction.transaction_type not in ["BUY", "SELL", "sell", "buy"]:
        raise HTTPException(status_code=404, detail="Transaction type must be BUY or SELL")

    stock = db.query(Stocks).filter(Stocks.ticker == transaction.ticker).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Query user by username
    user = db.query(Users).filter(Users.username == transaction.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction_price = stock.stock_price * transaction.transaction_volume

    if transaction.transaction_type == 'BUY' or 'buy':
        if user.balance < transaction_price:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user.balance -= transaction_price
    elif transaction.transaction_type == 'SELL' or 'sell':
        user.balance += transaction_price

    logger.info(f" {transaction.transaction_type} Transaction is created for: {user.username}")

    new_transaction = Transaction(
        user_id=user.id,
        ticker_id=stock.id,
        transaction_price=transaction_price,
        transaction_volume=transaction.transaction_volume,
        transaction_type=transaction.transaction_type
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    response = TransactionResponse(
        id=new_transaction.id,
        transaction_volume=new_transaction.transaction_volume,
        transaction_type=new_transaction.transaction_type,
        transaction_price=new_transaction.transaction_price,
        created_time=new_transaction.created_time,
        username=user.username,
        ticker=stock.ticker
    )

    return response


@router.get("/transactions/user/{username}", response_model=list[TransactionResponse],
            status_code=status.HTTP_200_OK)
async def get_transactions_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    logger.info(f" fetching transactions data for user: {user.username}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    response = []
    for transaction in transactions:
        response.append(TransactionResponse(
            id=transaction.id,
            transaction_volume=transaction.transaction_volume,
            transaction_type=transaction.transaction_type,
            transaction_price=transaction.transaction_price,
            created_time=transaction.created_time,
            username=user.username,
            ticker=transaction.ticker.ticker
        ))

    return response


@router.get("/transactions/{username}/by-date", response_model=list[TransactionResponse],
            status_code=status.HTTP_200_OK)
async def get_transactions_by_time(
        username: str,
        start_time: str,
        end_time: str,
        db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.username == username).first()
    logger.info(f" fetching transactions data for user: {user.username} from {start_time} to {end_time}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        start_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.created_time.between(start_timestamp, end_timestamp)
    ).all()

    return transactions
