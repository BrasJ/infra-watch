from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.session import get_db
from backend.app.schemas.alert import AlertCreate, AlertRead, AlertUpdate, AlertFilter, AlertSeverity
from backend.app.services.alert import (
    create_alert,
    get_alert,
    list_alerts,
    update_alert,
    delete_alert
)

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/", response_model=AlertRead)
def create_alert_endpoint(
    alert: AlertCreate,
    db: Session = Depends(get_db),
):
    return create_alert(db, alert)

@router.get("/", response_model=List[AlertRead])
def list_alerts_endpoint(
        snapshot_id: Optional[int] = Query(None),
        severity: Optional[AlertSeverity] = Query(None),
        acknowledged: Optional[bool] = Query(None),
        db: Session = Depends(get_db),
):
    return list_alerts(db, snapshot_id, severity, acknowledged)

@router.get("/{alert_id}", response_model=AlertRead)
def get_alert_endpoint(
        alert_id: int,
        db: Session = Depends(get_db),
):
    return get_alert(db, alert_id)

@router.put("/{alert_id}", response_model=AlertRead)
def update_alert_endpoint(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
):
    return update_alert(db, alert_id, alert_data)

@router.delete("/{alert_id}", status_code=204)
def delete_alert_endpoint(
        alert_id: int,
        db: Session = Depends(get_db),
):
    delete_alert(db, alert_id)

@router.patch("/{alert_id}", response_model=AlertRead)
def acknowledge_alert(alert_id: int, alert_data: AlertUpdate, db: Session = Depends(get_db)):
    return update_alert(db, alert_id, alert_data)