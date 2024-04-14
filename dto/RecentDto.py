from pydantic import BaseModel


class RecentDto(BaseModel):
    temperature: int
    humidity: int
    CO: int
    temperature_status: str
    humidity_status: str
    CO_status: str
