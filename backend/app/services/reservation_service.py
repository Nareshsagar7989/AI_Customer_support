import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transactions import Reservation, ReservationStatusEnum
from app.models.users import Customer
from app.schemas.reservations import ReservationCreate, ReservationBookRequest

def get_reservations(db: Session, restaurant_id: int):
    return db.query(Reservation).filter(Reservation.restaurant_id == restaurant_id).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    conf_code = str(uuid.uuid4())[:8].upper()
    db_reservation = Reservation(
        **reservation.model_dump(),
        status=ReservationStatusEnum.PENDING,
        confirmation_code=conf_code
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def book_table_dynamically(db: Session, book_req: ReservationBookRequest):
    """
    Dynamically finds or creates customer in MySQL, then books reservation.
    Zero static customer IDs!
    """
    # 1. Find or create customer
    customer = db.query(Customer).filter(Customer.phone == book_req.phone.strip()).first()
    if not customer:
        customer = Customer(
            restaurant_id=book_req.restaurant_id,
            name=book_req.customer_name.strip(),
            phone=book_req.phone.strip(),
            notes="Web Dine-in customer"
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # 2. Compute 2 hours end_time
    combined_start = datetime.combine(book_req.reservation_date, book_req.start_time)
    end_time = (combined_start + timedelta(hours=2)).time()

    conf_code = "CONF-" + str(uuid.uuid4())[:6].upper()

    db_res = Reservation(
        restaurant_id=book_req.restaurant_id,
        customer_id=customer.id,
        reservation_date=book_req.reservation_date,
        start_time=book_req.start_time,
        end_time=end_time,
        party_size=book_req.party_size,
        status=ReservationStatusEnum.CONFIRMED,
        special_request=book_req.special_request,
        confirmation_code=conf_code
    )
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

def update_reservation_status(db: Session, reservation_id: int, status: ReservationStatusEnum):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        reservation.status = status
        db.commit()
        db.refresh(reservation)
    return reservation
