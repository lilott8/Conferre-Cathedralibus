"""Initial church schema

Revision ID: 202404131000
Revises:
Create Date: 2025-04-13 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '202404131000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # op.create_table(
    #     'cathedrals',
    #     sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    #     sa.Column('name', sa.String(), nullable=True),
    #     sa.Column('latitude', sa.String(), nullable=True),
    #     sa.Column('longitude', sa.String(), nullable=True),
    #     sa.Column('denomination', sa.String(), nullable=True),
    #     sa.Column('commissioned_by', sa.String(), nullable=True),
    #     sa.Column('dimensions', sa.String(), nullable=True),
    #     sa.Column('architectural_style', sa.String(), nullable=True),
    #     sa.Column('attendance', sa.String(), nullable=True),
    # )

    # op.create_table(
    #     'timeline',
    #     sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
    #     sa.Column('cathedral_id', sa.Integer(), sa.ForeignKey('cathedrals.id', ondelete="CASCADE"), nullable=False),
    #     sa.Column('event', sa.String(), nullable=True),
    #     sa.Column('description', sa.Text(), nullable=True),
    #     sa.Column('date', sa.String(), nullable=True),
    # )
    # crawl_status = sa.Enum('pending', 'in_progress', 'done', 'failed', name='crawl_status_enum')
    # crawl_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'scrape_queue',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("url", sa.String(), unique=True, nullable=False),
        sa.Column('domain', sa.String()),
        sa.Column("relevance", sa.Float()),
        # sa.Column("status", crawl_status),
        sa.Column("status", sa.String()),
        sa.Column('last_attempt', sa.String(), nullable=True)
    )

    # op.create_index("idx_scraper_queue_url", "scrape_queue", "url")

    op.create_table(
        "corpus",
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('url', sa.String()),
        sa.Column('domain', sa.String()),
        sa.Column('path', sa.String()),
        sa.Column('title', sa.String()),
        sa.Column('hash', sa.String()),
        sa.Column('relevance', sa.Float()),
        sa.Column('last_scraped', sa.String())
    )

    # op.create_index('idx_corpus_url', 'corpus', 'url')


def downgrade():
    op.drop_column('scrap_queue', 'status')
    crawl_status = sa.Enum('pending', 'in_progress', 'done', 'failed', name='crawl_status_enum')
    crawl_status.drop(op.get_bind())
    op.drop_table('corpus')
    op.drop_table('scrape_queue')
