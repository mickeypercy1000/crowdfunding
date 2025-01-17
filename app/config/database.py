from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.config.settings import Settings
import os


settings = Settings()
env = settings.ENV

if env == "production":
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://sokdavms:S0B-mwT_zwnK-YcJNpKB9Zb1F-2Z_rLb@rogue.db.elephantsql.com/sokdavms")
else:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Enigma.100@localhost:5432/crowdfunddb")
    
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        