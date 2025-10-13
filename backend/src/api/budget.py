from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.budget import AddBudget, ResponseAddBudget
from src.models.budget import Budget
from sqlalchemy import select, update, delete, insert, or_, func
from sqlalchemy.orm import joinedload
from src.models.expense import Expense
from src.models.category import Category


router = APIRouter(prefix='/budget', tags=['Budget'])


@router.post('/set-budget')
def set_budget(data: AddBudget, db: DB, user: GetCurrentUser) -> ResponseAddBudget:

    category_ids = db.scalars(
        select(Category).where(
            Category.id == data.category_id
        )
    ).first()

    if not category_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

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

    budgets = db.scalars(
        select(Budget).where(
            Budget.user_id == user.id
        )
    ).all()

    if not budgets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You haven't set budget yet.")

    result = []

    for budget in budgets:
        category = db.scalars(
            select(Category).where(
                Category.id == budget.category_id,
            )
        ).first()

        expenses = db.scalars(
            select(Expense).where(
                Expense.category_id == category.id,
                Expense.user_id == user.id,
                # extract only month from Expense.expense_date and compare to budget.month | like also year >
                func.extract('month', Expense.expense_date) == budget.month,
                func.extract('year', Expense.expense_date) == budget.year
            )
        ).all()

        category = get_category_name(category)
        budget_lim = get_budget_limit(budget)
        total_spent = get_total_spent(expenses)
        length_of_expenses = get_how_much_spent(expenses)
        remaining = get_remaining_expenses(budget_lim, total_spent)
        percentage = get_percentage(total_spent, budget_lim)
        stat = get_status(percentage)

        result.append({
            'category': category,
            'budget_lim': budget_lim,
            'total_spent': total_spent,
            'remaining': remaining,
            'percentage': percentage,
            'stat': stat
        })

    return {
        'budget': result
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
