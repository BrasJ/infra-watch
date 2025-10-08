from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.snapshot import SnapshotCreate, SnapshotRead
from app.services.snapshot import (
    create_snapshot,
    get_snapshot_by_id,
    list_snapshots,
    delete_snapshot,
)

router = APIRouter(prefix="/snapshots", tags=["snapshots"])

@router.post("/", response_model=SnapshotRead)
def create_snapshot_endpoint(
    snapshot_data: SnapshotCreate,
    db: Session = Depends(get_db)
):
    return create_snapshot(db, snapshot_data)

@router.get("/{snapshot_id}", response_model=SnapshotRead)
def get_snapshot_endpoint(snapshot_id: int, db: Session = Depends(get_db)):
    return get_snapshot_by_id(db, snapshot_id)

@router.get("/", response_model=List[SnapshotRead])
def list_snapshots_endpoint(
    host_id: Optional[int] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    return list_snapshots(db, host_id=host_id, limit=limit)

@router.delete("/{snapshot_id}", status_code=204)
def delete_snapshot_endpoint(snapshot_id: int, db: Session = Depends(get_db)):
    delete_snapshot(db, snapshot_id)
