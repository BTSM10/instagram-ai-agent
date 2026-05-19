from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from model import Users
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

class User(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register')
def register_user(db:db_dependency,user:User):
    create_user = Users(
        email = user.email,
        username = user.username,
        hashed_password = bcrypt_context.hash(user.password),
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        is_active = True    
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user
@router.post('/login')
def login(db:db_dependency, user:User ):
    if user is None: 
        raise HTTPException(status_code=401, detail = "Invalid Credentials")
    user = db.query(Users).filter(Users.email == user.email).first()
    if user is None: 
        raise HTTPException(status_code=401, detail = "Invalid Credentials")
    if not bcrypt_context.verify(user.password, user.hashed_password):
        raise HTTPException(status_code=401, detail = "Invalid Credentials")
    return user


