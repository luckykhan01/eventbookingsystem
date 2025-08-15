from alembic import op
import sqlalchemy as sa

revision = "b810c538a9d1"
down_revision = "b183a215cd08"
branch_labels = None
depends_on = None

def upgrade():
    # 1) add as NULLable
    with op.batch_alter_table('event') as batch_op:
        batch_op.add_column(sa.Column('time', sa.Time(), nullable=True))

    # 2) existing rows
    op.execute("UPDATE event SET time = '00:00:00' WHERE time IS NULL")

    # 3) enforce NOT NULL (batch mode recreates the table in SQLite)
    with op.batch_alter_table('event') as batch_op:
        batch_op.alter_column('time', existing_type=sa.Time(), nullable=False)

def downgrade():
    with op.batch_alter_table('event') as batch_op:
        batch_op.drop_column('time')
