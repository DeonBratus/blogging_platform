from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from .models import UserCreate, Token
from blog_api.database_handler import UsersDB, get_database
from .auth import hash_password, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
app = APIRouter()

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_database)):
    existing_user = db.query(UsersDB).filter(UsersDB.username == user.username).first()
    if existing_user is not None:
        raise HTTPException(status_code=400)
    
    hashed_pwd = hash_password(user.password)
    new_user = UsersDB(username=user.username, email=user.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}