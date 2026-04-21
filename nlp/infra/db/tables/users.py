from sqlalchemy import (
    Table,
    Column,
    String
)
from sqlalchemy_utils import EmailType

from .base import (
    id_,
    metadata
)

users = Table(
    "users", metadata,
    id_(),
    Column("email", EmailType, unique=True, nullable=True),
    Column("password", String, nullable=False)
)
