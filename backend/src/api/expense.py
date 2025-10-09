from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter
from src.schemas.expense import AddExpense, ResponseAddExpense, ResponseExpense
from src.models.expense import Expense
from datetime import date
from sqlalchemy import select
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


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
    user: GetCurrentUser, db: DB) -> Page[ResponseExpense]:
    """List Expense with pagination (from fastapi_pagination.ext.sqlalchemy import paginate)
    when we using (fastapi_pagination.ext.sqlalchemy) with paginate we don't need db.scalars
    and pass directly query with db when return and cover with paginate
    and search with order_by. and we don't need to use message or anything when return like other
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
