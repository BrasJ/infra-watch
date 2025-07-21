from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MetricBase(BaseModel):
    snapshot_id: int
    name: str
    value: float
    unit: Optional[str] = None
    description: Optional[str] = None

class MetricCreate(MetricBase):
    pass

class MetricRead(MetricBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)