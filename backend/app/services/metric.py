from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.db.models.metric import Metric
from app.schemas.metric import MetricCreate

def create_metric(db: Session, metric_data: MetricCreate) -> Metric:
    metric = Metric(**metric_data.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def get_metrics_by_snapshot(db: Session, snapshot_id: int) -> List[Metric]:
    return db.query(Metric).filter(Metric.snapshot_id == snapshot_id).all()

def get_metric_by_id(db: Session, metric_id: int) -> Metric:
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

def delete_metric_by_id(db: Session, metric_id: int) -> None:
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()