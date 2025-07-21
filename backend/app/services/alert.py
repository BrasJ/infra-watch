from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException

from app.db.models.alert import Alert
from app.schemas.alert import AlertFilter, AlertUpdate, AlertCreate, AlertRead, AlertSeverity

def create_alert(
    db: Session,
    alert_data: AlertCreate
) -> Alert:
    alert = Alert(**alert_data.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_alert(
    db: Session,
    alert_id: int
) -> Alert:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

def list_alerts(
    db: Session,
    snapshot_id: Optional[int] = None,
    severity: Optional[AlertSeverity] = None,
    acknowledged: Optional[bool] = None
) -> List[Alert]:
    filters = []

    if snapshot_id is not None:
        filters.append(Alert.snapshot_id == snapshot_id)
    if severity is not None:
        filters.append(Alert.severity == severity)
    if acknowledged is not None:
        filters.append(Alert.acknowledged == acknowledged)

    return db.query(Alert).filter(and_(*filters)).all()

def update_alert(
    db: Session,
    alert_id: int,
    alert_data: AlertUpdate
) -> Alert:
    alert = get_alert(db, alert_id)

    update_data = alert_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)
    return alert

def delete_alert(
    db: Session,
    alert_id: int
) -> None:
    alert = get_alert(db, alert_id)
    db.delete(alert)
    db.commit()