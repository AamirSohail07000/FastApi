from fastapi import FastAPI
from models import *

# Create FastAPI application instance
app = FastAPI()

# Root endpoint
@app.get("/")
def greet():
  return "Welcome to homepage"

# Sample data (acting like a temporary database)
# Each item is created using the Products model
products = [
  Product(id=1, name="phone", description="budget phone", price=105, quantity=12),
  Product(id=2, name="laptop", description="gaming laptop", price=5000, quantity=5),
  Product(id=3, name="charger", description="fast charger", price=15, quantity=25),
  Product(id=4, name="battery", description="long life battery", price=25, quantity=8),
]

# return the list of all products defined above
@app.get("/products")
def get_all_products():
  return products

# Read product
@app.get("/product/{id}")
def get_product_by_id(id: int):
  for product in products:
    if product.id == id:
      return product
  return "Product not found"  

# Add product
@app.post("/product")
def add_product(product : Product):
    products.append(product)
    return product

# Update product
@app.put("/product")
def update_product(id: int, product: Product):
  for i in range(len(products)):
    if products[i].id == id:
      products[i] = product
      return "Product Added Successfully"

  return "No product found"

@app.delete("/product")
def delete_product(id: int):
  for i in range(len(products)):
    if products[i].id == id:
      del products[i]
      return "Product Deleted"
  return "Product not found"  