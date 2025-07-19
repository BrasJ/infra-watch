from pydantic import BaseModel
from datetime import datetime

class HostBase(BaseModel):
    hostname: str
    ip_address: str | None = None

class HostCreate(HostBase):
    pass

class HostRead(HostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True