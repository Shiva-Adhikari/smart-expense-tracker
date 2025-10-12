from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.budget import AddBudget, ResponseAddBudget
from src.models.budget import Budget
from sqlalchemy import select, update, delete, insert, or_
from sqlalchemy.orm import joinedload
from src.models.expense import Expense
from src.models.category import Category


router = APIRouter(prefix='/budget', tags=['Budget'])


@router.post('/set-budget')
def set_budget(data: AddBudget, db: DB, user: GetCurrentUser) -> ResponseAddBudget:

    add_budget = Budget(
            user_id=user.id,
            category_id=data.category_id,
            budget_limit=data.budget_limit,
            month=data.month,
            year=data.year
        )

    db.add(add_budget)
    db.commit()
    db.refresh(add_budget)

    return ResponseAddBudget(
        message='Added successfully',
        user_budget=add_budget
    )


@router.get('/stats')
def budget_status(db: DB, user: GetCurrentUser):

    budgets_ = db.scalars(
        select(Budget).where(
            Budget.user_id == user.id
        )
    ).first()

    if not budgets_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You haven't set budget yet.")

    category_ = db.scalars(
        select(Category).where(
            Category.id == budgets_.category_id,
        )
    ).first()

    expenses_ = db.scalars(
        select(Expense).where(
            Expense.category_id == category_.id,
            Expense.user_id == user.id
        )
    ).all()

    category = get_category_name(category_)
    budget_lim = get_budget_limit(budgets_)
    total_spent = get_total_spent(expenses_)
    length_of_expenses = get_how_much_spent(expenses_)
    remaining = get_remaining_expenses(budget_lim, total_spent)
    percentage = get_percentage(total_spent, budget_lim)
    get_status = get_status(percentage)

    return {
        'category': category,
        'budget': budget_lim,
        'spent': total_spent,
        'remaining': remaining,
        'percentage': percentage,
        'status': get_status
    }

# ################## utils ##################

def get_how_much_spent(expense: Expense) -> int:
    return len([amt.amount for amt in expense])

def get_category_name(category: Category) -> str:
    return category.category_name


def get_budget_limit(budget: Budget) -> float:
    return budget.budget_limit


def get_total_spent(expense: Expense) -> float:
    return sum(amt.amount for amt in expense)


def get_percentage(total_spent: int, budget_lim: int) -> int:
    return round((total_spent / budget_lim) * 100)


def get_remaining_expenses(budget_lim: float, total_spent: float) -> float:
    return budget_lim - total_spent


def get_status(percentage: int) -> str:
    if percentage < 80 and percentage > 0:
        return 'ok'
    elif percentage >= 80 and percentage < 100:
        return 'warning'
    elif percentage >= 100:
        return 'exceed'
    else:
        return 'no_expenses'
