from config import Config
import asyncio
from datetime import datetime

from .crawler import Crawler
# from scraper.db import SessionLocal
# from scraper.dao.url_queue_dao import UrlQueueDAO
# from scraper.models import CrawlStatus

class CrawlerController(object):

    def __init__(self, config: Config):
        self.config = config

    async def seed_urls(self):
            async with SessionLocal() as db:
                dao = UrlQueueDAO(db)
                for url in self.seeds:
                    await dao.add_if_not_exists(url, relevance=1.0)

    async def start(self):
        await self.seed_urls()


        workers = [
            Crawler(worker_id=i, delay=self.delay)
            for i in range(self.num_workers)
        ]
        await asyncio.gather(*(w.run() for w in workers))