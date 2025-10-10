from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.expense import AddExpense, UpdateExpense, ResponseExpense, ResponseUserExpense, ResponseStatistics
from src.models.expense import Expense
from datetime import date
from sqlalchemy import select, update, delete
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict


router = APIRouter(prefix='/expense', tags=['Expense'])


@router.post('/add')
def add_expense(data: AddExpense, user: GetCurrentUser, db: DB) -> ResponseUserExpense:
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

    return ResponseUserExpense(
        message='Added successfully',
        user_expense=expense
    )


@router.get('/list/{start_date}/{end_date}/{category}')
def list_expense(
    start_date: date, end_date: date, category: str,
    user: GetCurrentUser, db: DB) -> Page[ResponseExpense]:
    """List Expense with pagination (from fastapi_pagination.ext.sqlalchemy import paginate).
    when we using (fastapi_pagination.ext.sqlalchemy) with paginate we don't need db.scalars
    and pass directly (query with db) when return and cover with paginate
    and search with order_by. and we don't need to use message or anything 
    when return like (add_expense)other
    it will break code, remember that.
    docs link: https://uriyyo-fastapi-pagination.netlify.app/#quickstart
    """

    query = select(Expense).where(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
            Expense.category == category
        ).order_by(
            Expense.expense_date
        )

    return paginate(db, query)


@router.put('/update/{id}')
def update_expense(id: int, data: UpdateExpense, db: DB, user: GetCurrentUser) -> ResponseUserExpense:

    updated_data = db.scalars(
        update(Expense).where(
            Expense.id == id,
            Expense.user_id == user.id
        ).values(
            category=data.category,
            amount=data.amount,
            description=data.description,
            expense_date=data.expense_date,
        ).returning(Expense)
    ).first()

    if not updated_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return ResponseUserExpense(
        message='Updated successfully',
        user_expense=updated_data
    )


@router.delete('/delete/{id}')
def delete_expense(id: int, db: DB, user: GetCurrentUser) -> dict:

    delete_data = db.scalars(
        delete(Expense).where(
            Expense.id == id
        ).returning(Expense)
    ).first()

    if not delete_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return {'message': 'Deleted successfully'}

@router.get('/stats')
def simple_statistics(db: DB, user: GetCurrentUser):
    count_data = db.scalars(
        select(Expense).where(
            Expense.user_id == user.id
        )
    ).all()

    if not count_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Database is empty')

    total_expenses = sum(data.amount for data in count_data)
    expense_count = len(count_data)
    average = round(total_expenses/expense_count, 2)

    categories = defaultdict(float)
    for data in count_data:
        categories[data.category] += data.amount
    
    return ResponseStatistics(
        total_expenses=total_expenses,
        expense_count=expense_count,
        average=average,
        categories=dict(categories)
    )
