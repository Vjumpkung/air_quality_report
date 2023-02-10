from config import database

collection = database.client["exceed06"]["led_status"]

collection.delete_many({})

all_led = [
    {
        "sensor_type": "temperature",
        "status": False,
    },
    {
        "sensor_type": "humidity",
        "status": False,
    },
    {
        "sensor_type": "co",
        "status": False,
    }
]

collection.insert_many(all_led)
