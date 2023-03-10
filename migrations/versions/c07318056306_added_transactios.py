"""added transactios

Revision ID: c07318056306
Revises: 65ddc94b0316
Create Date: 2022-08-01 00:53:35.728666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c07318056306'
down_revision = '65ddc94b0316'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quote_id', sa.String(length=120), nullable=False),
    sa.Column('transfer_id', sa.Integer(), nullable=False),
    sa.Column('target_account_id)', sa.String(length=120), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('complaint_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Transaction')
    # ### end Alembic commands ###
