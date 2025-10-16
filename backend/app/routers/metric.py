from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.metric import MetricCreate, MetricRead, MetricGroupedByHost
from app.services.metric import (
    create_metric,
    get_metrics_by_snapshot,
    get_metric_by_id,
    delete_metric,
    get_latest_metric_for_host,
    list_metrics
)
from app.db.session import get_db

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/", response_model=MetricRead)
def register_metric(
        metric: MetricCreate,
        db: Session = Depends(get_db)
):
    return create_metric(db, metric)

@router.get("/", response_model=List[MetricRead])
def list_metrics_endpoint(
    host_id: Optional[int] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    return list_metrics(db, host_id=host_id, limit=limit)

@router.get("/snapshot/{snapshot_id}", response_model=List[MetricRead])
def list_metrics_by_snapshot(
        snapshot_id: int,
        db: Session = Depends(get_db)
):
    print(f"Fetching metrics for snapshot {snapshot_id}")
    return get_metrics_by_snapshot(db, snapshot_id)

@router.get("/{metric_id}", response_model=MetricRead)
def get_metric(
        metric_id: int,
        db: Session = Depends(get_db)
):
    return get_metric_by_id(db, metric_id)

@router.get('/latest', response_model=MetricRead)
def get_latest_metric(
    host_id: int,
    db: Session = Depends(get_db)
):
    return get_latest_metric_for_host(db, host_id)

@router.delete("/{metric_id}", status_code=204)
def remove_metric(
        metric_id: int,
        db: Session = Depends(get_db)
):
    delete_metric(db, metric_id)
    return

@router.get("/grouped/host", response_model=List[MetricGroupedByHost])
def get_metrics_grouped_by_host(
    db: Session = Depends(get_db)
):
    from app.services.metric import list_metrics_with_hosts
    return list_metrics_with_hosts(db)