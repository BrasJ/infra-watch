from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.db.models.snapshot import Snapshot
from app.schemas.snapshot import SnapshotCreate

def create_snapshot(db: Session, snapshot_data: SnapshotCreate) -> Snapshot:
    snapshot = Snapshot(**snapshot_data.model_dump())
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

def get_snapshot(db: Session, snapshot_id: int) -> Snapshot:
    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot

def list_snapshots_by_host(db: Session, host_id: int) -> List[Snapshot]:
    return db.query(Snapshot).filter(Snapshot.host == host_id).all()

def delete_snapshot(db: Session, snapshot_id: int) -> None:
    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    db.delete(snapshot)
    db.commit()