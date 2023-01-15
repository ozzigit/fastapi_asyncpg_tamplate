"""jobs test module

Revision ID: 139bd5d8e218
Revises: 5854cbb54436
Create Date: 2023-01-14 16:52:33.070062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "139bd5d8e218"
down_revision = "5854cbb54436"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("work_name", sa.String(), nullable=False),
        sa.Column("unit_of_measurement", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("jobs_pkey")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("jobs")
    # ### end Alembic commands ###
