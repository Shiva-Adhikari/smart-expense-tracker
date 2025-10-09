from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings
from src.utils.logger_util import logger
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated


DATABASE_URL = settings.DATABASE_URL.get_secret_value()

DEBUG = settings.DEBUG
engine = create_engine(DATABASE_URL, echo=DEBUG)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    with SessionLocal() as db:
        yield db


class Base(DeclarativeBase):
    pass


def create_tables():
    try:
        # Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        logger.info('Created tables successfully')
    except Exception as e:
        logger.info(f'(Failed to create tables) | {e}')


DB = Annotated[Session, Depends(get_db)]
