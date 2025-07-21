from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.snapshot import SnapshotCreate, SnapshotRead
from app.services.snapshot import (
    create_snapshot,
    get_snapshot,
    list_snapshots_by_host,
    delete_snapshot
)
from app.db.session import get_db

router = APIRouter(prefix="/snapshots", tags=["snapshots"])

@router.post("/", response_model=SnapshotRead)
def register_snapshot(
        snapshot: SnapshotCreate,
        db: Session = Depends(get_db)
):
    return create_snapshot(db, snapshot)

@router.get("/{snapshot_id}", response_model=SnapshotRead)
def retrieve_snapshot(
        snapshot_id: int,
        db: Session = Depends(get_db)
):
    return get_snapshot(db, snapshot_id)

@router.get("/host/{host_id}", response_model=List[SnapshotRead])
def list_host_snapshots(
        host_id: int,
        db: Session = Depends(get_db)
):
    return list_snapshots_by_host(db, host_id)

@router.delete("/{snapshot_id}", status_code=204)
def remove_snapshot(
        snapshot_id: int,
        db: Session = Depends(get_db)
):
    delete_snapshot(db, snapshot_id)
    return