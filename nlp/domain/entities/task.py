from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone


from nlp.domain.errors import TaskAlreadyFinishedError


class TaskStatus(Enum):
    PENDING = "pending"
    CRASHED = "crashed"
    DONE = "done"


@dataclass
class Task:
    name: str
    user_id: int
    project_id: int
    data: str
    id: int = field(default=None, init=False)
    created_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    status: TaskStatus = field(init=False, default_factory=lambda: TaskStatus.PENDING)

    def finish(self, status: TaskStatus):
        if self.status != TaskStatus.PENDING:
            raise TaskAlreadyFinishedError(f"Task already finished with status '{self.status}'")
        self.updated_at = datetime.now(timezone.utc)
        self.status = status
