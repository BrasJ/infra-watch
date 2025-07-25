from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.db.base import Base

class Snapshot(Base):
    __tablename__ = 'snapshots'

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey('hosts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    metrics = relationship('Metric', back_populates='snapshot', cascade='all, delete-orphan')
    host = relationship('Host', back_populates='snapshots')
    alerts = relationship('Alert', back_populates='snapshot', cascade='all, delete-orphan')