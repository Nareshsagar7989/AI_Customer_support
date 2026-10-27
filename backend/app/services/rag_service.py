import os
import chromadb
from app.data.knowledge_base import RESTAURANT_KNOWLEDGE

CHROMA_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

collection = chroma_client.get_or_create_collection(name="spice_garden_kb")


def init_knowledge_base():
    """
    Ingests initial restaurant policies, timings, and FAQs if not already present.
    """
    # Check if base policies are already present
    existing_count = collection.count()
    if existing_count > 0:
        print(f"ChromaDB already has {existing_count} items.")
        return

    print("Ingesting base knowledge into ChromaDB...")
    ids = [item["id"] for item in RESTAURANT_KNOWLEDGE]
    documents = [item["text"] for item in RESTAURANT_KNOWLEDGE]
    metadatas = [{"category": item["category"]} for item in RESTAURANT_KNOWLEDGE]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Successfully ingested {collection.count()} knowledge items into ChromaDB!")


def sync_menu_item_to_chroma(menu_item):
    """
    Real-time Dynamic Sync:
    Whenever an admin creates or edits a food item in MySQL,
    this function upserts (updates/inserts) the item directly into ChromaDB.
    """
    try:
        doc_id = f"menu_item_{menu_item.id}"
        dietary = "100% Vegetarian" if getattr(menu_item, 'is_vegetarian', False) else "Non-Vegetarian"
        if getattr(menu_item, 'is_vegan', False):
            dietary += ", Vegan"

        text = (
            f"Dish: {menu_item.name}. Price: ₹{menu_item.price}. "
            f"Description: {menu_item.description or 'Delicious chef specialty'}. "
            f"Dietary: {dietary}. Spice Level: {menu_item.spice_level or 'Medium'}. "
            f"Ingredients: {menu_item.ingredients or 'Fresh local ingredients'}. "
            f"Allergens: {menu_item.allergens or 'None reported'}. "
            f"Available: {'In Stock' if menu_item.is_available else 'Currently Out of Stock'}."
        )

        collection.upsert(
            ids=[doc_id],
            documents=[text],
            metadatas=[{
                "category": "menu",
                "item_id": menu_item.id,
                "restaurant_id": getattr(menu_item, 'restaurant_id', 1),
                "is_available": getattr(menu_item, 'is_available', True)
            }]
        )
        print(f"[RAG SYNC] Dynamically synced menu item '{menu_item.name}' (ID: {menu_item.id}) to ChromaDB.")
    except Exception as e:
        print(f"[RAG SYNC ERROR] Failed to sync menu item {menu_item.id} to ChromaDB: {e}")


def delete_menu_item_from_chroma(menu_item_id: int):
    """Removes a deleted food item from ChromaDB immediately."""
    try:
        doc_id = f"menu_item_{menu_item_id}"
        collection.delete(ids=[doc_id])
        print(f"[RAG SYNC] Deleted {doc_id} from ChromaDB.")
    except Exception as e:
        print(f"[RAG SYNC ERROR] Could not delete item {menu_item_id} from ChromaDB: {e}")


def search_knowledge_base(query: str, n_results: int = 3) -> list:
    """
    Retrieve Top-N relevant documents from ChromaDB based on semantic similarity.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    if results and "documents" in results and results["documents"]:
        return results["documents"][0]
    return []
