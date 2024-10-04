from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.transaction import Transaction
from models.user import User
from models.stock import Stock

from schemas.transaction_schema import TransactionCreate, TransactionResponse

router = APIRouter()


# Create a new transaction
@router.post("/transaction/", response_model=TransactionResponse)
def create_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == transaction_data.user_id).first()
    stock = db.query(Stock).filter(Stock.id == transaction_data.ticker_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

    # Example logic: If the user is buying, ensure they have enough balance
    if transaction_data.transaction_type == "BUY":
        total_cost = transaction_data.transaction_volume * stock.price
        if user.balance < total_cost:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

        user.balance -= total_cost
    else:
        total_cost = transaction_data.transaction_volume * stock.price
        if transaction_data.transaction_type == "SELL":
            user.balance -= total_cost

    transaction = Transaction(
        user_id=user.id,
        ticker_id=stock.id,
        transaction_type=transaction_data.transaction_type,
        transaction_volume=transaction_data.transaction_volume,
        transaction_price=stock.price * transaction_data.transaction_volume,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


# Get a user's transaction history
@router.get("/user/{user_id}/transactions/", response_model=list[TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found for this user")
    return transactions


@router.get("/transactions/{user_id}/", response_model=list[TransactionResponse])
def get_transactions_by_user_and_time(
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.created_at >= start_time,
        Transaction.created_at <= end_time
    ).all()

    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No transactions found for this user in the specified time range")

    return transactions
