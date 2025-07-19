from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base import Base

class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)