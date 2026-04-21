from fastapi import (
    APIRouter,
    Query
)
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)

from nlp.interfaces.dtos.task import (
    CreateTaskDTO,
    ShowTaskDTO
)
from nlp.application.interactors import (
    CreateTask,
    ShowProjectTasks
)
from nlp.domain.types import AuthenticatedUserId
from nlp.domain.entities import TaskStatus


task_router = APIRouter(prefix="/tasks", tags=["Tasks router"], route_class=DishkaRoute)


@task_router.post("")
async def create_task(
    dto: CreateTaskDTO,
    user_id: FromDishka[AuthenticatedUserId],
    interactor: FromDishka[CreateTask]
):
    return await interactor(user_id, dto.project_id, dto.name, dto.data)


@task_router.get("/project/{project_id}")
async def get_user_project_tasks(
    project_id: int,
    user_id: FromDishka[AuthenticatedUserId],
    interactor: FromDishka[ShowProjectTasks],
    status: TaskStatus = Query()
) -> list[ShowTaskDTO]:
    return await interactor(user_id, project_id, status)
