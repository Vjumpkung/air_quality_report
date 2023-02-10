from fastapi import APIRouter, Body, HTTPException
from pymongo import DESCENDING
from config import database
from datetime import datetime
from basemodel_class.basemodel_collection import Data

router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["test_db"]

led_collection = database.client["exceed06"]["led_status"]


def calculate_status_temp(temp):
    if temp >= 40:
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
    elif temp <= 7.9:
        return "Very Cold"


def calculate_status_humidity(humidity):
    if 0 <= humidity < 40:
        return "Too Dry"
    elif 40 <= humidity < 60:
        return "Optimal"
    elif 60 <= humidity:
        return "Too Humid"


def calculate_status_co(co):
    if 0 <= co < 4.5:
        return "Very Good"
    elif 4.5 <= co < 6.5:
        return "Good"
    elif 6.5 <= co < 9:
        return "Normal"
    elif 9.0 <= co < 30:
        return "Health affected"
    elif 30 <= co:
        return "Dangerous"


@router.get("/")
def air_test():
    return {"output": "test"}


@router.get("/get_last_ten_minutes_logs/")
def get_last_ten_minutes_logs():
    """Return the last 120 logs in the database."""
    lst = []
    time = 1
    skip = 0
    for j in range(10):
        avg_temp_lst = []
        avg_humid_lst = []
        avg_co_lst = []
        for i in collection.find({}, {"_id": 0}).sort("datetime", DESCENDING).limit(12).skip(skip):
            avg_temp_lst.append(i["temperature"])
            avg_humid_lst.append(i["humidity"])
            avg_co_lst.append(i["CO"])
        lst.append({"time": time,
                    "temperature": int(sum(avg_temp_lst) / len(avg_temp_lst)),
                    "humidity": int(sum(avg_humid_lst) / len(avg_humid_lst)),
                    "CO": int(sum(avg_co_lst) / len(avg_co_lst)),
                    "temperature_status": calculate_status_temp(sum(avg_temp_lst) / len(avg_temp_lst)),
                    "humidity_status": calculate_status_humidity(sum(avg_humid_lst) / len(avg_humid_lst)),
                    "CO_status": calculate_status_co(sum(avg_co_lst) / len(avg_co_lst))})
        time += 1
        skip += 12
        avg_temp_lst.clear()
        avg_humid_lst.clear()
        avg_co_lst.clear()
    return lst


@router.get("/get_most_recent_log/")
def get_most_recent_log():
    """Return the most recent log in the database."""
    recent_log = collection.find_one({}, {"_id": 0})
    return [{
        "temperature": recent_log.temperature,
        "humidity": recent_log.humidity,
        "CO": recent_log.CO,
        "temperature_status": calculate_status_temp(recent_log.temperature),
        "humidity_status": calculate_status_humidity(recent_log.humidity),
        "CO_status": calculate_status_co(recent_log.CO)
    }]



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
