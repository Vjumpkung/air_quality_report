from fastapi import APIRouter, Body, HTTPException
from pymongo import DESCENDING
from config import database
from datetime import datetime
from basemodel_class.basemodel_collection import Data

router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["air_quality"]

led_collection = database.client["exceed06"]["led_status"]

def calculate_status_temp(temp):
    if temp > 40:
        return "Very Hot"
    elif 35 <= temp <= 39.9:
        return "Hot"
    elif 23 <= temp <= 34.9:
        return "Normal"
    elif 18 <= temp <= 22.9:
        return "Cool"
    elif 16 <= temp <= 17.9:
        return "Moderately Cold"
    elif 8 <= temp <= 15.9:
        return "Cold"
    elif temp >= 7.9:
        return "Very Cold"


def calculate_status_humidity(humid):


def calculate_status_co(co):



@router.get("/")
def air_test():
    return {"output": "test"}


@router.get("/get_last_ten_minutes_logs/")
def get_last_ten_minutes_logs():
    """Return the last 120 logs in the database."""
    dic = {}
    time = 5
    for i in collection.find({}, {"_id": 0}).sort("datetime", DESCENDING).limit(120):
        dic.update({"time": time,
                    "temperature": i.temperature,
                    "humidity": i.humidity,
                    "CO": i.CO,
                    "temperature_status": calculate_status_temp(i.temperature),
                    "humidity_status": calculate_status_humidity(i.humidity),
                    "CO_status": calculate_status_co(i.CO)})
        time += 5
    return list(dic)


@router.get("/get_most_recent_log/")
def get_most_recent_log():
    """Return the most recent log in the database."""
    return list(collection.find_one({}, {"_id": 0}))


@router.post("/update_data/")
def update_data(data: Data):
    """
    Receive data from hardware and return RGB color of temperature, humidity, and co.
    Save data to the database adding datetime with the above body.
    """


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
