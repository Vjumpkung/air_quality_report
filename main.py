from fastapi import FastAPI, Body
from router import air_quality
from config import database
from pydantic import BaseModel
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


class Data(BaseModel):
    temperature: int
    humidity: int
    co: float


@app.get("/")
def root():
    return {"project": "group 6"}


@app.get("/get_all_info")
def test():
    # for test only
    return list(collection.find({}, {"_id": 0}))


@app.post("/color")
def test(data: Data):
    collection.insert_one(
        {"temperature": data.temperature, "humidity": data.humidity, "CO": data.co}
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
    if 0 <= data.co < 4.4:
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
    print(
        list(
            collection.find(
                {
                    "temperature": data.temperature,
                    "humidity": data.humidity,
                    "CO": data.co,
                }
            )
        )
    )
    return color
