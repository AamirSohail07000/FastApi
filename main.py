from fastapi import FastAPI
from models import *

app = FastAPI()

@app.get("/")
def greet():
  return "Welcome to homepage"

products = [
  Products(id=1, name="phone", description="budget phone", price=105, quantity=12),
  Products(id=2, name="laptop", description="gaming laptop", price=5000, quantity=5),
  Products(id=3, name="charger", description="fast charger", price=15, quantity=25),
  Products(id=4, name="battery", description="long life battery", price=25, quantity=8),
]

@app.get("/products")
def get_all_products():
  return products