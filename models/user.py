import enum
import sqlalchemy
from db import metadata


class RoleType(enum.Enum):
    APPROVER = "approver"
    COMPLAINER = "complainer"
    ADMIN = "admin"


user_model = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(122), unique=True),
    sqlalchemy.Column("phone", sqlalchemy.String(13), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("first_name", sqlalchemy.String(100)),
    sqlalchemy.Column("last_name", sqlalchemy.String(100)),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), nullable=False, server_default=RoleType.COMPLAINER.name),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now(),
                      server_onupdate=sqlalchemy.func.now()),
    sqlalchemy.Column("iban", sqlalchemy.String(200)))
