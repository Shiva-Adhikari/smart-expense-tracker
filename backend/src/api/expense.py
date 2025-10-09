from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter
from src.schemas.expense import AddExpense, ResponseAddExpense, ResponseListExpense, ResponseExpense
from src.models.expense import Expense
from datetime import date
from sqlalchemy import select


router = APIRouter(prefix='/expense', tags=['Expense'])


@router.post('/add')
def add_expense(data: AddExpense, user: GetCurrentUser, db: DB) -> ResponseAddExpense:
    """ Add Expense
    """

    expense = Expense(
        user_id=user.id,
        category=data.category,
        amount=data.amount,
        description=data.description,
        expense_date=data.expense_date
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return ResponseAddExpense(
        message='Added successfully',
        user_expense=expense
    )


@router.get('/list/{start_date}/{end_date}/{category}')
def list_expense(
    start_date: date, end_date: date, category: str,
    user: GetCurrentUser, db: DB) -> ResponseListExpense:
    """List Expense
    """

    expenses = db.scalars(
        select(Expense).where(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
            Expense.category == category
        )
    ).all()

    return ResponseListExpense(
        message='Fetch successfully',
        expense_count=len(expenses),
        expenses=expenses
    )


'''Pagination Works, learn and apply
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

@router.get('/list/{start_date}/{end_date}/{category}', response_model=Page[ResponseExpense])
def list_expense(
    start_date: date, 
    end_date: date, 
    category: str,
    user: GetCurrentUser, 
    db: DB
) -> Page[ResponseExpense]:
    """List Expense"""
    
    query = select(Expense).where(
        Expense.expense_date >= start_date,
        Expense.expense_date <= end_date,
        Expense.category == category
    ).order_by(Expense.expense_date.desc())
    
    return paginate(db, query)
'''
