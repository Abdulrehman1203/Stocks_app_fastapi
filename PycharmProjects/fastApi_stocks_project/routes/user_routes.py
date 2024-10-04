from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from passlib.context import CryptContext

from database.db import get_db
from models.user import User
from schemas.user_schema import UserResponse, LoginRequest, UserCreate, RegistrationResponse
from common.authentication import generate_jwt, user_authentication

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash the given password using bcrypt."""
    return pwd_context.hash(plain_password)


@router.post("/register/", response_model=RegistrationResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check for existing user
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create the new user and add it to the database
    new_user = User(username=user_data.username, password=hashed_password, balance=user_data.balance)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token for the new user
    token = generate_jwt(new_user)

    # Return the user details and the token
    return RegistrationResponse(
        user=UserResponse(id=new_user.id, username=new_user.username, balance=new_user.balance),
        token=token
    )


@router.post("/login/", response_model=LoginRequest)
def login_for_access_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    username = login_data.username
    password = login_data.password

    # Authenticate the user and get the token
    token = user_authentication(username, password, db)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    return JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)


@router.get("/user/{user_id}/", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
