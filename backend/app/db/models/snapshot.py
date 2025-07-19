from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.db.base import Base

class Snapshot(Base):
    __tablename__ = 'snapshots'

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey('hosts.id'), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    host = relationship('Host', backref='snapshots')