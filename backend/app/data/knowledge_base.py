"""
Spice Garden Restaurant - General Knowledge Base (FAQs, Policies, Timings)
NOTE: Food items are NOT stored here! All menu items are managed dynamically in MySQL database.
"""

RESTAURANT_KNOWLEDGE = [
    # ----------------- 1. TIMINGS & LOCATION -----------------
    {
        "id": "timing_hours",
        "text": "Spice Garden Operating Hours: The restaurant is open 7 days a week, Monday through Sunday, from 11:00 AM to 11:00 PM. Lunch is served between 12:00 PM and 3:30 PM. Dinner is served between 7:00 PM and 11:00 PM. Last kitchen order is taken at 10:30 PM.",
        "category": "timings"
    },
    {
        "id": "location_address",
        "text": "Spice Garden Location & Address: We are located at Plot 45, HITEC City Main Road, Madhapur, Hyderabad, Telangana 500081. Landmark: Opposite Cyber Towers, near Madhapur Metro Station.",
        "category": "location"
    },
    {
        "id": "parking_facilities",
        "text": "Parking Facilities: We offer free valet parking for four-wheelers and dedicated parking space for two-wheelers. Safe underground parking is available with security guards.",
        "category": "amenities"
    },

    # ----------------- 2. RESERVATION & PAYMENT POLICIES -----------------
    {
        "id": "table_booking_policy",
        "text": "Table Reservation Policy: Customers can book tables online through our website or our AI assistant. We recommend booking at least 2 hours in advance during weekdays, and 4 hours in advance on weekends (Saturday & Sunday). Reserved tables are held for up to 15 minutes past the booking time before being released.",
        "category": "reservations"
    },
    {
        "id": "payment_methods",
        "text": "Payment Options: We accept UPI (Google Pay, PhonePe, Paytm), Credit and Debit Cards (Visa, MasterCard, Rupay, Amex), Cash, and Food Wallets (Sodexo, Pluxee, Edenred). We do not accept international currency.",
        "category": "payments"
    },
    {
        "id": "home_delivery_policy",
        "text": "Home Delivery & Takeaway: We offer home delivery within a 7 km radius of Madhapur. Delivery is free for orders above ₹500; a delivery fee of ₹40 applies for orders below ₹500. Delivery usually takes 35 to 45 minutes.",
        "category": "delivery"
    },

    # ----------------- 3. SPECIAL DIETARY & AMENITIES -----------------
    {
        "id": "dietary_options",
        "text": "Dietary Preferences: We have 100% Halal certified meat. We also have a strictly separate kitchen section for pure Vegetarian and Jain food preparation. Gluten-free and Vegan options are marked on the menu.",
        "category": "dietary"
    },
    {
        "id": "wifi_and_ambience",
        "text": "Amenities: High-speed complimentary Wi-Fi is available for all guests. The restaurant has air-conditioned indoor dining, an open-air rooftop section, and a private party hall with capacity up to 40 guests.",
        "category": "amenities"
    }
]
