from decimal import Decimal
from typing import List, Optional
import uuid
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator, root_validator
from datetime import date, datetime

from app.schema.authentication import MyDetailsResponseSchema

class ProjectRequestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    goal_amount: float
    deadline: date

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
    
    @root_validator(pre=True)
    def check_fields_not_empty(cls, values):
        for field_name, field_value in values.items():
            if field_name == "description":
                continue
            if isinstance(field_value, str) and not field_value.strip():
                raise ValueError(f"{field_name} must not be empty or blank")
            if field_name == "goal_amount":
                minimum_amount = 5000
                if float(field_value) < minimum_amount:
                    raise ValueError(f"Goal amount cannot be less than ₵{minimum_amount}")
            
        return values


class ProjectContributors(BaseModel):
    username: str = None
    amount: float

    class Config:
        orm_mode = True

class ProjectResponseSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    goal_amount: float
    deadline: date
    total_contribution: float
    creator: MyDetailsResponseSchema

    class Config:
        from_attributes=True
        allow_population_by_field_name = True

class ModifiedProjectResponseSchema(BaseModel):
    project: ProjectResponseSchema
    contributors: Optional[List[ProjectContributors]] = []

    class Config:
        from_attributes=True
        allow_population_by_field_name = True


class ContributionRequestSchema(BaseModel):
    amount: float

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def check_fields_not_empty(cls, values):
        for field_name, field_value in values.items():
            if isinstance(field_value, str) and not field_value.strip():
                raise ValueError(f"{field_name} must not be empty or blank")
            minimum_amount = 100
            if float(field_value) < minimum_amount:
                raise ValueError(f"Goal amount cannot be less than ₵{minimum_amount}")
        return values

class ContributionResponseSchema(BaseModel):
    id: uuid.UUID
    amount: float
    contributor: MyDetailsResponseSchema
    project: ProjectResponseSchema
    
    class Config:
        from_attributes=True
        allow_population_by_field_name = True