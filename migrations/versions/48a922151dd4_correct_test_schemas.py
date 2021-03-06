"""Correct Test schemas

Revision ID: 48a922151dd4
Revises: 2b71d67ef04d
Create Date: 2013-11-07 13:12:14.375337

"""

# revision identifiers, used by Alembic.
revision = '48a922151dd4'
down_revision = '2b71d67ef04d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('UPDATE testgroup SET result = 0 WHERE result IS NULL')
    op.execute('UPDATE test SET result = 0 WHERE result IS NULL')
    op.execute('UPDATE testgroup SET num_failed = 0 WHERE num_failed IS NULL')
    op.execute('UPDATE testgroup SET num_tests = 0 WHERE num_tests IS NULL')

    op.alter_column('test', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('test', 'result',
               existing_type=sa.INTEGER(),
               server_default=text('0'),
               nullable=False)
    op.alter_column('testgroup', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('testgroup', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('testgroup', 'num_failed',
               existing_type=sa.INTEGER(),
               server_default=text('0'),
               nullable=False)
    op.alter_column('testgroup', 'num_tests',
               existing_type=sa.INTEGER(),
               server_default=text('0'),
               nullable=False)
    op.alter_column('testgroup', 'result',
               existing_type=sa.INTEGER(),
               server_default=text('0'),
               nullable=False)
    op.alter_column('testsuite', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('testsuite', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('testsuite', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('testsuite', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('testgroup', 'result',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('testgroup', 'num_tests',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('testgroup', 'num_failed',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('testgroup', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('testgroup', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('test', 'result',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('test', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    ### end Alembic commands ###
