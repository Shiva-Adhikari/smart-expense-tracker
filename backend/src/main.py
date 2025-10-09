import uvicorn
from src.api.authentication import router as authentication_router
from src.api.expense import router as expense_router
from src.utils.run import app
from src.core.database import create_tables


create_tables()


@app.get('/')
def health():
    return {'message': 'Running successfully'}


# Include router
app.include_router(authentication_router, prefix='/api/v1')
app.include_router(expense_router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run(
        app, host='localhost', port=8000, reload=True
    )
