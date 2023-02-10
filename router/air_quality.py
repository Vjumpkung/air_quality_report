from fastapi import APIRouter, Body, HTTPException
from config import database

router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["air_quality"]


@router.get("/")
def air_test():
    return {"output": "test"}
