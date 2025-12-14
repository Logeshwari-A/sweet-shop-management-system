from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    admin_secret: Optional[str] = None

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SweetIn(BaseModel):
    name: str
    category: str
    price: float
    quantity: int = Field(ge=0)

class SweetOut(SweetIn):
    id: str

class PurchaseIn(BaseModel):
    amount: int = Field(gt=0)

class RestockIn(BaseModel):
    amount: int = Field(gt=0)
