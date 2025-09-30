from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/')
def health():
    return {'message': 'Running successfully'}


if __name__ == "__main__":
    uvicorn.run(
        app, host='localhost', port=8000, reload=True
    )
