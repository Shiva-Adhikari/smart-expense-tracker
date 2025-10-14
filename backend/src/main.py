import uvicorn
from src.api.authentication import router as authentication_router
from src.api.expense import router as expense_router
from src.api.category import router as category_router
from src.api.budget import router as budget_router
from src.api.file_upload import router as file_upload_router
from src.api.income import router as income_router
from src.api.generate_monthly_report import router as generate_monthly_report_router
from src.utils.run import app
from src.core.database import create_tables
from fastapi_pagination import add_pagination


create_tables()


@app.get('/')
def health():
    return {'message': 'Running successfully'}


# Include router
app.include_router(authentication_router, prefix='/api/v1')
app.include_router(category_router, prefix='/api/v1')
app.include_router(expense_router, prefix='/api/v1')
app.include_router(budget_router, prefix='/api/v1')
app.include_router(file_upload_router, prefix='/api/v1')
app.include_router(income_router, prefix='/api/v1')
app.include_router(generate_monthly_report_router, prefix='/api/v1')

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        app, host='localhost', port=8000, reload=True
    )
