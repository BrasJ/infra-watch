from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

class AlertSeverity(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"

class AlertRuleBase(BaseModel):
    host_id: Optional[int] = None
    metric_name: str
    operator: str
    threshold: float
    severity: AlertSeverity
    message: str
    enabled: bool = True

class AlertRuleCreate(AlertRuleBase):
    pass

class AlertRuleUpdate(AlertRuleBase):
    pass

class AlertRuleRead(AlertRuleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)