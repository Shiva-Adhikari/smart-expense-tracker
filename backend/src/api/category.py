from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
# from src.schemas.expense import 
from src.models.category import Category
from datetime import date
from sqlalchemy import select, update, delete, insert
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict


router = APIRouter(prefix='/category', tags=['Category'])


@router.post('/init')
def init_category(db: DB) -> dict:
    
    init_data = [
        {'category_name': 'Shopping', 'is_default': True},
        {'category_name': 'Education', 'is_default': True},
        {'category_name': 'Healthcare', 'is_default': True},
        {'category_name': 'Entertainment', 'is_default': True},
        {'category_name': 'Food & Dining', 'is_default': True},
        {'category_name': 'Transportation', 'is_default': True},
        {'category_name': 'Bills & Utilities', 'is_default': True},
        {'category_name': 'Others', 'is_default': True}
    ]
    
    category_names = [data['category_name'] for data in init_data]
    
    existing = db.scalars(
        select(Category).where(
            Category.category_name.in_(category_names)
        )
    ).all()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Category name is already initialized')

    init_add = db.scalars(
        insert(Category).returning(Category),
        init_data
    )

    db.flush(init_add)
    db.commit()

    return {
        'message': 'Added successfully',
        'data': [{'id': cat.id, 'category_name': cat.category_name} for cat in init_add]
    }


@router.delete('/delete_all')
def init_category(db: DB) -> dict:
    is_delete = db.scalars(
        delete(Category).returning(Category)
    )
    
    if not is_delete.all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found to delete')

    db.commit()

    return {'message': 'Delete successfully'}
