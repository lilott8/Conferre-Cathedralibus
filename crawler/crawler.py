import colorlog

from config import Config
import aiohttp
import asyncio
import hashlib
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from models.base_model import get_session
from models.dao.crawler_queue_dao import CrawlerQueueDAO
from models.dao.corpus_dao import CorpusDao


class Crawler(object):

    def __init__(self, working_dir: str, db_url, worker_id, delay=1.5):
        self.logger = colorlog.getLogger(Crawler.__name__)
        self.worker_id = worker_id
        self.db_url = db_url
        self.delay = delay
        self.working_dir = working_dir

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with get_session(self.db_url) as db:
                    crawler_dao = CrawlerQueueDAO(db)
                    task = await crawler_dao.get_next_url()

                    if not task:
                        print(f"[Worker {self.worker_id}] No more work.")
                        return

                    await crawler_dao.mark_in_progress(task)

                try:
                    await self.crawl_url(task.id, task.url, session)
                    async with get_session(self.db_url) as db:
                        await CrawlerQueueDAO(db).mark_done(task.id)
                except Exception as e:
                    print(f"[Worker {self.worker_id}] Failed: {task.url} — {e}")
                    async with get_session(self.db_url) as db:
                        await CrawlerQueueDAO(db).mark_failed(task.id)
                await asyncio.sleep(self.delay)

    async def crawl_url(self, task_id, url, session):
        self.logger.info(f"[Worker {self.worker_id}] Crawling: {url}")
        async with session.get(url, timeout=10) as response:
            html = await response.text()
        hashed = hashlib.sha256(url.encode()).hexdigest()

        filename = self.save_html(url, html, hashed)

        async with get_session(self.db_url) as db:
            await CorpusDao(db).save(url=url, domain=self.extract_domain(url), path=filename,
                                     title=self.extract_title(html), hash=hashed)

        links = self.extract_links(html)
        async with get_session(self.db_url) as db:
            dao = CrawlerQueueDAO(db)
            for link in links:
                await dao.add_if_not_exists(link)

    def save_html(self, url, html, hashed):
        path = os.path.join(self.working_dir, f"{hashed}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def extract_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return {
            a["href"]
            for a in soup.find_all("a", href=True)
            if a["href"].startswith("http")
        }

    def extract_title(self, html):
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        return title_tag.text.strip() if title_tag else "No Title"

    def extract_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc
