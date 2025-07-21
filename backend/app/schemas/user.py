from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)