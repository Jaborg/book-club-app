from datetime import datetime

from pydantic import BaseModel


class MemberOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    join_date: datetime
    pass
