from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

DATABASE_URL = settings.DATABASE_URL.get_secret_value()
engine = create_engine(DATABASE_URL, echo=settings.DEBUG)

session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
