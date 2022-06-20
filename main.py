from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from prime_cm.routers.user import router as ur

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def index():
    return {
        'data': 'Welcome to Prime CM'
    }

app.include_router(ur)

TORTOISE_ORM = {
    "connections": {"default": "sqlite://./db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "prime_cm.models.user",
            ],
            "default_connection": "default"
        }
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)
