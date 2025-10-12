from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional


class AddExpense(BaseModel):
    category_id: int
    amount: float
    description: str
    expense_date: date


class UpdateExpense(BaseModel):
    category_id: Optional[int]
    amount: Optional[float]
    description: Optional[str]
    expense_date: Optional[date]


class ResponseExpense(BaseModel):
    id: int
    category_id: int
    amount: float
    description: str
    expense_date: date = Field(..., description="Date in YYYY-MM-DD format", example="2025-10-09")
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseUserExpense(BaseModel):
    message: str
    user_expense: ResponseExpense

    model_config = ConfigDict(from_attributes=True)


class ResponseStatistics(BaseModel):
    total_expenses: float
    expense_count: float
    average: float
    categories: dict[str, float]

    model_config = ConfigDict(from_attributes=True)
