from sqlalchemy import Column, Integer, String, DateTime

from app.db.base import Base

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(String, nullable=True)