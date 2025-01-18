import uuid
from pydantic import BaseModel, EmailStr, field_validator, root_validator
from datetime import datetime
from typing import Optional


class SignUpRequestSchema(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str

    @root_validator(pre=True)
    def check_fields_not_empty(cls, values):
        for field_name, field_value in values.items():
            if isinstance(field_value, str) and not field_value.strip():
                raise ValueError(f"{field_name} must not be empty or blank")
        return values
    
    @field_validator("password")
    def password_validator(cls, value):
        from app.common.utils import UserUtils
        return UserUtils.validate_password(value)

class SignupResponseSchema(BaseModel):
    status: bool
    id: uuid.UUID = None
    message: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

    @root_validator(pre=True)
    def check_fields_not_empty(cls, values):
        for field_name, field_value in values.items():
            if isinstance(field_value, str) and not field_value.strip():
                raise ValueError(f"{field_name} must not be empty or blank")
        return values

class LoginResponseSchema(BaseModel):
    status: bool
    user_id: uuid.UUID = None
    message: str
    email: EmailStr = None
    firstname: str = None
    lastname: str = None
    username: str = None
    access_token: str = None

class MyDetailsResponseSchema(BaseModel):
    status: bool = False
    id: uuid.UUID = None
    email: EmailStr = None
    firstname: str = None
    lastname: str = None
    username: str = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes=True
        populate_by_name = True
