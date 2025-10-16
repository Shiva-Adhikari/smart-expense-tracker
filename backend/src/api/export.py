from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.expense import AddExpense, UpdateExpense, ResponseExpense, ResponseUserExpense, ResponseStatistics
from src.models.expense import Expense
from datetime import date
from sqlalchemy import select, update, delete
from collections import defaultdict
from src.models.category import Category
from decimal import Decimal
import csv
from fastapi.responses import FileResponse
from src.utils.logger_util import logger


router = APIRouter(prefix='/export', tags=['Export'])


@router.get('/to_csv/{start_date}/{end_date}/{category_id}')
def export_to_csv(
    start_date: date, end_date: date, category_id: int,
    db: DB, user: GetCurrentUser):

    expenses = db.scalars(
        select(Expense).where(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
            Expense.category_id == category_id
        )
    ).all()

    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Database is empty')
    
    with open('list_expenses.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [key for key in expenses[0].__dict__.keys() if not key.startswith('_')]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for expense in expenses:
            row_data = {key: value for key, value in expense.__dict__.items() if not key.startswith('_')}
            writer.writerow(row_data)

    logger.info('csv file created successfully')

    return FileResponse(
        path='list_expenses.csv',
        filename='expenses_report.csv',
        media_type='text/csv'
    )
