"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

This migration script handles schema changes for the database. 
Generated by Alembic.

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# Revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """
    Apply schema changes to the database.
    
    Use Alembic's operations module (op) to modify the database schema. 
    Example: op.create_table, op.add_column, op.create_index, etc.
    """
    # TODO: Add upgrade logic
    ${upgrades if upgrades else "pass"}
    # Example:
    # op.create_table(
    #     'example_table',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(255), nullable=False),
    # )


def downgrade() -> None:
    """
    Revert schema changes made in the upgrade() method.
    
    This should reverse any operations performed in upgrade().
    """
    # TODO: Add downgrade logic
    ${downgrades if downgrades else "pass"}
    # Example:
    # op.drop_table('example_table')
