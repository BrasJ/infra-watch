from pydantic import BaseModel

class MetricBase(BaseModel):
    name: str
    unit: str | None = None
    description: str | None = None

class MetricCreate(MetricBase):
    pass

class MetricRead(MetricBase):
    id: int

    class Config:
        orm_mode = True