from fastapi import APIRouter
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)
from nlp.domain.types import AuthenticatedUserId
from nlp.application.interactors import (
    CreateProject,
    ShowProjects
)
from nlp.interfaces.dtos.project import (
    CreateProjectDTO,
    ShowProjectDTO
)

project_router = APIRouter(prefix="/projects", tags=["Projects router"], route_class=DishkaRoute)


@project_router.post("")
async def create_project(
    dto: CreateProjectDTO,
    user_id: FromDishka[AuthenticatedUserId],
    interactor: FromDishka[CreateProject]
) -> ShowProjectDTO:
    return await interactor(dto.name, dto.description, user_id)


@project_router.get("")
async def get_user_projects(
    user_id: FromDishka[AuthenticatedUserId],
    interactor: FromDishka[ShowProjects]
) -> list[ShowProjectDTO]:
    return await interactor(user_id)
