import hashlib
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User, Customer
from app.models.restaurant import Restaurant
from app.schemas.auth import UserRegister, UserLogin, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

HARDCODED_ADMIN_USERNAME = "ADMIN370"
HARDCODED_ADMIN_PASSWORD = "Admin@370"

def hash_password(password: str) -> str:
    """Returns 64-character hexadecimal SHA-256 hash of the password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

HARDCODED_DEMO_CUST_USERNAME = "customer_demo"
HARDCODED_DEMO_CUST_PASSWORD = "Customer@123"

def ensure_admin_exists(db: Session):
    """Ensures the hardcoded admin and demo customer accounts exist in MySQL."""
    # 1. Admin
    admin = db.query(User).filter(User.username == HARDCODED_ADMIN_USERNAME).first()
    if not admin:
        admin_hash = hash_password(HARDCODED_ADMIN_PASSWORD)
        admin = User(
            username=HARDCODED_ADMIN_USERNAME,
            name="Spice Garden Admin",
            password_hash=admin_hash,
            role="ADMIN",
            phone="9999999999",
            email="admin370@spicegarden.com"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    # 2. Demo Customer for 1-Click recruiter testing
    demo_cust = db.query(User).filter(User.username == HARDCODED_DEMO_CUST_USERNAME).first()
    if not demo_cust:
        cust_hash = hash_password(HARDCODED_DEMO_CUST_PASSWORD)
        demo_cust = User(
            username=HARDCODED_DEMO_CUST_USERNAME,
            name="Rahul Sharma",
            password_hash=cust_hash,
            role="CUSTOMER",
            phone="9876543210",
            email="rahul@example.com"
        )
        db.add(demo_cust)
        db.commit()
        
        # Link to customer table as well
        existing_c = db.query(Customer).filter(Customer.phone == "9876543210").first()
        if not existing_c:
            c = Customer(
                restaurant_id=1,
                name="Rahul Sharma",
                phone="9876543210",
                email="rahul@example.com",
                notes="Demo customer account"
            )
            db.add(c)
            db.commit()

    return admin

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    clean_username = user_data.username.strip()
    if not clean_username or not user_data.password:
        raise HTTPException(status_code=400, detail="Username and password are required.")

    if clean_username.upper() == HARDCODED_ADMIN_USERNAME.upper():
        raise HTTPException(status_code=400, detail="This username is reserved for system administration.")

    existing_user = db.query(User).filter(User.username == clean_username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already registered. Please choose another username.")

    # 64-character SHA-256 hash
    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        username=clean_username,
        name=user_data.name.strip(),
        phone=user_data.phone.strip() if user_data.phone else None,
        email=user_data.email.strip() if user_data.email else None,
        password_hash=hashed_pwd,
        role="CUSTOMER"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Also link or create Customer record for order history
    if user_data.phone:
        restaurant = db.query(Restaurant).first()
        rest_id = restaurant.id if restaurant else 1
        existing_cust = db.query(Customer).filter(Customer.phone == user_data.phone.strip()).first()
        if not existing_cust:
            new_cust = Customer(
                restaurant_id=rest_id,
                name=user_data.name.strip(),
                phone=user_data.phone.strip(),
                email=user_data.email.strip() if user_data.email else None,
                notes=f"Registered account: {clean_username}"
            )
            db.add(new_cust)
            db.commit()

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        name=new_user.name,
        phone=new_user.phone,
        email=new_user.email,
        role=new_user.role,
        message="Registration successful! You can now log in."
    )

@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    input_username = credentials.username.strip()
    input_password = credentials.password

    # 1. Hardcoded Admin Login Check
    if input_username == HARDCODED_ADMIN_USERNAME and input_password == HARDCODED_ADMIN_PASSWORD:
        admin = ensure_admin_exists(db)
        return UserResponse(
            id=admin.id,
            username=admin.username,
            name=admin.name,
            phone=admin.phone,
            email=admin.email,
            role="ADMIN",
            message="Admin login successful!"
        )

    # 2. General Database User Login (Customer or Admin)
    user = db.query(User).filter(User.username == input_username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    # Compare 64-character SHA-256 hashes
    input_hash = hash_password(input_password)
    if user.password_hash != input_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        phone=user.phone,
        email=user.email,
        role=user.role,
        message="Login successful!"
    )
