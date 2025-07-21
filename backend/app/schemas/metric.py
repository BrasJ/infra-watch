from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MetricBase(BaseModel):
    name: str
    unit: str | None = None
    description: str | None = None

class MetricCreate(MetricBase):
    snapshot_id: int

class MetricRead(MetricBase):
    id: int
    snapshot_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)