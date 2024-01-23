# Documentation w/ Swagger: http://127.0.0.1:8000/docs
# Documentation w/ Redocly: http://127.0.0.1:8000/redoc

# Start server: uvicorn main:app --reload

from fastapi import FastAPI
from routers import products, users, jwt_basic_auth_users, basic_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Routers
app.include_router(products.router)
app.include_router(users.router)
# app.include_router(basic_auth_users.router)
app.include_router(jwt_basic_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def greetings():
    return {
        "message": "Hello FastAPI!"
    }

@app.get("/url")
async def url():
    return {
        "url_curso": "https://mouredev.com/python"
    }

