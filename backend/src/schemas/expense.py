from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class AddExpense(BaseModel):
    category: str
    amount: float
    description: str
    expense_date: date


class ResponseExpense(BaseModel):
    id: int
    category: str
    amount: float
    description: str
    expense_date: date = Field(..., description="Date in YYYY-MM-DD format", example="2025-10-09")
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseAddExpense(BaseModel):
    message: str
    user_expense: ResponseExpense

    model_config = ConfigDict(from_attributes=True)


class ResponseListExpense(BaseModel):
    message: str
    expense_count: int
    expenses: list[ResponseExpense]

    model_config = ConfigDict(from_attributes=True)
