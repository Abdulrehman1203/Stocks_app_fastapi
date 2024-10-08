from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    balance: float


class UserResponse(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        from_attributes = True
