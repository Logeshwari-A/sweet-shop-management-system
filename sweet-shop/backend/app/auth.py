from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from .schemas import UserCreate, Token, UserOut
from .db import users_collection
from .core import settings
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/api/auth", tags=["auth"])

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    is_admin = False
    if user.admin_secret and user.admin_secret == settings.ADMIN_SECRET:
        is_admin = True

    hashed = pwd_context.hash(user.password)
    doc = {"username": user.username, "email": user.email, "password_hash": hashed, "is_admin": is_admin}
    res = await users_collection.insert_one(doc)
    return {"id": str(res.inserted_id), "username": user.username, "email": user.email, "is_admin": is_admin}

@router.post("/login", response_model=Token)
async def login(form: UserCreate):
    # login uses email and password
    user = await get_user_by_email(form.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user["_id"]), "exp": expire}
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
