from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class AddBudget(BaseModel):
    category_id: int
    budget_limit: Decimal
    month: int
    year: int


class ResponseBudget(BaseModel):
    id: int
    category_id: int
    budget_limit: Decimal
    month: int
    year: int

    model_config = ConfigDict(from_attributes=True)


class ResponseAddBudget(BaseModel):
    message: str
    user_budget: ResponseBudget

    model_config = ConfigDict(from_attributes=True)
