from fastapi import APIRouter, Depends
from UserResponse import ResponseMessage
from database import engine
from schemas import signUpModel, LoginModel
from models import User
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(prefix="/auth", tags=["auth"])


session = Session(bind=engine)


security = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(token.credentials)
    db_user = session.query(User).filter(User.username == payload["sub"]).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return db_user


# Configuration de la clé secrète et de l'algorithme
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


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



@auth_router.post('/login')
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not found")
    
    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Création d'un token JWT
    token = create_access_token(data={"sub": db_user.username})
    
    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active
        },
        "token": token
    }



# Exemple d'endpoint protégé
@auth_router.get('/protected')
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}