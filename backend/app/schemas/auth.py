from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: str
    message: Optional[str] = "Success"

    class Config:
        from_attributes = True
