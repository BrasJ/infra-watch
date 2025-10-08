from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.db.models.host import Host
from app.schemas.host import HostCreate

def create_host(db: Session, host_data: HostCreate) -> Host:
    db_host = Host(**host_data.model_dump())
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

def update_host(db:Session, host_id: int, host_data: HostCreate) -> Host:
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")

    host.hostname = host_data.hostname
    host.ip_address = host_data.ip_address
    host.os = host_data.os
    host.status = host_data.status
    db.commit()
    db.refresh(host)
    return host

def delete_host(db: Session, host_id: int) -> None:
    host = db.query(Host).filter(Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")

    db.delete(host)
    db.commit()