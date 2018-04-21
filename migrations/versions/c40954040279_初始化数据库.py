"""初始化数据库

Revision ID: c40954040279
Revises: 
Create Date: 2018-04-21 15:42:56.189636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c40954040279'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classifys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classify', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classifys_classify'), 'classifys', ['classify'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_tag'), 'tags', ['tag'], unique=False)
    op.create_table('marks',
    sa.Column('Post_id', sa.Integer(), nullable=True),
    sa.Column('Tag_id', sa.Integer(), nullable=True),
    sa.Column('Classify_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Classify_id'], ['classifys.id'], ),
    sa.ForeignKeyConstraint(['Post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['Tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('marks')
    op.drop_index(op.f('ix_tags_tag'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_classifys_classify'), table_name='classifys')
    op.drop_table('classifys')
    # ### end Alembic commands ###
