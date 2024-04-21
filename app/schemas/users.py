from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class SignUpRequest(UserBase):
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class UserDetails(UserBase):
    id: int


class AuthRequest(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
