from pydantic import BaseModel


class LastTenMinutesDto(BaseModel):
    time: int
    temperature: int
    humidity: int
    CO: int
    temperature_status: str
    humidity_status: str
    CO_status: str
