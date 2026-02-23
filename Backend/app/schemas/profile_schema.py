from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProfileCreate(BaseModel):
    profile_name: str
    age: Optional[int]
    gender: Optional[str]


class ProfileResponse(BaseModel):
    id: int
    profile_name: str
    age: Optional[int]
    gender: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
