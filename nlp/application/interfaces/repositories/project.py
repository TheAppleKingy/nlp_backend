from typing import Protocol, Optional

from nlp.domain.entities import Project


class ProjectRepositoryInterface(Protocol):
    async def get_user_projects(self, user_id: int) -> list[Project]: ...
    async def get_by_id(self, project_id: int) -> Optional[Project]: ...
