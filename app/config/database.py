from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import Settings
import os
from decouple import config

settings = Settings()
env = settings.ENV

DATABASE_URL: str = config("DATABASE_URL")
    
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        