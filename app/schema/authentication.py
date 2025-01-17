import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SignUpRequestSchema(BaseModel):
    """
    Schema for user sign up
    """
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str

class SignupResponseSchema(BaseModel):
    id: uuid.UUID = None
    status: bool
    message: str


class VerifyEmailRequestSchema(BaseModel):
    """
    Schema for email verification
    """
    verification_id: uuid.UUID
    otp: str

class VerifyEmailResponseSchema(BaseModel):
    status: bool
    user_id: uuid.UUID
    message: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

class LoginResponseSchema(BaseModel):
    user_id: uuid.UUID = None
    message: str
    email: EmailStr = None
    firstname: str = None
    lastname: str = None
    username: str = None
    access_token: str = None

class MyDetailsResponseSchema(BaseModel):
    user_id: uuid.UUID = None
    email: EmailStr = None
    firstname: str = None
    lastname: str = None
    username: str = None
    date_joined: Optional[datetime] = None
