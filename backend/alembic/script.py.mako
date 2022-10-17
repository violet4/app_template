"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    # conn = op.get_bind()
    # conn.execute(r"""""")
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    # conn = op.get_bind()
    # conn.execute(r"""""")
    ${downgrades if downgrades else "pass"}
