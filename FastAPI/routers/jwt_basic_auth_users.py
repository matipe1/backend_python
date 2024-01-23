from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "codiev": {
        "username": "codiev",
        "full_name": "Diego Petitto",
        "email": "codiev@gmail.com",
        "disabled": False,
        "password": "$2a$12$AF5vAL4Vnv/3Q9GUA.1W/uyInw7NCJHXG89ehHMvFbEvtaO3Lc5se" # Passwords must be encrypted (hashing or sth else)
    },
    "codiev2": {
        "username": "codiev2",
        "full_name": "Diego Petitto 2",
        "email": "codiev2@gmail.com",
        "disabled": True,
        "password": "$2a$14$c8l8nrHDEs334YDzDOs2GezMxyEJOdCQPMcDgH4am3WadyevzQQbG" # Passwords must be encrypted (hashing or sth else)
    }
}


# Functions
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

# Methods
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}