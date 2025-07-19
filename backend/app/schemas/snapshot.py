from pydantic import BaseModel
from datetime import datetime

class SnapshotBase(BaseModel):
    host_id: int

class SnapshotCreate(SnapshotBase):
    pass

class SnapshotRead(SnapshotBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True