import uuid
from sqlalchemy.orm import Session
from app.models.transactions import Reservation, ReservationStatusEnum
from app.schemas.reservations import ReservationCreate

def get_reservations(db: Session, restaurant_id: int):
    return db.query(Reservation).filter(Reservation.restaurant_id == restaurant_id).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    # Generate a unique confirmation code automatically
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

def update_reservation_status(db: Session, reservation_id: int, status: ReservationStatusEnum):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        reservation.status = status
        db.commit()
        db.refresh(reservation)
    return reservation
