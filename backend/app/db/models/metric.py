from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.db.base import Base

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    description = Column(String, nullable=True)

    snapshot = relationship('Snapshot', back_populates='metrics')