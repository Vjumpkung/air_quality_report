from fastapi import APIRouter, Body, HTTPException
from config import database
import datetime
from zoneinfo import ZoneInfo
from basemodel_class.basemodel_collection import Data


router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["air_quality"]


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
def update_data(data: Data):
    """
    Save data to the database adding datetime with the above body.
    Receive data from hardware and return RGB color of temperature, humidity, and co.
    """
    date_now = datetime.now(ZoneInfo("Asia/Bangkok"))
    collection.insert_one(
        {
            "datetime": date_now,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "CO": data.co,
        }
    )
    color = {}
    # temperature color
    if 35.0 <= data.temperature <= 39.9:
        # hot
        color["temperature_R"] = 255
        color["temperature_G"] = 153
        color["temperature_B"] = 51
    elif data.temperature >= 40:
        # very hot
        color["temperature_R"] = 255
        color["temperature_G"] = 0
        color["temperature_B"] = 0
    elif 23 <= data.temperature < 35:
        # optimal
        color["temperature_R"] = 0
        color["temperature_G"] = 255
        color["temperature_B"] = 0
    elif 16 <= data.temperature < 23:
        # cool
        color["temperature_R"] = 102
        color["temperature_G"] = 255
        color["temperature_B"] = 255
    elif 8 <= data.temperature < 16:
        # cold
        color["temperature_R"] = 51
        color["temperature_G"] = 153
        color["temperature_B"] = 255
    elif data.temperature < 8:
        # very cold
        color["temperature_R"] = 51
        color["temperature_G"] = 102
        color["temperature_B"] = 255
    # humidity color
    if 0 <= data.humidity < 40:
        # too dry
        color["humidity_R"] = 220
        color["humidity_G"] = 77
        color["humidity_B"] = 93
    elif 40 <= data.humidity < 60:
        # optimal
        color["humidity_R"] = 103
        color["humidity_G"] = 201
        color["humidity_B"] = 239
    elif 60 <= data.humidity:
        # too wet
        color["humidity_R"] = 86
        color["humidity_G"] = 105
        color["humidity_B"] = 177
    # CO AQI range
    if 0 <= data.co < 4.5:
        color["CO_R"] = 0
        color["CO_G"] = 204
        color["CO_B"] = 255
    elif 4.5 <= data.co < 6.5:
        color["CO_R"] = 0
        color["CO_G"] = 255
        color["CO_B"] = 0
    elif 6.5 <= data.co < 9:
        color["CO_R"] = 255
        color["CO_G"] = 255
        color["CO_B"] = 0
    elif 9.0 <= data.co < 30:
        color["CO_R"] = 255
        color["CO_G"] = 153
        color["CO_B"] = 51
    elif 30 <= data.co:
        color["CO_R"] = 255
        color["CO_G"] = 0
        color["CO_B"] = 0
    return color


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
    collection.delete_many(
        {
            "datetime": {
                "$lt": datetime.datetime.now(ZoneInfo("Asia/Bangkok"))
                - datetime.timedelta(days=1)
            }
        }
    )
    return {"status": "delete complete"}
