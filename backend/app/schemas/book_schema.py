from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.member_schema import MemberOut as MemberOutFull

from .member_schema import MemberOut


class BookBase(BaseModel):
    name: str
    author: str
    member_id: int
    original_due_date: datetime = Field(..., description="The original due date chosen")
    revised_due_date: datetime = Field(None, description="The revised due date chosen")
    rating: str = Field(None, description="The book rating")


class BookOut(BaseModel):
    id: int
    name: str
    author: str
    rating: str
    original_due_date: datetime
    member: MemberOut | None = None
    member_full: MemberOutFull | None = None

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    initial_date: datetime
    pass


class BookPayload(BaseModel):
    book_id: int
