from .base_model import BaseModel
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey


class Corpus(BaseModel):
    __tablename__ = "corpus"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True, nullable=True)
    domain = Column(String)
    path = Column(String)
    title = Column(String)
    hash = Column(String)
    relevance = Column(Float)
    last_scraped = Column(DateTime, default=datetime.now(UTC))
