from typing import Protocol

from nlp.domain.entities import Task


class PublisherInterface(Protocol):
    async def publish(self, task: Task) -> None: ...
