from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy import desc

from app.db.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricRead
from app.db.models.snapshot import Snapshot

def create_metric(db: Session, metric_data: MetricCreate) -> Metric:
    metric = Metric(**metric_data.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def get_metrics_by_snapshot(db: Session, snapshot_id: int) -> List[Metric]:
    print(f"Fetching metrics for snapshot {snapshot_id}")
    return db.query(Metric).filter(Metric.snapshot_id == snapshot_id).all()

def get_metric_by_id(db: Session, metric_id: int) -> Metric:
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

def list_metrics(db: Session, host_id: Optional[int] = None, limit: int = 100) -> List[Metric]:
    query = db.query(Metric)
    if host_id:
        query = query.filter(Metric.host_id == host_id)
    return query.order_by(desc(Metric.created_at)).limit(limit).all()

def get_latest_metric_for_host(db: Session, host_id: int) -> Optional[Metric]:
    return (
        db.query(Metric)
        .filter(Metric.host_id == host_id)
        .order_by(desc(Metric.created_at))
        .first()
    )

def delete_metric(db: Session, metric_id: int) -> None:
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()

def list_metrics_with_hosts(db: Session, host_id: int) -> List[Metric]:
    return (
        db.query(Metric)
        .filter(Metric.host_id == host_id)
        .order_by(Metric.snapshot_id, Metric.created_at)
        .all()
    )

