from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.models.host import Host
from backend.app.db.models.snapshot import Snapshot
from backend.app.db.models.metric import Metric
from backend.app.db.models.alert import Alert
from backend.app.schemas.dashboard import DashboardStats, DashboardAlert, AlertTrendEntry, MetricInsight

def get_dashboard_stats(db: Session) -> DashboardStats:
    now = datetime.utcnow()
    one_day_ago = now - timedelta(hours=24)

    total_hosts = db.query(func.count(Host.id)).scalar()
    snapshots_24h = db.query(func.count(Snapshot.id)).filter(Snapshot.created_at >= one_day_ago).scalar()
    metrics_24h = db.query(func.count(Metric.id)).filter(Metric.created_at >= one_day_ago).scalar()

    return DashboardStats(
        totalHosts=total_hosts or 0,
        snapshotsLast24h=snapshots_24h or 0,
        metricsLast24h=metrics_24h or 0
    )

def get_recent_alerts(db: Session, limit: int = 5):
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )
    return alerts

def get_alert_trends(db: Session):
    one_day_ago = datetime.utcnow() - timedelta(hours=24)

    # Group alerts per host by hour
    results = (
        db.query(
            func.date_trunc('hour', Alert.created_at).label('timestamp'),
            Alert.host_id,
            func.count(Alert.id).label('count')
        )
        .filter(Alert.created_at >= one_day_ago)
        .group_by(func.date_trunc('hour', Alert.created_at), Alert.host_id)
        .order_by('timestamp')
        .all()
    )

    return [
        {
            "timestamp": r.timestamp,
            "host_id": r.host_id,
            "count": r.count,
        }
        for r in results
    ]

def get_metric_insights(db: Session):
    one_day_ago = datetime.utcnow() - timedelta(hours=24)

    results = (
        db.query(
            Metric.host_id,
            Metric.name.label("metric_name"),
            func.avg(Metric.value).label("avg_value"),
            func.max(Metric.value).label("max_value")
        )
        .filter(Metric.created_at >= one_day_ago)
        .group_by(Metric.host_id, Metric.name)
        .all()
    )

    # Enrich with hostnames
    host_map = {h.id: h.hostname for h in db.query(Host).all()}

    return [
        {
            "host_id": r.host_id,
            "hostname": host_map.get(r.host_id, f"Host {r.host_id}"),
            "metric_name": r.metric_name,
            "avg_value": round(r.avg_value, 2),
            "max_value": round(r.max_value, 2),
        }
        for r in results
    ]