"""empty message

Revision ID: 11df199c2c13
Revises: 
Create Date: 2022-10-16 19:51:11.782763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11df199c2c13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(r"""ALTER TABLE "user" RENAME user_name TO username """)


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(r"""ALTER TABLE "user" RENAME username TO user_name """)
