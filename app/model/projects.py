from sqlalchemy import UUID, Column, ForeignKey, String, Date
from app.model.base_model import BaseData
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Numeric
from fastapi import status, HTTPException

class Project(BaseData):
    __tablename__ = 'Project'
    title = Column(String(100), index=True, unique=True)
    description = Column(String(500))
    goal_amount = Column(Numeric(10, 2))
    deadline = Column(Date)
    creator_id = Column(UUID, ForeignKey('User.id'), nullable=False)
    creator = relationship('User', back_populates='projects')

    @validates('goal_amount')
    def validate_goal_amount(self, _, value):
        minimum_goal = 5000
        if value < minimum_goal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Goal amount cannot be less ₵{minimum_goal}"
            )
        return value


