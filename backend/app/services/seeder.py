import logging
from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant, RestaurantTable
from app.models.menu import MenuCategory, MenuItem

logger = logging.getLogger("seeder")

def seed_initial_data(db: Session):
    """
    Auto-seeds base restaurant details, tables, categories, and signature dishes
    if the database is newly initialized (e.g., fresh cloud MySQL on Render/Aiven).
    Safe & idempotent: will only insert rows that do not already exist.
    """
    try:
        # 1. Ensure Restaurant with ID 1 exists
        restaurant = db.query(Restaurant).filter(Restaurant.id == 1).first()
        if not restaurant:
            restaurant = Restaurant(
                id=1,
                name="Spice Garden",
                description="Authentic Indian & Hyderabadi Fine Dining experience.",
                logo_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&auto=format&fit=crop&q=60",
                phone="+919876543210",
                email="contact@spicegarden.com",
                website="https://spicegarden.com",
                address="Madhapur, HITEC City",
                city="Hyderabad",
                state="Telangana",
                pincode="500081",
                is_active=True
            )
            db.add(restaurant)
            db.commit()
            db.refresh(restaurant)
            print("[SEEDER] Created base Restaurant (ID: 1, Spice Garden)")

        # 2. Ensure Restaurant Tables exist
        if db.query(RestaurantTable).filter(RestaurantTable.restaurant_id == 1).count() == 0:
            tables = [
                RestaurantTable(restaurant_id=1, table_number="T1", capacity=2, location="Indoor", status="AVAILABLE"),
                RestaurantTable(restaurant_id=1, table_number="T2", capacity=4, location="Indoor", status="AVAILABLE"),
                RestaurantTable(restaurant_id=1, table_number="T3", capacity=6, location="Indoor", status="AVAILABLE"),
                RestaurantTable(restaurant_id=1, table_number="T4", capacity=4, location="Rooftop", status="AVAILABLE"),
            ]
            db.add_all(tables)
            db.commit()
            print("[SEEDER] Created default Restaurant Tables (T1-T4)")

        # 3. Ensure Menu Categories exist
        categories_data = [
            (1, "Biryani & Rice", "Fragrant royal basmati rice preparations & dum biryanis", 1),
            (2, "Starters", "Crispy appetizing starters & tandoori platters", 2),
            (3, "Curries & Gravies", "Rich Mughlai and Indian curries", 3),
            (4, "Breads", "Clay tandoor fresh rotis, naans and parathas", 4),
            (5, "Desserts & Drinks", "Traditional Indian sweets and refreshing coolers", 5),
        ]
        for cat_id, cat_name, cat_desc, order in categories_data:
            cat = db.query(MenuCategory).filter(MenuCategory.id == cat_id).first()
            if not cat:
                cat = MenuCategory(
                    id=cat_id,
                    restaurant_id=1,
                    name=cat_name,
                    description=cat_desc,
                    display_order=order,
                    is_active=True
                )
                db.add(cat)
        db.commit()

        # 4. Ensure Menu Items exist
        if db.query(MenuItem).filter(MenuItem.restaurant_id == 1).count() == 0:
            dishes = [
                MenuItem(
                    id=2,
                    restaurant_id=1,
                    category_id=1,
                    name="Chicken Biryani",
                    description="Classic spiced rice cooked with succulent chicken and aromatic herbs.",
                    price=500.0,
                    image_url="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="High",
                    ingredients="Chicken, Basmati Rice, Chilli Masala, Ghee",
                    allergens="Dairy",
                    is_available=True,
                    preparation_time=20
                ),
                MenuItem(
                    id=3,
                    restaurant_id=1,
                    category_id=1,
                    name="Hyderabadi Chicken Dum Biryani",
                    description="Aromatic basmati rice slow-cooked with tender spiced chicken, saffron, and fried onions. Served with Mirchi Ka Salan and Raita.",
                    price=380.0,
                    image_url="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="High",
                    ingredients="Chicken, Basmati Rice, Saffron, Ghee, Mint, Spices",
                    allergens="Dairy (Ghee, Curd)",
                    is_available=True,
                    preparation_time=25
                ),
                MenuItem(
                    id=4,
                    restaurant_id=1,
                    category_id=1,
                    name="Special Mutton Dum Biryani",
                    description="Royal Nizam recipe with succulent baby goat meat layered with fragrant long-grain rice and whole spices.",
                    price=450.0,
                    image_url="https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="Medium-High",
                    ingredients="Goat Mutton, Basmati Rice, Fried Onions, Saffron, Shahi Masala",
                    allergens="Dairy (Ghee)",
                    is_available=True,
                    preparation_time=30
                ),
                MenuItem(
                    id=5,
                    restaurant_id=1,
                    category_id=1,
                    name="Paneer Dum Biryani",
                    description="Soft malai paneer cubes marinated in yogurt and herbs, layered with dum-cooked basmati rice and saffron milk.",
                    price=320.0,
                    image_url="https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Medium",
                    ingredients="Cottage Cheese (Paneer), Rice, Herbs, Ghee, Mint",
                    allergens="Dairy (Paneer, Ghee)",
                    is_available=True,
                    preparation_time=20
                ),
                MenuItem(
                    id=6,
                    restaurant_id=1,
                    category_id=2,
                    name="Hyderabadi Chicken 65",
                    description="Crispy golden fried chicken chunks tossed with tempered curry leaves, green chillies, and tangy yogurt masala.",
                    price=310.0,
                    image_url="https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="High",
                    ingredients="Boneless Chicken, Curry leaves, Kashmiri chilli, Yogurt",
                    allergens="Egg, Dairy",
                    is_available=True,
                    preparation_time=15
                ),
                MenuItem(
                    id=7,
                    restaurant_id=1,
                    category_id=2,
                    name="Tandoori Paneer Tikka",
                    description="Smoky char-grilled cottage cheese cubes marinated in tandoori spices, served with bell peppers, onion rings, and mint chutney.",
                    price=280.0,
                    image_url="https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Medium",
                    ingredients="Paneer, Capsicum, Onion, Tandoori Masala, Mustard oil",
                    allergens="Dairy",
                    is_available=True,
                    preparation_time=18
                ),
                MenuItem(
                    id=8,
                    restaurant_id=1,
                    category_id=3,
                    name="Butter Chicken (Murgh Makhani)",
                    description="Tender tandoori chicken simmered in a velvet-smooth makhani gravy of vine-ripened tomatoes, butter, and cashew cream.",
                    price=360.0,
                    image_url="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="Mild",
                    ingredients="Chicken, Butter, Cream, Cashew paste, Tomatoes, Kasuri methi",
                    allergens="Dairy, Nuts (Cashew)",
                    is_available=True,
                    preparation_time=20
                ),
                MenuItem(
                    id=9,
                    restaurant_id=1,
                    category_id=3,
                    name="Royal Dal Makhani",
                    description="Black urad lentils and kidney beans slow-simmered overnight over charcoal embers, finished with churned butter and fresh cream.",
                    price=260.0,
                    image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Mild",
                    ingredients="Black lentils, Rajma, Butter, Cream, Spices",
                    allergens="Dairy",
                    is_available=True,
                    preparation_time=15
                ),
                MenuItem(
                    id=10,
                    restaurant_id=1,
                    category_id=4,
                    name="Garlic Butter Naan",
                    description="Traditional clay tandoor baked leavened bread brushed generously with garlic butter and fresh coriander.",
                    price=65.0,
                    image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Mild",
                    ingredients="Refined flour, Fresh Garlic, Butter, Coriander",
                    allergens="Gluten, Dairy",
                    is_available=True,
                    preparation_time=8
                ),
                MenuItem(
                    id=11,
                    restaurant_id=1,
                    category_id=5,
                    name="Hot Gulab Jamun with Ice Cream",
                    description="Warm golden khoya dumplings steeped in rose cardamom syrup, served alongside rich creamy vanilla ice cream.",
                    price=140.0,
                    image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Sweet",
                    ingredients="Khoya, Sugar, Rose water, Cardamom, Vanilla Ice Cream",
                    allergens="Dairy, Gluten",
                    is_available=True,
                    preparation_time=5
                ),
                MenuItem(
                    id=12,
                    restaurant_id=1,
                    category_id=5,
                    name="Alphonso Mango Lassi",
                    description="Thick chilled sweet yogurt blended with authentic Ratnagiri Alphonso mango pulp and sprinkled with slivered pistachios.",
                    price=120.0,
                    image_url="https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=True,
                    is_vegan=False,
                    spice_level="Sweet",
                    ingredients="Yogurt, Alphonso Mango, Sugar, Pistachio",
                    allergens="Dairy, Nuts (Pistachio)",
                    is_available=True,
                    preparation_time=5
                ),
                MenuItem(
                    id=13,
                    restaurant_id=1,
                    category_id=1,
                    name="Mutton Biryani",
                    description="Aromatic and well-cooked royal mutton biryani prepared with choice spices.",
                    price=600.0,
                    image_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=60",
                    is_vegetarian=False,
                    is_vegan=False,
                    spice_level="Medium",
                    ingredients="Mutton, Basmati Rice, Spices, Ghee",
                    allergens="Dairy",
                    is_available=True,
                    preparation_time=20
                )
            ]
            db.add_all(dishes)
            db.commit()
            print(f"[SEEDER] Successfully seeded {len(dishes)} signature menu items.")
        
        print("[SEEDER] Database check completed. All base entities are healthy.")
    except Exception as e:
        db.rollback()
        print(f"[SEEDER ERROR] Error running database seeder: {e}")
