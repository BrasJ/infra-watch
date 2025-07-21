from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AlertBase(BaseModel):
    snapshot_id: int
    message: str
    severity: str

class AlertCreate(AlertBase):
    pass

class AlertRead(AlertBase):
    id: int
    acknowledged: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)