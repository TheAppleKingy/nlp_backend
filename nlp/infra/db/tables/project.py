from sqlalchemy import (
    Table,
    Column,
    String,
)
from .base import (
    id_,
    metadata
)

projects = Table(
    "projects", metadata,
    id_(),
    Column("name", String, nullable=False, unique=False),
    Column("description", String, nullable=False, unique=False)
)
