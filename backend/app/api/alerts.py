from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate
from app.services import alert as alert_service

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Create alert
@router.post("/", response_model=AlertRead)
def create_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    return alert_service.create_alert(db, alert_in)

# Get alert by ID
@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    return alert_service.get_alert_by_id(db, alert_id)

# List all alerts
@router.get("/", response_model=List[AlertRead])
def list_alerts(db: Session = Depends(get_db)):
    return alert_service.list_alerts(db)

# Filter alerts by severity or acknowledged
@router.get("/filter", response_model=List[AlertRead])
def filter_alerts(
    severity: Optional[str] = Query(None),
    acknowledged: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return alert_service.filter_alerts(db, severity=severity, acknowledged=acknowledged)

# Update alert by ID
@router.put("/{alert_id}", response_model=AlertRead)
def update_alert(alert_id: int, alert_in: AlertUpdate, db: Session = Depends(get_db)):
    return alert_service.update_alert(db, alert_id, alert_in)

# Delete alert by ID
@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert_service.delete_alert(db, alert_id)
    return
