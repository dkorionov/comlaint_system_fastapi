"""added field updated_at to complaint model

Revision ID: 65ddc94b0316
Revises: 35cdb17152de
Create Date: 2022-07-27 23:55:34.854462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65ddc94b0316'
down_revision = '35cdb17152de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('complaints', 'updated_at', server_default=sa.text('now()'), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('complaints', 'updated_at', server_default=None)
    # ### end Alembic commands ###
