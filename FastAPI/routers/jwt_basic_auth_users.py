from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "127341iouok23jf2iof7u39usdf90audp12aposcjkasopcqoweruipo2b"


router = APIRouter(tags=["JWT Basic auth"])

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
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization credentials",
                            headers={"WWW-Autenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")

    return user


# Methods
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect password")

    access_token = {
        "sub": user.username, # Subject
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
