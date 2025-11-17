from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from src.main import app
from fastapi.testclient import TestClient
from src.core.database import get_db as production_get_db, Base


TEST_DATABASE_URL = 'postgresql://postgres:@localhost:5432/smart_expense_tracker_test'

'''
create from terminal
# createdb -U postgres smart_expense_tracker_test
'''

engine = create_engine(TEST_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    with SessionLocal() as db:
        yield db

def create_tables():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print('Created tables successfully')
    except Exception as e:
        print(f'(Failed to create tables) | {e}')


app.dependency_overrides[production_get_db] = get_db

create_tables()
client = TestClient(app)
