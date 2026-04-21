from nlp.domain.entities import (
    Project
)
from nlp.application.interfaces import (
    UoWInterface
)
from nlp.application.interfaces.repositories import (
    UserRepositoryInterface,
    ProjectRepositoryInterface
)


class CreateProject:
    def __init__(
        self,
        uow: UoWInterface,
        user_repo: UserRepositoryInterface
    ):
        self._uow = uow
        self._user_repo = user_repo

    async def __call__(self, name: str, description: str, user_id: int):
        async with self._uow as uow:
            user = await self._user_repo.get_by_id(user_id)  # TODO: why don't check?
            project = Project(name, description)
            project.users.append(user)
            uow.add(project)
            await uow.flush(project)
            return project


class ShowProjects:
    def __init__(
        self,
        uow: UoWInterface,
        project_repo: ProjectRepositoryInterface
    ):
        self._uow = uow
        self._project_repo = project_repo

    async def __call__(self, user_id: int):
        async with self._uow:
            return await self._project_repo.get_user_projects(user_id)
