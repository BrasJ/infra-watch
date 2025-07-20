from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.db.models.host import Host
from app.schemas.host import HostCreate

def create_host(db: Session, host_data: HostCreate) -> Host:
    db_host = Host(**host_data.dict())
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

def get_all_hosts(db: Session) -> List[Host]:
    return db.query(Host).all()

def get_host_by_id(db: Session, host_id: int) -> Host:
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    return host