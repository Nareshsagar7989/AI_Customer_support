from sqlalchemy.orm import Session
from app.models.menu import MenuItem, MenuCategory
from app.schemas.menu import MenuItemCreate
from app.services.rag_service import sync_menu_item_to_chroma, delete_menu_item_from_chroma

def get_menu_items(db: Session, restaurant_id: int):
    """Fetch all active menu items for a restaurant."""
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

def get_categories(db: Session, restaurant_id: int):
    """Fetch dynamic menu categories from MySQL."""
    return db.query(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id).order_by(MenuCategory.display_order).all()

def create_menu_item(db: Session, item: MenuItemCreate):
    """
    Creates a new menu item in MySQL and instantly syncs it with ChromaDB RAG.
    """
    db_item = MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Real-time RAG sync
    sync_menu_item_to_chroma(db_item)
    return db_item

def update_menu_item(db: Session, item_id: int, update_data: dict):
    """Updates a menu item in MySQL and re-syncs to ChromaDB."""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return None

    for key, value in update_data.items():
        if hasattr(db_item, key) and value is not None:
            setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    
    # Real-time RAG sync
    sync_menu_item_to_chroma(db_item)
    return db_item

def delete_menu_item(db: Session, item_id: int):
    """Deletes menu item from MySQL and removes it from ChromaDB."""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    
    # Real-time RAG removal
    delete_menu_item_from_chroma(item_id)
    return True
