from sqlalchemy import Boolean, Column, String

from app.model.base_model import BaseData
from sqlalchemy.orm import relationship



class User(BaseData):
    __tablename__ = "User"

    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, index=True, unique=True)
    email = Column(String, nullable=False, index=True, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    password = Column(String, nullable=False)
    projects = relationship('Project', back_populates='creator', cascade='all')