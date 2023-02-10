from fastapi import APIRouter, Body, HTTPException
from config import database


router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["air_quality"]

led_collection = database.client["exceed06"]["led_status"]


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
    Return RGB color of temperature, humidity, and co.
    """
    pass


@router.post("/turn_on/{sensor_type}")
def turn_on_led(sensor_type: str):
    """
    sensor_type = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {device_name} to True.
    """
    led_collection.update_one({'sensor_type': sensor_type}, {"$set": {"status": True}})
    return f"led of {sensor_type} is turned on"


@router.post("/turn_off/{sensor_type}")
def turn_off_led(sensor_type: str):
    """
    sensor_type = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {device_name} to False.
    """
    led_collection.update_one({'sensor_type': sensor_type}, {"$set": {"status": False}})
    return f"led of {sensor_type} is turned off"


@router.get("/clear_database/")
def clear_database():
    """Delete the data that is older than 24 hours."""
    pass
