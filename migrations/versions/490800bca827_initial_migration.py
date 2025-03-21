"""Initial migration.

Revision ID: 490800bca827
Revises: 
Create Date: 2025-02-28 15:54:24.682016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '490800bca827'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('contact', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('pasword', sa.String(length=34), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('email')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('contact', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('pasword', sa.String(length=34), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('email')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.Column('authors_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('no_of_pages', sa.Integer(), nullable=True),
    sa.Column('price_unit', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('contact', sa.String(length=20), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('publication_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['authors_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_table('companies')
    op.drop_table('authors')
    # ### end Alembic commands ###
