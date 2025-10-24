from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from backend.app.db.models.snapshot import Snapshot
from backend.app.schemas.snapshot import SnapshotCreate, SnapshotRead

def create_snapshot(db: Session, snapshot_data: SnapshotCreate) -> Snapshot:
    snapshot = Snapshot(**snapshot_data.model_dump())
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

def list_snapshots(
    db: Session,
    host_id: Optional[int] = None,
    limit: int = 100
) -> List[SnapshotRead]:
    query = db.query(Snapshot)
    if host_id:
        query = query.filter(Snapshot.host_id == host_id)
    return query.order_by(Snapshot.created_at.desc()).limit(limit).all()

def get_snapshot(db: Session, snapshot_id: int) -> Snapshot:
    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot

def delete_snapshot(db: Session, snapshot_id: int) -> None:
    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    db.delete(snapshot)
    db.commit()