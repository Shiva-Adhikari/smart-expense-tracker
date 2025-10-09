from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter
from src.schemas.expense import AddExpense, UserExpense
from src.models.expense import Expense


router = APIRouter(prefix='/expense', tags=['Expense'])


@router.post('/add')
def add_expense(data: AddExpense, user: GetCurrentUser, db: DB):
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

    return UserExpense(
        message='Added successfully',
        user_expense=expense
    )
