from pydantic import BaseModel


class LedStatusResponseDto(BaseModel):
    temperature: bool
    humidity: bool
    co: bool
