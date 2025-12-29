from pydantic import BaseModel, Field
from datetime import datetime


class BookBase(BaseModel):
    name: str
    author: str
    member_id: int
    due_date: datetime = Field(..., description="When the book is due to be discussed")
    rating: str = Field(None, description="The book rating")


class BookCreate(BookBase):
    initial_date: datetime
    pass


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    join_date: datetime
    pass
