from pydantic import EmailStr, BaseModel, ConfigDict
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    message: str
    user: AuthResponse

    model_config = ConfigDict(from_attributes=True)
