from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.host import HostCreate, HostRead
from app.services.host import create_host, get_all_hosts, get_host_by_id
from app.db.session import get_db

print("Host router loaded")

router = APIRouter(prefix="/hosts", tags=["hosts"])

@router.post("/", response_model=HostRead)
def register_host(host: HostCreate, db: Session = Depends(get_db)):
    return create_host(db, host)

@router.get("/", response_model=List[HostRead])
def list_hosts(db: Session = Depends(get_db)):
    return get_all_hosts(db)

@router.get("/{host_id}", response_model=HostRead)
def get_host(host_id: int, db: Session = Depends(get_db)):
    return get_host_by_id(db, host_id)