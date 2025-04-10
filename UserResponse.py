from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: Optional[int]
    username: str
    email: str
    is_staff: bool
    is_active: bool

class ResponseMessage(BaseModel):
    message: str
    user: UserResponse

    class Config:
        schema_extra = {
            "example": {
                "message": "User created successfully",
                "user": {
                    "id": 1,
                    "username": "juste_monace",
                    "email": "moa@gmail.com",
                    "is_staff": False,
                    "is_active": True
                }
            }
        }
