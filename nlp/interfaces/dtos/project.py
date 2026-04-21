from pydantic import BaseModel


class CreateProjectDTO(BaseModel):
    name: str
    description: str


class ShowProjectDTO(BaseModel):
    id: int
    name: str
    description: str
