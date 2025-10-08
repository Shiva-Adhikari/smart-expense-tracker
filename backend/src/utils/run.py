from fastapi import FastAPI
from src.core.database import create_tables
from src.utils.rate_limit_util import rate_limit


create_tables()

app = FastAPI()

limiter = rate_limit(app)
