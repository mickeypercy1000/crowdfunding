from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

app = FastAPI()

def init_db():
    Base.metadata.create_all(bind=engine)

def cleanup_db():
    Base.metadata.drop_all(bind=engine)
