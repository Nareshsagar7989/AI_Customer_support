import json
import uuid
from datetime import datetime, time, date, timedelta
from app.database import SessionLocal
from app.models.transactions import (
    Order, OrderItem, OrderTypeEnum, OrderStatusEnum, 
    Reservation, ReservationStatusEnum
)
from app.models.menu import MenuItem
from app.models.users import Customer
from app.models.restaurant import Restaurant

# ============================================================================
# 1. ACTUAL PYTHON TOOL IMPLEMENTATIONS (Database Operations)
# ============================================================================

def tool_get_order_status(order_number: str) -> dict:
    """Queries MySQL database to fetch the live status and details of an order."""
    db = SessionLocal()
    try:
        clean_order_num = order_number.strip().upper()
        order = db.query(Order).filter(Order.order_number == clean_order_num).first()
        
        if not order:
            return {
                "success": False,
                "message": f"Order with number '{clean_order_num}' not found. Please verify the order number."
            }
            
        return {
            "success": True,
            "order_number": order.order_number,
            "status": order.status.value,
            "total_amount": f"₹{order.total_amount}",
            "payment_status": order.payment_status,
            "order_type": order.order_type.value,
            "created_at": order.created_at.strftime("%I:%M %p, %d %b %Y")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()


def tool_book_table(customer_name: str, phone: str, reservation_date: str, reservation_time: str, party_size: int, special_request: str = "") -> dict:
    """Inserts a new table reservation into MySQL and returns confirmation code."""
    db = SessionLocal()
    try:
        # Default restaurant ID 1 ("Spice Garden")
        restaurant = db.query(Restaurant).first()
        rest_id = restaurant.id if restaurant else 1

        # Find or create customer
        customer = db.query(Customer).filter(Customer.phone == phone.strip()).first()
        if not customer:
            customer = Customer(
                restaurant_id=rest_id,
                name=customer_name.strip(),
                phone=phone.strip(),
                notes="Booked via AI Assistant"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Parse Date & Time
        res_date = datetime.strptime(reservation_date.strip(), "%Y-%m-%d").date()
        try:
            res_time = datetime.strptime(reservation_time.strip(), "%H:%M").time()
        except ValueError:
            res_time = datetime.strptime(reservation_time.strip(), "%I:%M %p").time()

        # End time (2 hours duration by default)
        end_time = (datetime.combine(res_date, res_time) + timedelta(hours=2)).time()

        # Generate unique confirmation code (e.g. CONF-7F3A2B)
        conf_code = "CONF-" + str(uuid.uuid4())[:6].upper()

        new_reservation = Reservation(
            restaurant_id=rest_id,
            customer_id=customer.id,
            reservation_date=res_date,
            start_time=res_time,
            end_time=end_time,
            party_size=party_size,
            status=ReservationStatusEnum.CONFIRMED,
            special_request=special_request,
            confirmation_code=conf_code
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

        return {
            "success": True,
            "message": "Table booked successfully!",
            "confirmation_code": conf_code,
            "customer_name": customer_name,
            "party_size": party_size,
            "date": str(res_date),
            "time": res_time.strftime("%I:%M %p"),
            "status": "CONFIRMED"
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Failed to book table: {str(e)}"}
    finally:
        db.close()


def tool_place_delivery_order(
    customer_name: str, 
    phone: str, 
    delivery_address: str, 
    items: list, 
    special_instructions: str = "",
    payment_method: str = "CASH_ON_DELIVERY"
) -> dict:
    """
    Places a food home delivery order directly into MySQL.
    Calculates dynamic prices from MySQL MenuItem table.
    """
    import re
    db = SessionLocal()
    try:
        # Default restaurant (Spice Garden)
        restaurant = db.query(Restaurant).first()
        rest_id = restaurant.id if restaurant else 1

        # 1. Find or create Customer in DB
        clean_phone = phone.strip()
        customer = db.query(Customer).filter(Customer.phone == clean_phone).first()
        if not customer:
            customer = Customer(
                restaurant_id=rest_id,
                name=customer_name.strip(),
                phone=clean_phone,
                notes=f"Delivery Address: {delivery_address.strip()}",
                total_orders=1
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        else:
            customer.total_orders = (customer.total_orders or 0) + 1
            if customer_name and not customer.name:
                customer.name = customer_name.strip()
            db.commit()

        # 2. Match items and calculate pricing dynamically
        order_items_data = []
        subtotal = 0.0

        for item_entry in items:
            if isinstance(item_entry, dict):
                item_name = str(item_entry.get("name", "")).strip()
                try:
                    qty = int(item_entry.get("quantity", 1))
                except (ValueError, TypeError):
                    qty = 1
            elif isinstance(item_entry, str):
                match = re.match(r"^(\d+)\s*(?:x\s*)?(.*)$", item_entry.strip())
                if match:
                    qty = int(match.group(1))
                    item_name = match.group(2).strip()
                else:
                    qty = 1
                    item_name = item_entry.strip()
            else:
                continue

            if qty <= 0:
                qty = 1

            # Match item from MySQL menu_items
            matched_item = db.query(MenuItem).filter(
                MenuItem.name.ilike(f"%{item_name}%"),
                MenuItem.restaurant_id == rest_id
            ).first()

            if not matched_item:
                words = [w for w in item_name.split() if len(w) > 3]
                for kw in words:
                    matched_item = db.query(MenuItem).filter(
                        MenuItem.name.ilike(f"%{kw}%"),
                        MenuItem.restaurant_id == rest_id
                    ).first()
                    if matched_item:
                        break

            if matched_item:
                unit_price = float(matched_item.price)
                item_total = round(unit_price * qty, 2)
                subtotal += item_total
                order_items_data.append({
                    "menu_item_id": matched_item.id,
                    "item_name": matched_item.name,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "total_price": item_total
                })
            else:
                return {
                    "success": False,
                    "error": f"Item '{item_name}' was not found in our restaurant menu. Please verify items from the menu."
                }

        if not order_items_data:
            return {
                "success": False,
                "error": "No valid food items were provided to place the order."
            }

        # 3. Financial calculations
        tax = round(subtotal * 0.05, 2)  # 5% GST
        delivery_fee = 0.0 if subtotal >= 500 else 40.0  # Free delivery over ₹500
        discount = 0.0
        total_amount = round(subtotal + tax + delivery_fee - discount, 2)

        # 4. Generate unique order tracking number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        # 5. Save Order to MySQL
        new_order = Order(
            restaurant_id=rest_id,
            customer_id=customer.id,
            order_number=order_number,
            order_type=OrderTypeEnum.DELIVERY,
            status=OrderStatusEnum.PLACED,
            subtotal=subtotal,
            tax=tax,
            delivery_fee=delivery_fee,
            discount=discount,
            total_amount=total_amount,
            delivery_address=delivery_address.strip(),
            payment_status="CASH_ON_DELIVERY"
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # 6. Save OrderItems to MySQL
        for it in order_items_data:
            db_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=it["menu_item_id"],
                quantity=it["quantity"],
                unit_price=it["unit_price"],
                total_price=it["total_price"],
                special_instructions=special_instructions
            )
            db.add(db_item)

        db.commit()

        return {
            "success": True,
            "message": "Home delivery order booked successfully!",
            "order_number": order_number,
            "customer_name": customer.name,
            "phone": customer.phone,
            "delivery_address": delivery_address.strip(),
            "items": [
                f"{it['quantity']}x {it['item_name']} (₹{it['total_price']})"
                for it in order_items_data
            ],
            "subtotal": f"₹{subtotal:.2f}",
            "tax": f"₹{tax:.2f} (5% GST)",
            "delivery_fee": f"₹{delivery_fee:.2f}" if delivery_fee > 0 else "FREE",
            "total_amount": f"₹{total_amount:.2f}",
            "payment_status": "Cash on Delivery",
            "estimated_delivery_time": "35-45 minutes",
            "status": "PLACED"
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Failed to place delivery order: {str(e)}"}
    finally:
        db.close()


# ============================================================================
# 2. TOOL DEFINITIONS FOR LLM (Groq / OpenAI JSON Schema)
# ============================================================================

AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Check the current status and details of a customer's food order using their unique order number (e.g., ORD-12345678).",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "string",
                        "description": "The unique order tracking number provided to the customer, e.g., 'ORD-12345678' or 'ORD-ABCDEF12'."
                    }
                },
                "required": ["order_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_table",
            "description": "Book a dining table reservation at Spice Garden restaurant for a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the customer booking the table."
                    },
                    "phone": {
                        "type": "string",
                        "description": "Customer contact phone number (10 digits)."
                    },
                    "reservation_date": {
                        "type": "string",
                        "description": "The date of the reservation in YYYY-MM-DD format (e.g., '2026-10-25')."
                    },
                    "reservation_time": {
                        "type": "string",
                        "description": "The start time of the reservation in 24-hour HH:MM format (e.g., '19:30' for 7:30 PM) or '07:30 PM'."
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "Number of guests/people for the reservation (e.g., 2, 4, 6)."
                    },
                    "special_request": {
                        "type": "string",
                        "description": "Any special preferences such as window seat, outdoor, high chair, birthday decoration, etc."
                    }
                },
                "required": ["customer_name", "phone", "reservation_date", "reservation_time", "party_size"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_delivery_order",
            "description": "Place a food home delivery order for a customer directly in the system. CRITICAL: ONLY invoke this tool AFTER the customer has provided ALL 4 required pieces of information: (1) food items with quantities, (2) customer name, (3) phone number, and (4) complete delivery address. If any of these are missing, DO NOT call this tool; ask the customer for the missing details first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the customer placing the order."
                    },
                    "phone": {
                        "type": "string",
                        "description": "Customer contact phone number (10 digits)."
                    },
                    "delivery_address": {
                        "type": "string",
                        "description": "Complete physical address for food delivery including flat/house number, street, or landmark."
                    },
                    "items": {
                        "type": "array",
                        "description": "List of dishes/food items to order with their quantities.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the dish or menu item (e.g. 'Hyderabadi Chicken Biryani', 'Butter Naan')."
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Number of portions (e.g. 1, 2)."
                                }
                            },
                            "required": ["name", "quantity"]
                        }
                    },
                    "special_instructions": {
                        "type": "string",
                        "description": "Optional instructions for food preparation or delivery."
                    }
                },
                "required": ["customer_name", "phone", "delivery_address", "items"]
            }
        }
    }
]


# ============================================================================
# 3. TOOL DISPATCHER (Executes whichever tool the AI decides to call)
# ============================================================================

def execute_tool(tool_name: str, arguments: dict) -> str:
    """Executes the tool requested by the AI agent and returns the JSON string result."""
    if tool_name == "get_order_status":
        result = tool_get_order_status(**arguments)
    elif tool_name == "book_table":
        result = tool_book_table(**arguments)
    elif tool_name == "place_delivery_order":
        result = tool_place_delivery_order(**arguments)
    else:
        result = {"error": f"Tool '{tool_name}' is not recognized."}
        
    return json.dumps(result)

