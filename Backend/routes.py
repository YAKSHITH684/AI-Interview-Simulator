from fastapi import APIRouter
from database.database import SessionLocal
from database.models import User

router=APIRouter()


@router.post("/register")
def register(
email:str,
password:str
):

    db=SessionLocal()

    exists=(
        db.query(User)
        .filter(User.email==email)
        .first()
    )

    if exists:

        db.close()

        return {
            "message":"User already exists"
        }

    user=User(
        email=email,
        password=password
    )

    db.add(user)

    db.commit()

    db.close()

    return {
        "message":"Registration Successful"
    }



@router.post("/login")
def login(
email:str,
password:str
):

    db=SessionLocal()

    user=(
        db.query(User)
        .filter(
            User.email==email,
            User.password==password
        )
        .first()
    )

    db.close()

    if user:

        return {
            "success":True
        }

    return {
        "success":False
    }