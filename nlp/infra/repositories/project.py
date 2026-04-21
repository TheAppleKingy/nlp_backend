from typing import Optional

from sqlalchemy import select

from nlp.domain.entities import (Project)
from nlp.application.interfaces.repositories import ProjectRepositoryInterface
from nlp.infra.db.tables import users_projects
from .base import BaseAlchemyRepository


class AlchemyProjectRepository(BaseAlchemyRepository, ProjectRepositoryInterface):
    async def get_user_projects(self, user_id: int) -> list[Project]:
        stmt = (
            select(Project)
            .join(users_projects, users_projects.c.project_id == Project.id)
            .where(users_projects.c.user_id == user_id)
        )
        res = await self._session.scalars(stmt)
        return res.all()

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        return await self._session.scalar(select(Project).where(Project.id == project_id))
