from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
)
from .base import metadata

users_projects = Table(
    "users_projects", metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), unique=False, nullable=False),
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), unique=False, nullable=False)
)
