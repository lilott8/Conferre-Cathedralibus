from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship


class Cathedral(BaseModel):
    __tablename__ = "cathedral"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    denomination = Column(String)
    tradition = Column(String)
    website = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    denomination = Column(String)
    commissioned_by = Column(String)
    dimensions = Column(String)
    architectural_style = Column(String)
    attendance = Column(String)

    timeline = relationship("timeline", back_populates="cathedral", cascade="all, delete-orphan")

