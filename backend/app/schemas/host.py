from pydantic import BaseModel
from datetime import datetime

class HostBase(BaseModel):
    hostname: str
    ip_address: str | None = None

class HostCreate(HostBase):
    hostname: str
    ip_address: str

class HostRead(HostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }