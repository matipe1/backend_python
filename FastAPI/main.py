# Documentation w/ Swagger: http://127.0.0.1:8000/docs
# Documentation w/ Redocly: http://127.0.0.1:8000/redoc

# Start server: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()


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

