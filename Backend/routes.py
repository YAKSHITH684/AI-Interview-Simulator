
from fastapi import APIRouter
from pydantic import BaseModel

from database.database import SessionLocal
from database.models import User


router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str



@router.post("/register")
def register(data: RegisterRequest):

    db = SessionLocal()

    exists = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if exists:

        db.close()

        return {
            "message":
            "User already exists"
        }


    user = User(
        email=data.email,
        password=data.password
    )

    db.add(user)

    db.commit()

    db.close()

    return {
        "message":
        "Registration Successful"
    }



@router.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.email == data.email,
            User.password == data.password
        )
        .first()
    )

    db.close()

    return {
        "success": bool(user)
    }



@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:

        db.close()

        return {
            "message":
            "Email not found"
        }


    user.password = data.new_password

    db.commit()

    db.close()

    return {
        "message":
        "Password Updated Successfully"
    }

