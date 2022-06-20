from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return {
        'data': 'Welcome to Prime CM'
    }
