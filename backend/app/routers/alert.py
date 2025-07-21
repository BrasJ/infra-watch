from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate, AlertFilter
from app.services.alert import list_alerts, update_alert

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=List[AlertRead])
def get_alerts(
        severity: AlertFilter.severity | None = None,
        acknowledged: bool | None = None,
        db: Session = Depends(get_db),
):
    filters = AlertFilter(severity=severity, acknowledged=acknowledged)
    return list_alerts(db, filters)

@router.put("/{alert_id}", response_model=AlertRead)
def put_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
):
    return update_alert(db, alert_id, alert_data)