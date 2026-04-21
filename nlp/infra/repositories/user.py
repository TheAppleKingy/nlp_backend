from typing import Optional

from sqlalchemy import select

from nlp.domain.entities import User
from nlp.application.interfaces.repositories import UserRepositoryInterface
from .base import BaseAlchemyRepository


class AlchemyUserRepository(BaseAlchemyRepository, UserRepositoryInterface):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._session.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._session.scalar(select(User).where(User.email == email))
