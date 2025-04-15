from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
import enum


class CrawlStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class ScraperQueue(BaseModel):
    __tablename__ = "scrape_queue"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    domain = Column(String)
    relevance = Column(Float, default=0)
    status = Column(Enum(CrawlStatus), default=CrawlStatus.pending)
    last_attempt = Column(DateTime)
