from fastapi import FastAPI, Body
from router import air_quality
from config import database
from dto.RootResponseDto import RootResponseDto
from fastapi.middleware.cors import CORSMiddleware


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
def root() -> RootResponseDto:
    return {"project": "group 6"}
