from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
import enum


class CrawlerStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class CrawlerQueue(BaseModel):
    __tablename__ = "enqueue"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    domain = Column(String)
    relevance = Column(Float, default=0)
    status = Column(Enum(CrawlStatus), default=CrawlStatus.pending)
    last_attempt = Column(DateTime)
