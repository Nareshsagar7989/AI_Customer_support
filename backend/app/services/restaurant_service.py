from sqlalchemy.orm import Session
from fastapi import HTTPException 
from app.models.restaurant import Restaurant 
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate 

def create_restaurant(db: Session, restaurant_data: RestaurantCreate):
    try:
        db_restaurant = Restaurant(**restaurant_data.model_dump())
        db.add(db_restaurant) 
        db.commit() 
        db.refresh(db_restaurant) 
        return db_restaurant 
    except Exception as e: 
        db.rollback() 
        raise HTTPException(status_code=500, detail = f"failed to create restaurant: {str(e)}")

def get_restaurant_by_id(db: Session, restaurant_id: int):
    try:
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first() 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail = f"failed to fetch the restaurant: {str(e)}") 

def get_restaurants(db:Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Restaurant).offset(skip).limit(limit).all() 
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail = f"failed to fetch the restaurant: {str(e)}") 

def update_restaurant(db: Session, restaurant_id: int, update_data: RestaurantUpdate):
    try:
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first() 

        if not db_restaurant:
            return None 
            
        for key, value in update_data.model_dump(exclude_unset=True).items(): 
            setattr(db_restaurant, key, value)  
        
        db.commit() 
        db.refresh(db_restaurant) 
        return db_restaurant   
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"failed to update restaurant: {str(e)}")


def delete_restaurant(db: Session, restaurant_id: int):
    try:
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not db_restaurant:
            return False

        db.delete(db_restaurant)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"failed to delete restaurant: {str(e)}")
