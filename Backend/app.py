from fastapi import FastAPI
from routes import router

from database.database import engine
from database.database import Base


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(
router
)


@app.get("/")

def home():

    return{

    "message":

    "AI Interview Simulator API Running"

    }