from pydantic import BaseModel


class TemperatureSensorResponseDto(BaseModel):
    temperature: bool


class HumiditySensorResponseDto(BaseModel):
    humidity: bool


class CoSensorResponseDto(BaseModel):
    co: bool
