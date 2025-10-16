from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MetricBase(BaseModel):
    id: int
    name: str
    value: float
    created_at: datetime
    snapshot_id: int
    host_id: int

class MetricCreate(MetricBase):
    pass

class MetricRead(MetricBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MetricGroupedByHost(BaseModel):
    id: int
    name: str
    value: float
    created_at: datetime
    snapshot_id: int
    host_id: int

    model_config = ConfigDict(from_attributes=True)
