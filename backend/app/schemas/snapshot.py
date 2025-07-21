from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SnapshotBase(BaseModel):
    host_id: int

class SnapshotCreate(SnapshotBase):
    pass

class SnapshotRead(SnapshotBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)