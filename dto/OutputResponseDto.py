from pydantic import BaseModel


class OutputResponseDto(BaseModel):
    output: str
