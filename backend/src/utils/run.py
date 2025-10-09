from fastapi import FastAPI
from src.utils.rate_limit_util import rate_limit


app = FastAPI()

limiter = rate_limit(app)
