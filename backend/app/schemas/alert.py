from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class SeverityLevel(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"

class AlertBase(BaseModel):
    message: Optional[str] = None
    severity: Optional[SeverityLevel] = None
    acknowledged: Optional[bool] = None

class AlertUpdate(AlertBase):
    model_config = ConfigDict(from_attributes=True)

class AlertCreate(AlertBase):
    message: str
    severity: SeverityLevel
    acknowledged: bool = False

class AlertUpdate(BaseModel):
    message: Optional[str] = None
    severity: Optional[SeverityLevel] = None
    acknowledged: Optional[bool] = None

class AlertFilter(BaseModel):
    severity: Optional[SeverityLevel] = None
    acknowledged: Optional[bool] = None

class AlertRead(AlertBase):
    id: int
    snapshot_id: Optional[int]
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)