from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.metric import MetricRead
from app.services.metric import (
    get_latest_metric_for_host,
    get_metrics_by_snapshot,
    list_metrics
)

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/", response_model=List[MetricRead])
def list_metrics_endpoint(
    host_id: Optional[int] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    return list_metrics(db, host_id=host_id, limit=limit)

@router.get('/latest', response_model=MetricRead)
def get_latest_metric(
    host_id: int,
    db: Session = Depends(get_db)
):
    return get_latest_metric_for_host(db, host_id)

@router.get("/snapshot/{snapshot_id}", response_model=MetricRead)
def get_metric_by_snapshot_endpoint(
    snapshot_id: int,
    db: Session = Depends(get_db)
):
    return get_metrics_by_snapshot(db, snapshot_id)