from datetime import datetime

from pydantic import BaseModel

from nlp.domain.entities import TaskStatus


class CreateTaskDTO(BaseModel):
    name: str
    project_id: int
    data: str


class ShowTaskDTO(BaseModel):
    id: int
    name: str
    data: str
    project_id: int
    created_at: datetime
    updated_at: datetime
    status: TaskStatus


class HandleTaskDTO(BaseModel):
    task_id: int
