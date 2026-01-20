from pydantic import BaseModel

from .book_schema import BookOut
from .member_schema import MemberOut


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    member_ids: list[int] = []
    active_book_id: int | None = None


class GroupOut(BaseModel):
    id: int
    name: str
    members: list[MemberOut] = []
    active_book: BookOut | None = None

    class Config:
        from_attributes = True
