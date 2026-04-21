from dataclasses import dataclass, field

from .task import Task
from .user import User


@dataclass
class Project:
    id: int = field(init=False, default=None)
    name: str
    description: str
    tasks: list[Task] = field(default_factory=list, init=False)
    users: list[User] = field(default_factory=list, init=False)
