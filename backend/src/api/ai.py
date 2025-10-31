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

        
@router.post('/anomalies')
def anomalies(db: DB, user: GetCurrentUser):
    """Detect spending anomalies"""
    
    today_date = datetime.now()
    logger.debug(f'today_date: {today_date}')
    month_ago = today_date - relativedelta(months=1)
    logger.debug(f'month_ago: {month_ago}')
    
    
    # Get all categories
    categories = db.scalars(select(Category)).all()
    logger.debug(f'categories: {categories}')
    
    
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    
    anomalies_list = []
    
    for category in categories:
        # Step 1: Get historical average (last 30 days)
        historical_avg = db.scalar(
            select(func.avg(Expense.amount)).where(
                Expense.user_id == user.id,
                Expense.category_id == category.id,
                Expense.expense_date >= month_ago,
                Expense.expense_date < today_date
            )
        )
        
        # Skip if no historical data
        if not historical_avg:
            continue
            
        logger.debug(f'historical_avg: {historical_avg}')
        
        
        # Step 2: Get today's total for this category
        today_total = db.scalar(
            select(func.sum(Expense.amount)).where(
                Expense.user_id == user.id,
                Expense.category_id == category.id,
                Expense.expense_date == today_date.date()
            )
        )
        
        # Skip if no expenses today
        if not today_total:
            continue
        logger.debug(f'today_total: {today_total}')

        
        # Step 3: Check if anomaly (threshold: 2x average)
        threshold = historical_avg * 2
        logger.debug(f'threshold: {threshold}')

        
        if today_total > threshold:
            # Step 4: Calculate details
            difference = float(today_total - historical_avg)
            multiplier = round(float(today_total / historical_avg), 2)
            
            # Step 5: Determine severity
            if multiplier >= 5.0:
                severity = "critical"
            elif multiplier >= 3.0:
                severity = "high"
            elif multiplier >= 2.0:
                severity = "moderate"
            else:
                severity = "low"
            
            # Step 6: Add to anomalies list
            anomalies_list.append({
                "category": category.category_name,
                "today_amount": float(today_total),
                "expected_average": float(historical_avg),
                "difference": difference,
                "multiplier": multiplier,
                "severity": severity,
                "message": f"आज {category.category_name} मा {multiplier}x बढी खर्च भयो!"
            })
    
    # Return response
    return {
        "date": today_date.strftime('%Y-%m-%d'),
        "anomalies_detected": len(anomalies_list),
        "anomalies": anomalies_list,
        "status": "critical" if any(a['severity'] == 'critical' for a in anomalies_list) else "normal"
    }
