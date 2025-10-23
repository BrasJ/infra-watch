from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DashboardStats(BaseModel):
    totalHosts: int
    snapshotsLast24h: int
    metricsLast24h: int

class DashboardAlert(BaseModel):
    id: int
    message: str
    severity: str
    host_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class AlertTrendEntry(BaseModel):
    timestamp: datetime
    host_id: int
    count: int

class MetricInsight(BaseModel):
    host_id: int
    hostname: Optional[str]
    metric_name: str
    avg_value: float
    max_value: float