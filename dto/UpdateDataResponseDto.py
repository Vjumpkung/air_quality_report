from pydantic import BaseModel


class UpdateDataResponseDto(BaseModel):
    temperature_R: int
    temperature_G: int
    temperature_B: int
    humidity_R: int
    humidity_G: int
    humidity_B: int
    CO_R: int
    CO_G: int
    CO_B: int
