from typing import Protocol, Optional

from nlp.domain.entities import (
    Task,
    TaskStatus
)


class TaskRepositoryInterface(Protocol):
    async def get_by_id(self, task_id: int) -> Optional[Task]: ...
    async def get_user_project_tasks(self, user_id: int, project_id: int, status: TaskStatus) -> list[Task]: ...
