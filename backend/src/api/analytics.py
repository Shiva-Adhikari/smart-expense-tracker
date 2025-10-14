from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.models.expense import Expense
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import select, update, delete, func
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict
from src.models.category import Category
import calendar
from src.models.income import Income
from decimal import Decimal
from src.schemas.generate_monthly_report import ResponseMonthlyReport
from src.utils.logger_util import logger


router = APIRouter(prefix='/analytics', tags=['Analytics'])


@router.get('/trends/{aggregation}')
def daily_weekly_aggregation(aggregation: str, db: DB, user: GetCurrentUser):

    match (aggregation):
        case 'monthly':
            return monthly(aggregation, db, user)

        case 'weekly':
            pass

        case 'daily':
            pass

        case _:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='allowed only (monthly, weekly and daily)')


def monthly(aggregation: str, db: DB, user: GetCurrentUser):
    
    period = 'Last 6 months'

    today = datetime.now()
    date = today - relativedelta(months=6)

    data = []
    for i in range(6):
        # increment date month by month
        date = date + relativedelta(months=1)
        year = date.year
        month = date.month

        # get like this (may 2025)
        month_name = calendar.month_name[month]
        date_formatted = f'{month_name} {year}'

        # get expenses using join
        expenses = db.execute(
            select(Expense, Category).where(
                Expense.user_id == user.id,
                func.extract('year', Expense.expense_date) == year,
                func.extract('month', Expense.expense_date) == month
            ).join(Category, Expense.category_id == Category.id)
        ).all()

        # get category_name and sum of amount of same category
        categories = defaultdict(Decimal)
        for expense, category in expenses:
            categories[category.category_name] += expense.amount

        # sum total expense
        total_expense = sum(categories.values())

        if expenses:
            data.append({
                'date':date.strftime('%Y-%m-%d'),
                'month':date_formatted,
                'categories': categories
            })

    return {
        'period':period,
        'aggregation':aggregation,
        'data': data
    }
