from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    APIRouter,
    Request,
)
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import setup_dishka as fastapi_setup
from dishka.integrations.faststream import setup_dishka as faststream_setup
from sqlalchemy.orm import (
    registry,
    relationship,
)
from faststream.rabbit import RabbitBroker

from nlp.application.interfaces import *
from nlp.application.interfaces.repositories import *
from nlp.application.interfaces.services import *
from nlp.domain.errors import HandlingError
from nlp.container import container
from nlp.interfaces.controllers.http import *
from nlp.interfaces.controllers.broker import handle_router
from nlp.domain.entities import *
from nlp.infra.db.tables import *


def map_tables():
    reg = registry()
    reg.map_imperatively(Task, tasks)
    reg.map_imperatively(User, users)
    reg.map_imperatively(Project, projects, properties={
        "users": relationship(User, users_projects, lazy="raise"),
        "tasks": relationship(Task, lazy="selectin", cascade="all, delete-orphan")
    })


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routers(app)
    broker = await container.get(RabbitBroker)
    broker.include_router(handle_router)
    faststream_setup(container, broker=broker, auto_inject=True)
    await broker.start()
    setup_routers(app)
    map_tables()
    yield
    await broker.stop()
    await container.close()

app = FastAPI(lifespan=lifespan)
fastapi_setup(container, app)


@app.exception_handler(HandlingError)
async def handle_error(r: Request, err: HandlingError):
    return JSONResponse({"detail": str(err)}, err.status)


def setup_routers(app: FastAPI):
    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(task_router)
    api_router.include_router(user_router)
    api_router.include_router(project_router)
    app.include_router(api_router)
