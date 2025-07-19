from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.host import HostCreate, HostRead
from app.services.host import create_host
from app.db.session import get_db

router = APIRouter(prefix="/hosts", tags=["hosts"])

@router.get("/", response_model=HostRead)
def register_host(host: HostCreate, db: Session = Depends(get_db)):
    return create_host(db, host)