import uuid
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from datetime import date, datetime

from app.schema.authentication import MyDetailsResponseSchema

class ProjectRequestSchema(BaseModel):
    title: str
    description: str
    goal_amount: float
    deadline: date

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
    
    @field_validator("title")
    def validate_title_not_empty(cls, value):
        if not value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )
        return value
    
    @field_validator("deadline")
    def validate_deadline(cls, value):
        current_year = datetime.now().date()
        if value < current_year:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid deadline date"
            )
        return value


class ProjectResponseSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    goal_amount: float
    deadline: date
    current_user: MyDetailsResponseSchema