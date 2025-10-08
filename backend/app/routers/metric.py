from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.metric import MetricCreate, MetricRead
from app.services.metric import (
    create_metric,
    get_metric_by_snapshot,
    get_metric_by_id,
    delete_metric,
)
from app.db.session import get_db

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/", response_model=MetricRead)
def register_metric(
        metric: MetricCreate,
        db: Session = Depends(get_db)
):
    return create_metric(db, metric)

@router.get("/snapshot/{snapshot_id}", response_model=List[MetricRead])
def list_metrics_by_snapshot(
        snapshot_id: int,
        db: Session = Depends(get_db)
):
    return get_metrics_by_snapshot(db, snapshot_id)

@router.get("/{metric_id}", response_model=MetricRead)
def get_metric(
        metric_id: int,
        db: Session = Depends(get_db)
):
    return get_metric_by_id(db, metric_id)

@router.delete("/{metric_id}", status_code=204)
def remove_metric(
        metric_id: int,
        db: Session = Depends(get_db)
):
    delete_metric(db, metric_id)
    return