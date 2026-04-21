from faststream.rabbit import RabbitRouter
from dishka.integrations.faststream import FromDishka
from nlp.interfaces.dtos.task import HandleTaskDTO
from nlp.application.interactors import HandleTask

handle_router = RabbitRouter()


@handle_router.subscriber("task_handling")
async def handle_task(dto: HandleTaskDTO, interactor: FromDishka[HandleTask]):
    await interactor(dto.task_id)
