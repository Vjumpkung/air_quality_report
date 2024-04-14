from pydantic import BaseModel


class RootResponseDto(BaseModel):
    project: str
