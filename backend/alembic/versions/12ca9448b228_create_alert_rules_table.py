"""create alert_rules table"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_alert_rules_table'
down_revision = '247877720273'  # replace this with the last migration id
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'alert_rules',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('host_id', sa.Integer(), sa.ForeignKey('hosts.id', ondelete='CASCADE'), nullable=True),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('operator', sa.String(), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )


def downgrade() -> None:
    op.drop_table('alert_rules')
