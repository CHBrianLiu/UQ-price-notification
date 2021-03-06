"""Added tables

Revision ID: 30a4426d48c3
Revises: 
Create Date: 2022-01-17 13:02:58.777218

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '30a4426d48c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
                    sa.Column('product_code', sa.String(length=14), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('current_price', sa.Integer(), nullable=False),
                    sa.Column('original_price', sa.Integer(), nullable=False),
                    sa.Column('short_description', sa.String(), nullable=True),
                    sa.Column('last_updated', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('product_code')
                    )
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=16), nullable=False),
                    sa.Column('permission', sa.JSON(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('settings',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('value', sa.String(), nullable=False),
                    sa.Column('last_updated', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('id', sa.String(length=100), nullable=False),
                    sa.Column('role_id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users_products',
                    sa.Column('user_id', sa.String(length=100), nullable=False),
                    sa.Column('product_code', sa.String(length=14), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['product_code'], ['products.product_code'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'product_code')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_products')
    op.drop_table('users')
    op.drop_table('settings')
    op.drop_table('roles')
    op.drop_table('products')
    # ### end Alembic commands ###
