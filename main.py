from fastapi import FastAPI, Body
from router import air_quality
from config import database
from fastapi.middleware.cors import CORSMiddleware
from basemodel_class.basemodel_collection import Data

collection = database.client["exceed06"]["test_db"]

app = FastAPI()
app.include_router(air_quality.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"project": "group 6"}
