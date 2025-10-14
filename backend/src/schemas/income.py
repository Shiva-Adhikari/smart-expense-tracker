from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class AddIncome(BaseModel):
    amount: Decimal
    source: str
    income_date: date
    description: str
    recurring: bool


class UpdateIncome(BaseModel):
    amount: Decimal | None
    source: str | None
    income_date: date | None
    description: str | None
    recurring: bool | None


class ResponseIncome(BaseModel):
    id: int
    amount: Decimal
    source: str
    description: str
    recurring: bool
    income_date: date = Field(..., description="Date in YYYY-MM-DD format", example="2025-10-09")
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseUserIncome(BaseModel):
    message: str
    user_income: ResponseIncome

    model_config = ConfigDict(from_attributes=True)


class ResponseSummary(BaseModel):
    month: str
    total_income: Decimal
    sources: dict
    recurring_income: Decimal
    variable_income: Decimal
    
    model_config = ConfigDict(from_attributes=True)
