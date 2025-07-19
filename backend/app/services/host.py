from sqlalchemy.orm import Session
from typing import List

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