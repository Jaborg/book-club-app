from datetime import datetime

from pydantic import BaseModel, Field

from .member_schema import MemberOut


class BookOut(BaseModel):
    id: int
    name: str
    author: str
    rating: str
    due_date: datetime
    member: MemberOut | None = None

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    name: str
    author: str
    member_id: int
    due_date: datetime = Field(..., description="When the book is due to be discussed")
    rating: str = Field(None, description="The book rating")


class BookCreate(BookBase):
    initial_date: datetime
    pass


class CreateResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True
