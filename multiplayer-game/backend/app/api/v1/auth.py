from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter()

fake_users_db = {}

class LoginData(BaseModel):
    username: str
    password: str

def create_token(username: str):
    exp = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(
        {"sub": username, "exp": exp},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

@router.post("/login")
def login( LoginData):
    if data.username not in fake_users_db or fake_users_db[data.username] != data.password:
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(data.username), "token_type": "bearer"}

@router.post("/signup")
def signup( LoginData):
    if data.username in fake_users_db:
        raise HTTPException(400, "User exists")
    fake_users_db[data.username] = data.password
    return {"access_token": create_token(data.username), "token_type": "bearer"}
