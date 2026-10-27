from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.services import restaurant_service

# 1. Router Setup
router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

# 2. CREATE: POST /restaurants/
@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    return restaurant_service.create_restaurant(db, restaurant)

# 3. READ ALL: GET /restaurants/
@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return restaurant_service.get_restaurants(db, skip=skip, limit=limit)

# 4. READ ONE: GET /restaurants/{restaurant_id}
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = restaurant_service.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# 5. UPDATE: PUT /restaurants/{restaurant_id}
@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, update_data: RestaurantUpdate, db: Session = Depends(get_db)):
    updated = restaurant_service.update_restaurant(db, restaurant_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

# 6. DELETE: DELETE /restaurants/{restaurant_id}
@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    success = restaurant_service.delete_restaurant(db, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}

