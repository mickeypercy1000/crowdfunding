from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import UUID, DateTime
import uuid
from datetime import datetime


Base = declarative_base()

class BaseData(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
    