from pydantic import BaseModel
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

    class Config:
        orm_mode = True