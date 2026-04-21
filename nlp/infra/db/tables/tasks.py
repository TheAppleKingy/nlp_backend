from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    DateTime,
    Enum
)

from nlp.domain.entities import TaskStatus
from .base import (
    id_,
    metadata
)


tasks = Table(
    "tasks", metadata,
    id_(),
    Column("name", String, unique=False, nullable=False),
    Column("user_id", ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=False),
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), unique=False, nullable=False),
    Column("data", String, nullable=False, unique=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("status", Enum(TaskStatus), nullable=False, unique=False)
)
