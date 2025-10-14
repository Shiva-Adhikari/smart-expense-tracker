from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class ResponseMonthlyReport(BaseModel):
    month: str
    total_income: Decimal
    total_expense: Decimal
    savings: Decimal
    savings_rate: float
    category_breakdown: list
    daily_average: Decimal
    highest_day: Decimal
    lowest_day: Decimal
