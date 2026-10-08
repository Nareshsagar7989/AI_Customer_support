from fastapi import FastAPI
from app.database import engine, Base

# Import all models to ensure they are registered with Base
from app.models import *

# Create all tables in the database
Base.metadata.create_all(bind=engine)

from app.routers import menu, reservations, orders, chat

app = FastAPI(title="AI Customer Support API")

# Register routers
app.include_router(menu.router)
app.include_router(reservations.router)
app.include_router(orders.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Customer Support API!"}
