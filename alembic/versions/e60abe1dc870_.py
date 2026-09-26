"""

Revision ID: e60abe1dc870
Revises: a109fa04837d
Create Date: 2026-02-01 20:48:06.730189

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "e60abe1dc870"
down_revision: Union[str, Sequence[str], None] = "a109fa04837d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op: breed_descriptions is already created in 14a47eeaad4b."""
    pass


def downgrade() -> None:
    """No-op: breed_descriptions is dropped in 14a47eeaad4b."""
    pass
