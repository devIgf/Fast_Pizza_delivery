from fastapi import APIRouter
from UserResponse import ResponseMessage
from database import engine
from schemas import signUpModel
from models import User
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(prefix="/auth", tags=["auth"])


session = Session(bind=engine)

@auth_router.get('')
async def hello_auth():
    return {"message": "Hello Auth"}



@auth_router.post('/signup', response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def signup(user: signUpModel):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_staff": new_user.is_staff,
            "is_active": new_user.is_active
        }
    }
