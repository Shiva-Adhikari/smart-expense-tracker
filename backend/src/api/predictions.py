from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
# from src.schemas.income import AddIncome, UpdateIncome, ResponseIncome, ResponseUserIncome, ResponseSummary
from src.models.expense import Expense
from datetime import date, datetime
from sqlalchemy import select, update, delete, func
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict
from src.models.category import Category
from decimal import Decimal
import calendar
from dateutil.relativedelta import relativedelta
from src.utils.logger_util import logger


router = APIRouter(prefix='/predictions', tags=['Predictions'])


@router.get('/daily')
def daily_predictions(user: GetCurrentUser, db: DB):
    """ predict daily expenses
    """
    
    # ##day = "Like sunday,monday ..."
    
    # Today date and day
    today_date = datetime.now()
    format_today_date = today_date.strftime('%Y-%m-%d')
    today_day = today_date.strftime('%A')

    # Debug
    logger.debug(f'format_today_date: {format_today_date}')
    logger.debug(f'today_day: {today_day}')
    
    # Set time of 3 months earlier date
    previous_3_months_date = today_date - relativedelta(months=3)
    # Debug
    logger.debug(f'previous_2_months_date: {previous_3_months_date}')
    
    # Fetch 3 months expense
    expenses = db.scalars(
        select(Expense).where(
            Expense.user_id == user.id,
            Expense.expense_date >= previous_3_months_date,
            # func.trim(func.to_char(Expense.expense_date, 'Day')) == today_day
        )
    ).all()

    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Please insert expense first')

    # Find length
    expenses_len = len(expenses)
    expenses_day_len = len([amt.amount for amt in expenses if amt.expense_date.strftime('%A') == today_day])

    # Average sum
    expenses_day_sum = sum(amt.amount for amt in expenses if amt.expense_date.strftime('%A') == today_day)
    expenses_sum = sum(amt.amount for amt in expenses)

    # Debug
    logger.debug(f'expenses_day_sum: {expenses_day_sum}')
    logger.debug(f'expenses_sum: {expenses_sum}')

    # Calculate multiplier
    base_average = expenses_sum // expenses_len
    base_day_average = expenses_day_sum // expenses_day_len
    multiplier = round(base_day_average / base_average, 2)

    # Debug
    logger.debug(f'multiplier: {multiplier}')
    logger.debug(f'base_day_average: {base_day_average}')

    # Predict Amount using multiplier
    predicted_amount = round(base_average * multiplier, 0)
    logger.debug(f'predicted_amount: {predicted_amount}')

    calculation_method = 'average_with_multiplier'
    
    # Which day is today
    if today_day == 'Saturday' or today_day == 'Sunday':
        reason = 'Weekend pattern detected'
    elif today_day == 'Friday':
        reason = 'Payday effect'
    else:
        reason = 'Normal weekday pattern'

    # Yesterday
    yesterday_date = today_date - relativedelta(days=1)
    yesterday_day = yesterday_date.strftime('%A')

    # Debug
    logger.debug(f'yesterday_date: {yesterday_date}')
    logger.debug(f'yesterday_day: {yesterday_day}')

    # Yesterday expense
    yesterday_expenses = db.scalars(
        select(Expense).where(
            Expense.user_id == user.id,
            Expense.expense_date == yesterday_date.date(),
        )
    ).first()

    if yesterday_expenses:
        yesterday_expense = yesterday_expenses.amount
    else:
        yesterday_expense = f'previous {yesterday_day} expense not found'

    # Get previous today day (Sunday or any day)
    previous_date = today_date - relativedelta(days=8)
    previous_day = previous_date.strftime('%A')

    # Debug
    logger.debug(f'previous_date: {previous_date}')
    logger.debug(f'previous_day: {previous_day}')

    # Prevous today day expense
    last_day_expenses = db.scalars(
        select(Expense).where(
            Expense.user_id == user.id,
            Expense.expense_date == previous_date.date(),
            func.trim(func.to_char(Expense.expense_date, 'Day')) == previous_day
        )
    ).first()

    if last_day_expenses:
        last_day_expense = last_day_expenses.amount
    else:
        last_day_expense = f'previous {previous_day} expense not found'

    # Get confidence by how much data we fetch
    if expenses_len >= 90:
        confidence = 'high'
    elif expenses_len >= 60:
        confidence = 'good'
    elif expenses_len >= 30:
        confidence = 'medium'
    else:
        confidence = 'low'

    message = f'Today you are going to expense Rs. {predicted_amount} ({reason})'

    result = {
        'date': format_today_date,
        'day_of_week': today_day,
        'predicted_amount': predicted_amount,
        'calculation_method': calculation_method,
        'details': {
            'base_average': base_average,
            'multiplier': multiplier,
            'reason': reason
        },
        'comparison': {
            'yesterday': yesterday_expense,
            f'last_{today_day.lower()}': last_day_expense,
            f'average_{today_day.lower()}': base_average
        },
        'confidence': confidence,
        'message': message
    }
    
    return result
