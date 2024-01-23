from fastapi import APIRouter


router = APIRouter(prefix="/products", tags=['products'], responses={404: {"msg": "Not found"}}) # Tag is for the documentation

products_fake_database = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]

# Return all products
@router.get("/")
async def products():
    return products_fake_database


# Return product by id (index)
@router.get("/{id}")
async def product(id: int):
    return products_fake_database[id - 1]