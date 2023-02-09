from fastapi import FastAPI
from router import air_quality
from config import database
from fastapi.middleware.cors import CORSMiddleware

collection = database.client["exceed06"]["air_quality"]

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


@app.get("/insert_test")
def test():
    collection.insert_one({"test": "test2"})
    return {"project": "done"}
