from pydantic import BaseModel


class Data(BaseModel):
    temperature: int
    humidity: int
    co: float
