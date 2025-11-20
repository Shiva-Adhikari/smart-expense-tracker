from tests.test_db import client, get_db
from src.schemas.category import AddCategory
from datetime import datetime, timezone
from tests.api.test_authentication import _login_user


def _add_category():
    # add category first
    category = AddCategory(
        category_name = 'shopping',
        icon=''
    )
    response1 = client.post('/api/v1/category/add', json=category.model_dump())
    
    # Check status
    assert response1.status_code == 200


class TestCategory:
    def test_add_category_success(self):
        # verify user
        _login_user()

        # add category
        _add_category()
