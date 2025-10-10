from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.budget import AddBudget, ResponseAddBudget
from src.models.budget import Budget
from sqlalchemy import select, update, delete, insert, or_
from sqlalchemy.orm import joinedload


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

    # return {'message': 'done'}
    return ResponseAddBudget(
        message='Added successfully',
        user_budget=add_budget
    )
