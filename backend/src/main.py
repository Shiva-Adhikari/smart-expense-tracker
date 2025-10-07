from fastapi import FastAPI
import uvicorn
from src.core.database import create_tables
from src.api.authentication import routes as authentication_router


create_tables()

app = FastAPI()


@app.get('/')
def health():
    return {'message': 'Running successfully'}


# Include router
app.include_router(authentication_router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run(
        app, host='localhost', port=8000, reload=True
    )
