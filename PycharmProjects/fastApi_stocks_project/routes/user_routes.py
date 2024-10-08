from middleware.logs import logger
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from common.authentication import get_password_hash, pwd_context, create_access_token, verify_password
from models.users import Users
from schemas.user_schema import UserCreate, UserResponse
from database.db import get_db

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"User registration attempt for: {user.username}")

    existing_user = db.query(Users).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if user.balance <= 0:
        raise HTTPException(status_code=400, detail="Balance must be greater than zero")

    # Hash the password and create the user
    hashed_password = pwd_context.hash(user.password)
    new_user = Users(
        username=user.username,

        hashed_password=hashed_password,
        balance=user.balance
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {f"message:  User created successfully, user_id: {new_user.id}  username: {new_user.username}  balance: "
                f"{new_user.balance} "}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")


@router.get("/users/{username}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(username: str, db: Session = Depends(get_db)):
    """
    Retrieves user details by username.
    """
    logger.info(f"fetched User data for: {username}")

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(id=user.id, username=user.username, balance=user.balance)
