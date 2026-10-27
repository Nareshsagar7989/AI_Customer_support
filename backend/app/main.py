from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base, SessionLocal
from app.models import *
from app.routers import menu, reservations, orders, chat, restaurant, auth
from app.routers.auth import ensure_admin_exists
from app.services.rag_service import init_knowledge_base, sync_menu_item_to_chroma

# Create all tables in the database
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize RAG and sync any existing MySQL dishes to ChromaDB
    try:
        init_knowledge_base()
        db = SessionLocal()
        ensure_admin_exists(db)
        from app.models.menu import MenuItem
        items = db.query(MenuItem).all()
        for item in items:
            sync_menu_item_to_chroma(item)
        db.close()
        print(f"[STARTUP] Synchronized {len(items)} MySQL menu items into ChromaDB and ensured ADMIN370 exists.")
    except Exception as e:
        print(f"[STARTUP ERROR] Error syncing RAG: {e}")
    yield

app = FastAPI(title="AI Customer Support API", lifespan=lifespan)

# Enable CORS for React Frontend (Universal Deployment Compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(restaurant.router)
app.include_router(menu.router)
app.include_router(reservations.router)
app.include_router(orders.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Customer Support API!"}
