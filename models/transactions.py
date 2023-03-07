import sqlalchemy

from db import metadata

transaction_model = sqlalchemy.Table(
    'Transaction',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("quote_id", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("transfer_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("target_account_id)", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("complaint_id", sqlalchemy.ForeignKey("complaints.id"), nullable=False),
)
