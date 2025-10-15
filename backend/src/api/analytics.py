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
            return weekly(aggregation, db, user)

        case 'daily':
            return daily(aggregation, db, user)

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

        if expenses:
            # get category_name and sum of amount of same category
            categories = defaultdict(Decimal)
            for expense, category in expenses:
                categories[category.category_name] += expense.amount

            # sum total expense
            total_expense = sum(categories.values())

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


# get only weekly report not other
def weekly(aggregation: str, db: DB, user: GetCurrentUser):
    
    period = 'Last 6 months of weeks'

    today = datetime.now()
    date = today - relativedelta(months=6)

    # print(date)
    # date1 = date - relativedelta(weeks=1)
    # print(date1)
    # print(f"Start date (6 months ago): {date}")

    current_date = date

    data = []
    # Loop while current_date is less than today
    while current_date < today:
        # print(f"Week1: {current_date}")
        # print('done')
        year = current_date.year
        month = current_date.month
        # week = current_date.weekday
        get_current_date = current_date
        current_date = current_date + relativedelta(weeks=1) - relativedelta(days=1)
        print(f'get_current_date: {get_current_date}')
        print(f'current_date: {current_date}\n')
        if current_date > today:
            current_date = today

        # get like this (may 2025)
        month_name = calendar.month_name[month]
        date_formatted = f'{month_name} {year}'
        
        # logger.debug(f'date_formatted: {date_formatted}')

        # get expenses using join
        expenses = db.execute(
            select(Expense, Category).where(
                Expense.user_id == user.id,
                func.extract('year', Expense.expense_date) == year,
                func.extract('month', Expense.expense_date) == month,
                Expense.expense_date >= get_current_date,
                Expense.expense_date < current_date + relativedelta(days=1),
            ).join(Category, Expense.category_id == Category.id)
        ).all()

        if expenses:
            # get category_name and sum of amount of same category
            categories = defaultdict(Decimal)
            for expense, category in expenses:
                categories[category.category_name] += expense.amount

            # sum total expense
            total_expense = sum(categories.values())

            data.append({
                'date':get_current_date.strftime('%Y-%m-%d'),
                'month':date_formatted,
                'categories': categories
            })
        
    
    # print(f"\nTotal weeks: {week_count}")
    # print(f"Today: {today}")

    return {
        'period':period,
        'aggregation':aggregation,
        'data': data
    }


def daily(aggregation: str, db: DB, user: GetCurrentUser):
    
    period = 'Last months of 30 days'

    today = datetime.now()
    date = today - relativedelta(months=1)

    # print(date)
    # date1 = date - relativedelta(days=1)
    # print(date1)
    # print(f"Start date (6 months ago): {date}")

    current_date = date

    data = []
    # Loop while current_date is less than today
    while current_date < today:
        # print(f"Week1: {current_date}")
        # print('done')
        year = current_date.year
        month = current_date.month
        day = current_date.day
        get_current_date = current_date
        current_date = current_date + relativedelta(days=1)

        # get like this (may 2025)
        month_name = calendar.month_name[month]
        date_formatted = f'{month_name} {year}'
        
        # logger.debug(f'date_formatted: {date_formatted}')
        # print(f'get_current_date: {get_current_date}')

        # get expenses using join
        expenses = db.execute(
            select(Expense, Category).where(
                Expense.user_id == user.id,
                func.extract('year', Expense.expense_date) == year,
                func.extract('month', Expense.expense_date) == month,
                func.extract('day', Expense.expense_date) == day
            ).join(Category, Expense.category_id == Category.id)
        ).all()

        # this should be here
        if expenses:

            # get category_name and sum of amount of same category
            categories = defaultdict(Decimal)
            for expense, category in expenses:
                categories[category.category_name] += expense.amount

            # sum total expense
            total_expense = sum(categories.values())

        # if expenses:
            data.append({
                'date':get_current_date.strftime('%Y-%m-%d'),
                'month':date_formatted,
                'categories': categories
            })


    # print(f"\nTotal weeks: {week_count}")
    # print(f"Today: {today}")

    return {
        'period':period,
        'aggregation':aggregation,
        'data': data
    }
