import json


from faststream.rabbit import RabbitBroker
from nlp.application.interfaces import PublisherInterface
from nlp.domain.entities import Task


class RabbitPublisher(PublisherInterface):
    def __init__(
        self,
        queue_name: str,
        broker: RabbitBroker
    ):

        self._queue_name = queue_name
        self._broker = broker

    async def publish(self, task: Task):
        await self._broker.publish(
            json.dumps({"task_id": task.id}, default=str).encode(),
            persist=True,
            queue=self._queue_name
        )
