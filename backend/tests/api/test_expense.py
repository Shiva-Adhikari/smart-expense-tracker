from tests.test_db import client, get_db
from src.schemas.expense import AddExpense
from datetime import datetime, timezone, date
from tests.api.test_category import _add_category
from tests.api.test_authentication import _login_user
import json


class TestExpense:
    def test_add_expense_success(self):
        # verify user
        _login_user()

        # Add category first
        _add_category()

        # add expense
        expense = AddExpense(
            category_id=1,
            amount=200,
            description='coffee',
            expense_date=date.today()
        )

        response = client.post('/api/v1/expense/add', json=json.loads(expense.model_dump_json()))
    
        # check status
        assert response.status_code == 200
