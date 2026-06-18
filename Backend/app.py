
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

from database.database import Base
from database.database import engine


Base.metadata.create_all(
    bind=engine
)

app = FastAPI()


# ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(
    router
)


@app.get("/")
def home():

    return {
        "message":
        "AI Interview Simulator API Running"
    }
