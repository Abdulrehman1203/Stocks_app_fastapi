from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str
    balance: int


class UserResponse(BaseModel):
    id: int
    username: str
    balance: int

    class Config:
        orm_mode = True


class RegistrationResponse(BaseModel):
    user: UserResponse
    token: str


class LoginRequest(BaseModel):
    username: str
    password: str
