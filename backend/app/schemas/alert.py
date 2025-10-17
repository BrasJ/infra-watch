from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class AlertSeverity(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"

class AlertBase(BaseModel):
    message: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    acknowledged: Optional[bool] = None
    type: Optional[str] = None
    host_id: Optional[int] = None
    snapshot_id: int

class AlertCreate(AlertBase):
    snapshot_id: int
    message: str
    severity: AlertSeverity
    type: str
    acknowledged: bool = False

class AlertUpdate(BaseModel):
    acknowledged: Optional[bool] = None

class AlertFilter(BaseModel):
    severity: Optional[AlertSeverity] = None
    acknowledged: Optional[bool] = None

class AlertRead(AlertBase):
    id: int
    snapshot_id: Optional[int]
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)