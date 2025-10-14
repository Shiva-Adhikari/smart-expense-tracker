from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.models.expense import Expense
from datetime import date
from sqlalchemy import select, update, delete
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict
from src.models.category import Category
import calendar
from src.models.income import Income
from decimal import Decimal
from src.schemas.generate_monthly_report import ResponseMonthlyReport


router = APIRouter(prefix='/reports', tags=['Monthly-Reports'])


@router.get('/monthly/{income_date}')
def monthly_summary(income_date: str, db: DB, user: GetCurrentUser):

    year, month = map(int, income_date.split('-'))
    month_name = calendar.month_name[month]
    date_formatted = f'{month_name} {year}'
    days_in_month = calendar.monthrange(year, month)[1]

    incomes = db.scalars(
        select(Income).where(
            Income.user_id == user.id
        )
    ).all()

    total_income = sum(amt.amount for amt in incomes)

    expenses = db.scalars(
        select(Expense).where(
            Expense.user_id == user.id
        )
    ).all()

    total_expense = sum(amt.amount for amt in expenses)

    savings = total_income - total_expense
    savings_rate = round((savings / total_income) * 100, 2)
    
    categories = db.execute(
        select(Expense, Category).where(
            Expense.user_id == user.id
        ).join(Category, Expense.category_id == Category.id)
    ).all()

    # get in tuple and sum all expenses amount
    category = defaultdict(Decimal)
    for expense, data in categories:
        category[data.category_name] += expense.amount
    
    # get in dictionary
    category_breakdown = []
    for key, value in category.items():
        category_breakdown.append({
            'category': key,
            'amount': value,
            'percentage': round((value / total_expense) * 100, 0)
        })
    
    daily_average = round(total_expense / days_in_month, 2)

    highest_day = max(amt.amount for amt in expenses)
    lowest_day = min(amt.amount for amt in expenses)

    return ResponseMonthlyReport(
        month=date_formatted,
        total_income=total_income,
        total_expense=total_expense,
        savings=savings,
        savings_rate=savings_rate,
        category_breakdown=category_breakdown,
        daily_average=daily_average,
        highest_day=highest_day,
        lowest_day=lowest_day
    )
