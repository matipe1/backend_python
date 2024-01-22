# Start server: uvicorn users:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# User entity
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str


# @app.get("/usersjson")
# async def users_json():
#     return [{
#         "name": "Diego",
#         "surname": "Petitto",
#         "age": 19,
#         "url": "https://diegol.dev"
#     },
#     {
#         "name": "Felipe",
#         "surname": "Lopez",
#         "age": 35,
#         "url": "https://felipe.com"
#     }]


# @app.get("/usersclass")
# async def users_class():
#     return User(name = "Diego", surname = "Petitto", age = 19, url = "https://diegol.dev")


users_fake_database = [User(id=1, name="Matias", surname="Peta", age=19, url="https://diegol.dev"), 
                       User(id=2, name="Silvio", surname="Batata", age=40, url="https://batata.com")]


# Call all the users
@app.get("/users")
async def users_class():
    return users_fake_database


# Recycle function
def search_user(id):
    users = filter(lambda user: user.id == id, users_fake_database)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}


# Call through Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

# Call through Query
@app.get("/user") # ThunderClient -> .../user/?id=1
async def user_query(id: int):
    return search_user(id)
