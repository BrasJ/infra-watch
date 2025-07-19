from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, UTC

from app.db.base import Base

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey('snapshots.id'))
    message = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    acknowledged = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))