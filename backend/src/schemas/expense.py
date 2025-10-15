from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class AddExpense(BaseModel):
    category_id: int
    amount: Decimal
    description: str
    expense_date: date


class UpdateExpense(BaseModel):
    category_id: Optional[int]
    amount: Optional[Decimal]
    description: Optional[str]
    expense_date: Optional[date]


class ResponseExpense(BaseModel):
    id: int
    category_id: int
    amount: Decimal
    description: str
    expense_date: date = Field(..., description="Date in YYYY-MM-DD format", example="2025-10-09")
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseUserExpense(BaseModel):
    message: str
    user_expense: ResponseExpense

    model_config = ConfigDict(from_attributes=True)


class ResponseStatistics(BaseModel):
    total_expenses: Decimal
    expense_count: Decimal
    average: Decimal
    categories: dict
    # categories: dict[str, Decimal]

    model_config = ConfigDict(from_attributes=True)
