# Start server: uvicorn users:app --reload

from fastapi import FastAPI, HTTPException
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


# Call through Path
# Mostly used when you consider the parameter is obligatory (good practices)
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

# Call through Query
# Mostly used when you consider the parameter is not necessary (good practices)
@app.get("/user") # ThunderClient -> .../user/?id=1
async def user_query(id: int):
    return search_user(id)


# The example above is not a good practice with query
# The path with query should be .../user/1/?service=1 (quite a good practice)

# Create a new user
@app.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail='User already exists')
    else:
        users_fake_database.append(user)
        return {"msg": "A new user has been added"}


# Is a good practice with puth method to update everything in the object
# And when you are not updating everything you should use patch
    
# Update a user
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_fake_database):
        if saved_user.id == user.id:
            users_fake_database[index] = user
            found = True
        
    if not found:
        return {"error": "User not found"}
    

@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_fake_database):
        if saved_user.id == id:
            del users_fake_database[index]
            found = True
        
    if not found:
        return {"error": "User not found"}



# Recycled functions
def search_user(id):
    users = filter(lambda user: user.id == id, users_fake_database)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}

