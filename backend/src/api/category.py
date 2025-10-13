from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.schemas.category import AddCategory, UpdateCategory, ResponseUserCategory
from src.models.category import Category
from sqlalchemy import select, update, delete, insert, or_


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
def delete_all_category(db: DB) -> dict:
    is_delete = db.scalars(
        delete(Category).returning(Category)
    )
    
    if not is_delete.all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found to delete')

    db.commit()

    return {'message': 'Delete successfully'}


@router.get('/list_all')
def list_all_category(db: DB, user: GetCurrentUser):
    categories = db.scalars(
        select(Category).where(
            or_(
                Category.user_id == user.id,
                Category.user_id.is_(None)
            )
        )
    ).all()

    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category is empty')

    return {
        'message': 'Fetch successfully',
        'data': [data for data in categories]
    }


@router.post('/add')
def add_category(data: AddCategory, user: GetCurrentUser, db: DB) -> ResponseUserCategory:
    """ Add Category
    """

    category = Category(
        user_id=user.id,
        category_name=data.category_name,
        icon=data.icon,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return ResponseUserCategory(
        message='Added successfully',
        user_category=category
    )


@router.put('/update/{id}')
def update_category(id: int, data: UpdateCategory, db: DB, user: GetCurrentUser) -> ResponseUserCategory:

    updated_data = db.scalars(
        update(Category).where(
            Category.id == id,
            Category.user_id == user.id,
            Category.is_default.is_(False)
        ).values(
            category_name=data.category_name,
            icon=data.icon,
        ).returning(Category)
    ).first()

    if not updated_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return ResponseUserCategory(
        message='Updated successfully',
        user_category=updated_data
    )


@router.delete('/delete/{id}')
def delete_category(id: int, db: DB, user: GetCurrentUser) -> dict:

    delete_data = db.scalars(
        delete(Category).where(
            Category.id == id,
            Category.user_id == user.id,
            Category.is_default.is_(False)
        ).returning(Category)
    ).first()

    if not delete_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not found')

    db.commit()

    return {'message': 'Deleted successfully'}
