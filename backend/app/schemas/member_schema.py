from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class MemberOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    email: EmailStr
    password: str = Field(min_length=6)
    join_date: datetime | None = None


class MemberLogin(BaseModel):
    email: EmailStr
    password: str


class MemberPayload(BaseModel):
    member_id: int
