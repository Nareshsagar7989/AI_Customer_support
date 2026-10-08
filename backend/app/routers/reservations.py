from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.reservations import ReservationCreate, ReservationResponse
from app.services import reservation_service
from app.models.transactions import ReservationStatusEnum

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return reservation_service.create_reservation(db, reservation)

@router.get("/{restaurant_id}", response_model=List[ReservationResponse])
def get_reservations(restaurant_id: int, db: Session = Depends(get_db)):
    return reservation_service.get_reservations(db, restaurant_id)

@router.patch("/{reservation_id}/status", response_model=ReservationResponse)
def update_status(reservation_id: int, status: ReservationStatusEnum, db: Session = Depends(get_db)):
    res = reservation_service.update_reservation_status(db, reservation_id, status)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res
