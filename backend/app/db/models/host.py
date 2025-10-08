from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.db.base import Base

class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=True)
    os = Column(String, nullable=True)
    status = Column(String, nullable=True)
    snapshots = relationship('Snapshot', back_populates='host', cascade="all, delete-orphan")
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))