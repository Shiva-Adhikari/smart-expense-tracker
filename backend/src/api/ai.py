from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status
from src.models.expense import Expense
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import select, update, delete, func
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from collections import defaultdict
from src.models.category import Category
import calendar
from src.models.income import Income
from decimal import Decimal
from src.schemas.generate_monthly_report import ResponseMonthlyReport
from src.utils.logger_util import logger
import os
import pickle


router = APIRouter(prefix='/ai', tags=['Ai'])


@router.post('/categorize/{description}')
def predict_category(description: str, db: DB, user: GetCurrentUser):
    
    # Get absolute path
    BASE_DIR = os.path.abspath('src/ml_models')

    VECTORIZER_PATH = os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl')
    MODEL_PATH = os.path.join(BASE_DIR, 'logistic_regression.pkl')
    
    # load
    with open(VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)

    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)

    vector = vectorizer.transform([description])
    prediction = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]
    categories = model.classes_

    # Get max confidence
    confidence = round(max(probabilities) * 100, 2)

    if confidence < 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot predict category - description is unclear or invalid')

    alternatives = [
        {
            'category': cat,
            'confidence': round(prob * 100, 2)
        }
        for cat, prob in zip(categories, probabilities)
    ]

    alternatives = sorted(alternatives, key=lambda x: x['confidence'], reverse=True)

    return {
        'predicted_category': prediction,
        'confidence': f'{confidence}%',
        'alternatives': alternatives
    }
