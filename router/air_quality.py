from fastapi import APIRouter, Body, HTTPException
from config import database

router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["test_db"]

@router.get("/")
def air_test():
    return {"output":"test"}