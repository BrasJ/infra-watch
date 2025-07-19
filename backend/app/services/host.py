from sqlalchemy.orm import Session

from app.db.models.host import Host
from app.schmas.host import HostCreate

def create_host(db: Session, host_data: HostCreate) -> Host:
    db_host = Host(**host_data.dict())
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host