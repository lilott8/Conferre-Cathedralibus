from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .base_model import BaseModel


class Timeline(BaseModel):
    __tablename__ = 'timeline'
    id = Column(Integer, primary_key=True)
    cathedral_id = Column(Integer, ForeignKey('cathedral.id'), nullable=False)
    event = Column(String)
    description = Column(Text, nullable=True)
    start_date = Column(String)
    end_date = Column(String)

    church = relationship("cathedral", back_populates="timeline")