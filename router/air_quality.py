from fastapi import APIRouter, HTTPException, Response
from pymongo import DESCENDING
from config import database
import datetime
from zoneinfo import ZoneInfo
from basemodel_class.basemodel_collection import Data
from dotenv import load_dotenv
from dto.OutputResponseDto import OutputResponseDto
from dto.LastTenMinutesDto import LastTenMinutesDto
from dto.UpdateDataResponseDto import UpdateDataResponseDto
from dto.TurnOnOffSensorResponseDto import *
from dto.LedStatusResponseDto import LedStatusResponseDto
from dto.RecentDto import RecentDto
from typing import List, Union

load_dotenv(".env")

router = APIRouter(prefix="/air_quality", tags=["air_quality"])
collection = database.client["exceed06"]["air_quality"]

led_collection = database.client["exceed06"]["led_status"]
user_collection = database.client["exceed06"]["user"]


def calculate_status_temp(temp: int) -> str:
    """Return the string status from the given temperature number."""
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


def calculate_status_humidity(humidity: int) -> str:
    """Return the string status from the given humidity number."""
    if 0 <= humidity < 40:
        return "Too Dry"
    elif 40 <= humidity < 60:
        return "Optimal"
    elif 60 <= humidity:
        return "Too Humid"


def calculate_status_co(co: int) -> str:
    """Return the string status from the given co number."""
    if 0 <= co < 780:
        return "Very Good"
    elif 780 <= co < 1160:
        return "Good"
    elif 1160 <= co < 1540:
        return "CO_Normal"
    elif 1540 <= co < 1920:
        return "Health affected"
    elif 1920 <= co:
        return "Dangerous"


@router.get("/")
def air_test() -> OutputResponseDto:
    return {"output": "test"}


@router.get("/get_last_ten_minutes_logs/")
def get_last_ten_minutes_logs() -> List[LastTenMinutesDto]:
    """Return the last 120 logs in the database."""
    if len(list(collection.find({}))) < 120:
        raise HTTPException(503, "data is not enough please try again")

    lst = list(collection.find({}, {"_id": 0}).sort("datetime", DESCENDING).limit(120))
    res = []
    for i in range(0, len(lst), 12):
        temp = lst[i : i + 12]
        temperature_avg = sum([x["temperature"] for x in temp]) // 12
        humidity_avg = sum([x["humidity"] for x in temp]) // 12
        co_avg = sum([x["CO"] for x in temp]) // 12
        res.append(
            {
                "time": i // 12 + 1,
                "temperature": temperature_avg,
                "humidity": humidity_avg,
                "CO": co_avg,
                "temperature_status": calculate_status_temp(temperature_avg),
                "humidity_status": calculate_status_humidity(temperature_avg),
                "CO_status": calculate_status_co(co_avg),
            }
        )
    return res


@router.get("/get_most_recent_log/")
def get_most_recent_log() -> List[RecentDto]:
    """Return the most recent log in the database."""
    recent_log = list(
        collection.find({}, {"_id": 0}).sort("datetime", DESCENDING).limit(1)
    )[0]
    return [
        {
            "temperature": recent_log["temperature"],
            "humidity": recent_log["humidity"],
            "CO": recent_log["CO"],
            "temperature_status": calculate_status_temp(recent_log["temperature"]),
            "humidity_status": calculate_status_humidity(recent_log["humidity"]),
            "CO_status": calculate_status_co(recent_log["CO"]),
        }
    ]


@router.post("/update_data/")
def update_data(data: Data) -> UpdateDataResponseDto:
    """
    Receive data from hardware and return RGB color of temperature, humidity, and co.
    Save data to the database adding datetime with the above body.
    """
    date_now = datetime.datetime.now(ZoneInfo("Asia/Bangkok"))
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
    if 0 <= data.co < 780:
        color["CO_R"] = 0
        color["CO_G"] = 204
        color["CO_B"] = 255
    elif 780 <= data.co < 1160:
        color["CO_R"] = 0
        color["CO_G"] = 255
        color["CO_B"] = 0
    elif 1160 <= data.co < 1540:
        color["CO_R"] = 255
        color["CO_G"] = 255
        color["CO_B"] = 0
    elif 1540 <= data.co < 1920:
        color["CO_R"] = 255
        color["CO_G"] = 153
        color["CO_B"] = 51
    elif 1920 <= data.co:
        color["CO_R"] = 255
        color["CO_G"] = 0
        color["CO_B"] = 0
    return color


@router.post("/turn_on/{sensor_type}/")
def turn_on_led(
    sensor_type: str,
) -> Union[
    HumiditySensorResponseDto, CoSensorResponseDto, TemperatureSensorResponseDto
]:
    """
    sensor_type = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {sensor_type} to True.
    """
    if sensor_type not in ["temperature", "humidity", "co"]:
        return HTTPException(status_code=406, detail="Sensor type is invalid.")
    led_collection.update_one({"sensor_type": sensor_type}, {"$set": {"status": True}})
    return {sensor_type: True}


@router.post("/turn_off/{sensor_type}/")
def turn_off_led(
    sensor_type: str,
) -> Union[
    HumiditySensorResponseDto, CoSensorResponseDto, TemperatureSensorResponseDto
]:
    """
    sensor_type = "temperature"/ "humidity" / "co"
    Set status of LED that show status of {sensor_type} to False.
    """
    if sensor_type not in ["temperature", "humidity", "co"]:
        return HTTPException(status_code=406, detail="Sensor type is invalid.")
    led_collection.update_one({"sensor_type": sensor_type}, {"$set": {"status": False}})
    return {sensor_type: False}


@router.get("/get_led_status/")
def get_led_status() -> LedStatusResponseDto:
    """Get status of all led."""
    result = {}
    for i in led_collection.find({}, {"_id": False}):
        result[i["sensor_type"]] = i["status"]
    return result


@router.get("/clear_database/", status_code=204)
def clear_database():
    """Delete data older than 20 min."""
    collection.delete_many(
        {"datetime": {"$lt": datetime.datetime.now() - datetime.timedelta(minutes=20)}}
    )
    return Response(status_code=204)
