from fastapi import FastAPI
from app.database import engine, Base

# Import all models to ensure they are registered with Base
from app.models import *

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Customer Support API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Customer Support API!"}
