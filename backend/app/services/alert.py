from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.db.models.alert import Alert
from app.schemas.alert import AlertFilter, AlertUpdate

def list_alerts(
        db: Session,
        filters: AlertFilter = AlertFilter()
) -> List[Alert]:
    query = select(Alert)

    if filters.severity is not None:
        query = query.where(Alert.severity == filters.severity)
    if filters.acknowledged is not None:
        query = query.where(Alert.acknowledged == filters.acknowledged)
    else:
        query = query.where(Alert.acknowledged == False)

    return db.execute(query).scalars().all()

def update_alert(
    db: Session,
    alert_id: int,
    alert_data: AlertUpdate
) -> Alert:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    update_data = alert_data.model_dump(exclude_unset=True)
    for key, values in update_data.items():
        setattr(alert, key, values)

    db.commit()
    db.refresh(alert)
    return alert