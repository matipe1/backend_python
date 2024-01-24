from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=["Basic auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456" # Passwords must be encrypted (hashing or sth else)
    },
    "codiev2": {
        "username": "codiev2",
        "full_name": "Diego Petitto 2",
        "email": "codiev2@gmail.com",
        "disabled": True,
        "password": "456789" # Passwords must be encrypted (hashing or sth else)
    }
}


# Functions
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization credentials",
                            headers={"WWW-Autenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")

    return user


# Methods
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return { "access_token": user.username, "token_type": "bearer" }

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
