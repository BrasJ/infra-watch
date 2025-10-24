from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services import dashboard as dashboard_service
from backend.app.schemas.dashboard import DashboardStats, DashboardAlert, AlertTrendEntry, MetricInsight

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):
    return dashboard_service.get_dashboard_stats(db)

@router.get("/alerts/recent", response_model=list[DashboardAlert])
def recent_alerts(db: Session = Depends(get_db)):
    return dashboard_service.get_recent_alerts(db)

@router.get("/alerts/trends", response_model=list[AlertTrendEntry])
def alert_trends(db: Session = Depends(get_db)):
    return dashboard_service.get_alert_trends(db)

@router.get("/metrics/insights", response_model=list[MetricInsight])
def metric_insights(db: Session = Depends(get_db)):
    return dashboard_service.get_metric_insights(db)