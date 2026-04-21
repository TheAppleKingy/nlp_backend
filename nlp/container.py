from typing import AsyncGenerator

from dishka import (
    Provider,
    provide,
    make_async_container,
    Scope
)
from faststream.rabbit import RabbitBroker
from fastapi import Request
from dishka.integrations.fastapi import FastapiProvider
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from nlp.domain.types import AuthenticatedUserId
from nlp.application.interactors import *
from nlp.application.interfaces import *
from nlp.application.interfaces.repositories import *
from nlp.application.interfaces.services import *
from nlp.infra.configs import (
    DBConfig,
    RabbitMQConfig,
    AppConfig
)
from nlp.infra.broker import *
from nlp.infra.repositories import *
from nlp.infra.services import *
from nlp.infra.uow import AlchemyUoW


class ConfigsProvider(Provider):
    scope = Scope.APP

    @provide
    def db_config(self) -> DBConfig:
        return DBConfig()

    @provide
    def rabbit_config(self) -> RabbitMQConfig:
        return RabbitMQConfig()

    @provide
    def app_config(self) -> AppConfig:
        return AppConfig()


class DBProvider(Provider):
    scope = Scope.APP

    @provide
    def engine(self, config: DBConfig) -> AsyncEngine:
        return create_async_engine(config.conn_url)

    @provide
    def sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
            autobegin=False
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            try:
                yield session
            finally:
                await session.close()

    @provide(scope=Scope.REQUEST)
    async def uow(self, session: AsyncSession) -> UoWInterface:
        return AlchemyUoW(session)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    password = provide(PasswordService, provides=PasswordServiceInterface)

    @provide
    def auth(self, conf: AppConfig) -> AuthServiceInterface:
        return JWTAuthService(conf.secret, conf.token_expire_time)


class BrokerProvider(Provider):
    scope = Scope.APP

    @provide
    def publisher(self, conf: RabbitMQConfig, broker: RabbitBroker) -> PublisherInterface:
        return RabbitPublisher(conf.rabbitmq_queue, broker)

    @provide
    def broker(self, conf: RabbitMQConfig) -> RabbitBroker:
        return RabbitBroker(conf.conn_url)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    user = provide(AlchemyUserRepository, provides=UserRepositoryInterface)
    task = provide(AlchemyTaskRepository, provides=TaskRepositoryInterface)
    project = provide(AlchemyProjectRepository, provides=ProjectRepositoryInterface)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def authenticate(self, r: Request, interactor: AuthenticateUser) -> AuthenticatedUserId:
        return AuthenticatedUserId(await interactor(r.cookies.get("token")))


interactor_provider = InteractorProvider()
interactor_provider.provide_all(
    RegisterUser,
    LoginUser,
    AuthenticateUser,
    CreateTask,
    HandleTask,
    ShowProjectTasks,
    CreateProject,
    ShowProjects
)


container = make_async_container(
    ConfigsProvider(),
    DBProvider(),
    ServiceProvider(),
    BrokerProvider(),
    RepositoryProvider(),
    interactor_provider,
    FastapiProvider(),
)
