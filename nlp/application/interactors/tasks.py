import random
import asyncio

from nlp.domain.entities import (
    User,
    Task,
    TaskStatus
)
from nlp.application.interfaces import (
    PublisherInterface,
    UoWInterface
)
from nlp.application.interfaces.repositories import (
    TaskRepositoryInterface,
    UserRepositoryInterface,
    ProjectRepositoryInterface
)
from nlp.application.errors import (
    UndefinedTaskError,
    UndefinedProjectError,
    UserDoesNotRelatedToProject
)


class CreateTask:
    def __init__(
        self,
        uow: UoWInterface,
        publisher: PublisherInterface,
        project_repo: ProjectRepositoryInterface,
        user_repo: UserRepositoryInterface
    ):
        self._uow = uow
        self._publisher = publisher
        self._project_repo = project_repo
        self._user_repo = user_repo

    async def __call__(self, user_id: int, project_id: int, name: str, data: dict) -> Task:
        async with self._uow as uow:
            project = await self._project_repo.get_by_id(project_id)
            if not project:
                raise UndefinedProjectError("Project does not exist")
            user = await self._user_repo.get_by_id(user_id)
            if not user in project.users:
                raise UserDoesNotRelatedToProject("Current user not in the project", status=403)
            task = Task(name, user_id, project_id, data)
            uow.add(task)
            await uow.flush(task)
            await self._publisher.publish(task)
            return task


class HandleTask:
    def __init__(
        self,
        uow: UoWInterface,
        task_repo: TaskRepositoryInterface
    ):
        self._uow = uow
        self._task_repo = task_repo

    async def __call__(self, task_id: int):
        async with self._uow:
            task = await self._task_repo.get_by_id(task_id)
            if not task:
                raise UndefinedTaskError("Task does not exist")
            await asyncio.sleep(random.randint(1, 10))
            task.finish(random.choice([TaskStatus.CRASHED, TaskStatus.DONE]))


class ShowProjectTasks:
    def __init__(
        self,
        uow: UoWInterface,
        task_repo: TaskRepositoryInterface
    ):
        self._uow = uow
        self._task_repo = task_repo

    async def __call__(self, user_id: int, project_id: int, status: TaskStatus):
        async with self._uow:
            return await self._task_repo.get_user_project_tasks(user_id, project_id, status)
