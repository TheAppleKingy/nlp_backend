from typing import Optional

from sqlalchemy import select

from nlp.domain.entities import (
    Task,
    TaskStatus
)
from nlp.application.interfaces.repositories import TaskRepositoryInterface
from .base import BaseAlchemyRepository


class AlchemyTaskRepository(BaseAlchemyRepository, TaskRepositoryInterface):
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        return await self._session.scalar(select(Task).where(Task.id == task_id))

    async def get_user_project_tasks(self, user_id: int, project_id: int, status: TaskStatus) -> list[Task]:
        stmt = (
            select(Task).where(Task, user_id == user_id, Task.project_id == project_id, Task.status == status)
        )
        return await self._session.scalars(stmt)
