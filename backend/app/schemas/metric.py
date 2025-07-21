from pydantic import BaseModel, ConfigDict

class MetricBase(BaseModel):
    name: str
    unit: str | None = None
    description: str | None = None

class MetricCreate(MetricBase):
    pass

class MetricRead(MetricBase):
    id: int

    model_config = ConfigDict(from_attributes=True)