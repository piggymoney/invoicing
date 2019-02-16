"""Adding invoice payments

Revision ID: ea47e51a2021
Revises: 4492fb1ec2b2
Create Date: 2019-02-16 20:19:55.598914+11:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea47e51a2021'
down_revision = '4492fb1ec2b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'status',
               existing_type=sa.INTEGER())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'status',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
