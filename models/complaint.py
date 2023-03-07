import sqlalchemy
from db import metadata
import enum


class State(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


complaint_model = sqlalchemy.Table(
    "complaints",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(500), nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False, server_onupdate=sqlalchemy.func.now(),
                      server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("state", sqlalchemy.Enum(State), nullable=False, server_default=State.PENDING.name),
    sqlalchemy.Column("complainer_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
)
