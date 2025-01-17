from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON

from app.model.base_model import BaseData



class User(BaseData):
    __tablename__ = "User"

    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, index=True, unique=True)
    email = Column(String, nullable=False, index=True, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    password = Column(String, nullable=False)
