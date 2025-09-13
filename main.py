from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import *
from config import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)
# Create FastAPI application instance
app = FastAPI()

# Middleware 
app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],
   allow_methods = ["*"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def init_db():
  db = SessionLocal()

  existing_count = db.query(database_models.Product).count()

  if existing_count == 0:
    for product in products:
      db.add(database_models.Product(**product.model_dump()))
    db.commit()
    print("Database initialized with sample products.")

  db.close()  

init_db()    

# return the list of all products defined above
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): # Dependency injection

  db_products = db.query(database_models.Product).all()
  return db_products

# Read product
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)): # Dependency injection
  db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
  if db_product:
    return db_product
  return "Product not found"  

# Add product
@app.post("/products")
def add_product(product : Product, db: Session = Depends(get_db)): # Dependency injection
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product
    
# Update product, First check if product is there in db , then update it
@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)): # Dependency injection

  db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
  if db_product:
     db_product.name = product.name
     db_product.description = product.description
     db_product.price = product.price
     db_product.quantity = product.quantity
     db.commit()
     return "Product updated"
  else:  
    return "No product found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)): # Dependency injection
  db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
  if db_product:
      db.delete(db_product)
      db.commit()
      return "Product Deleted"
  else:
     return "Product not found"  