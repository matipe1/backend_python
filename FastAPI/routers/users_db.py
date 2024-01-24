from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemes.user import user_scheme, users_scheme
from bson import ObjectId

router = APIRouter(prefix='/usersdb',
                   tags=['users_db'],
                   responses={status.HTTP_404_NOT_FOUND:{"error":"Not found"}})



# Call all the users
@router.get("/", response_model=list[User])
async def users_class():
    return users_scheme(db_client.local.users.find())


# Call a user
@router.get("/{id}") # Path
async def user(id: str):
    return search_user(key="_id", field=ObjectId(id))

@router.get("/{id}") # Query
async def user(id: str):
    return search_user(key="_id", field=ObjectId(id))



# Create a new user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user(key="username", field=user.username)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exists')

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_scheme(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)
    

# Replace a user
@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def user(user: User):

    user_dict = dict(user)
    try:
        
        db_client.local.users.find_one_and_replace(
            {
            "_id": ObjectId(user.id)
            }, user_dict)

    except:
        return {"error": "User has not been updated"}
    
    return search_user(key="_id", field=ObjectId(user.id))

# Is a good practice with puth method to update everything in the object
# And when you are not updating everything you should use patch


# Delete a user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "User not found"}



# Recycled functions
def search_user(key, field: str):
    try:
        user = db_client.local.users.find_one({key: field})
        return User(**user_scheme(user))

    except:
        return {"error": "User not found"}
