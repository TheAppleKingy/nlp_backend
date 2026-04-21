from typing import Optional

from nlp.domain.entities import User

from nlp.application.interfaces.services import (
    AuthServiceInterface,
    PasswordServiceInterface
)
from nlp.application.interfaces.repositories import UserRepositoryInterface
from nlp.application.interfaces import UoWInterface
from nlp.application.errors import (
    InvalidPasswordError,
    UndefinedUserError,
    AuthError,
    UserAlreadyExists
)


class RegisterUser:
    def __init__(
        self,
        uow: UoWInterface,
        user_repo: UserRepositoryInterface,
        password_service: PasswordServiceInterface
    ):
        self._uow = uow
        self._password_service = password_service
        self._user_repo = user_repo

    async def __call__(self, email: str, password: str) -> int:
        async with self._uow as uow:
            if await self._user_repo.get_by_email(email):
                raise UserAlreadyExists("Already registered")
            user = User(email, self._password_service.hash_password(password))
            await uow.flush(user)
            uow.add(user)
            return user.id


class LoginUser:
    def __init__(
        self,
        uow: UoWInterface,
        auth_service: AuthServiceInterface,
        password_service: PasswordServiceInterface,
        user_repo: UserRepositoryInterface
    ):
        self._uow = uow
        self._auth_service = auth_service
        self._password_service = password_service
        self._user_repo = user_repo

    async def __call__(self, email: str, password: str) -> str:
        async with self._uow:
            user = await self._user_repo.get_by_email(email)
            if not user:
                raise UndefinedUserError("User does not exist")
            if not self._password_service.check_password(user.password, password):
                raise InvalidPasswordError("Invalid password")
            return self._auth_service.generate_user_token(user.id)


class AuthenticateUser:
    def __init__(
        self,
        uow: UoWInterface,
        auth_service: AuthServiceInterface,
        password_service: PasswordServiceInterface,
        user_repo: UserRepositoryInterface
    ):
        self._uow = uow
        self._auth_service = auth_service
        self._password_service = password_service
        self._user_repo = user_repo

    async def __call__(self, token: Optional[str]):
        if not token:
            raise AuthError("Unauthorized", status=401)
        user_id = self._auth_service.get_user_id(token)
        if not user_id:
            raise AuthError("Invalid credentials", status=401)
        async with self._uow:
            if not await self._user_repo.get_by_id(user_id):
                raise AuthError("Unauthorized", status=401)
            return user_id
