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
    expense_date: date = Field(..., description="Date in YYYY-MM-DD format")
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserExpense(BaseModel):
    message: str
    user_expense: ResponseExpense

    model_config = ConfigDict(from_attributes=True)
