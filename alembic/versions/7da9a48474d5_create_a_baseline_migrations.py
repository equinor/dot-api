"""Create a baseline migrations

Revision ID: 7da9a48474d5
Revises: 
Create Date: 2025-06-24 10:44:01.456165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = '7da9a48474d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('azure_id', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('azure_id')
    )
    op.create_table('project',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=600), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_name'), 'project', ['name'], unique=False)
    op.create_table('scenario',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('project_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenario_name'), 'scenario', ['name'], unique=False)
    op.create_index(op.f('ix_scenario_project_id'), 'scenario', ['project_id'], unique=False)
    op.create_table('issue',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('scenario_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('type', sa.String(length=60), nullable=False),
    sa.Column('boundary', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=600), nullable=False),
    sa.Column('order', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_issue_name'), 'issue', ['name'], unique=False)
    op.create_table('objective',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('scenario_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=600), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objective_name'), 'objective', ['name'], unique=False)
    op.create_index(op.f('ix_objective_scenario_id'), 'objective', ['scenario_id'], unique=False)
    op.create_table('opportunity',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('scenario_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=600), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_opportunity_name'), 'opportunity', ['name'], unique=False)
    op.create_index(op.f('ix_opportunity_scenario_id'), 'opportunity', ['scenario_id'], unique=False)
    op.create_table('decision',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('issue_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('alternatives', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('scenario_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('issue_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_node_name'), 'node', ['name'], unique=False)
    op.create_table('uncertainty',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('issue_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('probabilities', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utility',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('issue_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('values', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('value_metric',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('issue_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edge',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('tail_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('head_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('scenario_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.ForeignKeyConstraint(['head_id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.id'], ),
    sa.ForeignKeyConstraint(['tail_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node_style',
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('node_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('x_position', sa.INTEGER(), nullable=False),
    sa.Column('y_position', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('node_style')
    op.drop_table('edge')
    op.drop_table('value_metric')
    op.drop_table('utility')
    op.drop_table('uncertainty')
    op.drop_index(op.f('ix_node_name'), table_name='node')
    op.drop_table('node')
    op.drop_table('decision')
    op.drop_index(op.f('ix_opportunity_scenario_id'), table_name='opportunity')
    op.drop_index(op.f('ix_opportunity_name'), table_name='opportunity')
    op.drop_table('opportunity')
    op.drop_index(op.f('ix_objective_scenario_id'), table_name='objective')
    op.drop_index(op.f('ix_objective_name'), table_name='objective')
    op.drop_table('objective')
    op.drop_index(op.f('ix_issue_name'), table_name='issue')
    op.drop_table('issue')
    op.drop_index(op.f('ix_scenario_project_id'), table_name='scenario')
    op.drop_index(op.f('ix_scenario_name'), table_name='scenario')
    op.drop_table('scenario')
    op.drop_index(op.f('ix_project_name'), table_name='project')
    op.drop_table('project')
    op.drop_table('user')
    # ### end Alembic commands ###
