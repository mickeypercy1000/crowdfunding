from datetime import datetime
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Date
from app.model.base_model import BaseData
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric

class Project(BaseData):
    __tablename__ = 'Project'
    title = Column(String(100), index=True, unique=True)
    description = Column(String(500), nullable=True)
    goal_amount = Column(Numeric(10, 2))
    deadline = Column(Date)
    creator_id = Column(UUID, ForeignKey('User.id'), nullable=False)
    total_contribution = Column(Numeric(10, 2), default=0.00)
    creator = relationship('User', back_populates='projects')
    contributions = relationship('Contribution', back_populates='project')

class Contribution(BaseData):
    __tablename__ = 'Contribution'

    contributor_id = Column(UUID, ForeignKey('User.id'), nullable=False)
    project_id = Column(UUID, ForeignKey('Project.id'), nullable=False)
    amount = Column(Numeric(10, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)

    contributor = relationship('User', back_populates='contributions')
    project = relationship('Project', back_populates='contributions')
    