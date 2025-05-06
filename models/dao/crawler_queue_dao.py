from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import CrawlerQueue, CrawlerStatus


class CrawlerQueueDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_next_url(self):
        result = await self.db.execute(
            select(CrawlerQueue)
            .where(CrawlerQueue.status == CrawlerStatus.pending)
            .order_by(CrawlerQueue.relevance.desc())
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        return result.scalar_one_or_none()

    async def mark_in_progress(self, task: CrawlerQueue):
        task.status = CrawlerStatus.in_progress
        task.last_attempt = datetime.utcnow()
        await self.db.commit()

    async def mark_done(self, task_id: int):
        await self.db.execute(
            CrawlerQueue.__table__.update()
            .where(CrawlerQueue.id == task_id)
            .values(status=CrawlerStatus.done)
        )
        await self.db.commit()

    async def mark_failed(self, task_id: int):
        await self.db.execute(
            CrawlerQueue.__table__.update()
            .where(CrawlerQueue.id == task_id)
            .values(status=CrawlerStatus.failed)
        )
        await self.db.commit()

    async def add_if_not_exists(self, url: str, relevance: float = 0.5):
        exists = await self.db.execute(
            select(CrawlerQueue).where(CrawlerQueue.url == url)
        )
        if not exists.scalar_one_or_none():
            self.db.add(CrawlerQueue(
                url=url,
                relevance=relevance,
                status=CrawlerStatus.pending,
                last_attempt=datetime.utcnow()
            ))
            await self.db.commit()