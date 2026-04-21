from dataclasses import dataclass, field
from .task import Task


@dataclass
class User:
    id: int = field(default=None, init=False)
    email: str
    password: str
