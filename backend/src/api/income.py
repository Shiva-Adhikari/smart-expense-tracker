from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.income import AddIncome, UpdateIncome, ResponseIncome, ResponseUserIncome, ResponseSummary
from src.models.income import Income
from datetime import date
from sqlalchemy import select, update, delete, func
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict
from src.models.category import Category
from decimal import Decimal
import calendar


router = APIRouter(prefix='/income', tags=['Income'])


@router.post('/add')
def add_income(data: AddIncome, user: GetCurrentUser, db: DB) -> ResponseUserIncome:
    """ Add Income
    """

    income = Income(
        user_id=user.id,
        amount=data.amount,
        source=data.source,
        income_date=data.income_date,
        description=data.description,
        recurring=data.recurring
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return ResponseUserIncome(
        message='Added successfully',
        user_income=income
    )


@router.get('/list/{start_date}/{end_date}/{source}')
def list_income(
    start_date: date, end_date: date, source: str,
    user: GetCurrentUser, db: DB) -> Page[ResponseIncome]:
    """List Income with pagination (from fastapi_pagination.ext.sqlalchemy import paginate).
    when we using (fastapi_pagination.ext.sqlalchemy) with paginate we don't need db.scalars
    and pass directly (query with db) when return and cover with paginate
    and search with order_by. and we don't need to use message or anything 
    when return like (add_income)other
    it will break code, remember that.
    docs link: https://uriyyo-fastapi-pagination.netlify.app/#quickstart
    """

    query = select(Income).where(
            Income.income_date >= start_date,
            Income.income_date <= end_date,
            Income.source == source
        ).order_by(
            Income.income_date
        )

    return paginate(db, query)


@router.put('/update/{id}')
def update_income(id: int, data: UpdateIncome, db: DB, user: GetCurrentUser) -> ResponseUserIncome:

    updated_data = db.scalars(
        update(Income).where(
            Income.id == id,
            Income.user_id == user.id
        ).values(
            amount=data.amount,
            source=data.source,
            income_date=data.income_date,
            description=data.description,
            recurring=data.recurring
        ).returning(Income)
    ).first()

    if not updated_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return ResponseUserIncome(
        message='Updated successfully',
        user_income=updated_data
    )


@router.delete('/delete/{id}')
def delete_income(id: int, db: DB, user: GetCurrentUser) -> dict:

    delete_data = db.scalars(
        delete(Income).where(
            Income.id == id,
            Income.user_id == user.id
        ).returning(Income)
    ).first()

    if not delete_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return {'message': 'Deleted successfully'}


@router.get('/summary/{income_date}')
def monthly_summary(income_date: str, db: DB, user: GetCurrentUser):
    count_data = db.scalars(
        select(Income).where(
            Income.user_id == user.id,
            func.to_char(Income.income_date, 'YYYY-MM') == income_date
        )
    ).all()

    if not count_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Please add your income first')

    total_income = sum(amt.amount for amt in count_data)

    sources = defaultdict(Decimal)
    for data in count_data:
        sources[data.source] += data.amount
    
    recurring_income = sum(amt.amount for amt in count_data if Income.recurring)
    variable_income = sum(amt.amount for amt in count_data if not Income.recurring)
    
    year, month = map(int, income_date.split('-'))
    month_name = calendar.month_name[month]
    date_formatted = f'{month_name} {year}'

    return ResponseSummary(
        month=date_formatted,
        total_income=total_income,
        sources=dict(sources),
        recurring_income=recurring_income,
        variable_income=variable_income
    )
