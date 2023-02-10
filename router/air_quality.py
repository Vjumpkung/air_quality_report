from fastapi import APIRouter, Body, HTTPException
from config import database


router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["test_db"]


@router.get("/")
def air_test():
    return {"output": "test"}


@router.get("/get_last_ten_minutes_logs/")
def get_last_ten_minutes_logs():
    """Return the last 120 logs in the database."""
    pass


@router.get("/get_most_recent_log/")
def get_most_recent_log():
    """Return the most recent log in the database."""
    pass


@router.post("/update_data/")
def update_data():
    """
    Save data to the database adding datetime with the above body.
    Receive data from hardware and return RGB color of temperature, humidity, and co.
    """
    pass


@router.post("/turn_on/{device_name}")
def turn_on_led():
    """
    device_name = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {device_name} to True.
    """
    pass


@router.post("/turn_off/{device_name}")
def turn_off_led():
    """
    device_name = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {device_name} to False.
    """
    pass


@router.get("/clear_database/")
def clear_database():
    """Delete the data that is older than 24 hours."""
    pass

