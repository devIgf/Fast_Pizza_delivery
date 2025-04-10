from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class signUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: bool | None = False
    is_active: bool | None = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "juste_monace",
                "email": "moa@gmail.com",
                "password": "password123",
                "is_staff": False,
                "is_active": True
            }
        }



class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "juste_monace",
                "password": "password123"
            }
        }