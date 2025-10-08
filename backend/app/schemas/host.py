from pydantic import BaseModel, ConfigDict
from datetime import datetime

class HostBase(BaseModel):
    hostname: str
    ip_address: str | None = None
    os: str | None = None
    status: str | None = None

class HostCreate(HostBase):
    hostname: str
    ip_address: str
    os: str
    status: str

class HostRead(HostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)