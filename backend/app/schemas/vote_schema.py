from datetime import datetime

from pydantic import BaseModel


class VoteCreate(BaseModel):
    candidate_book_ids: list[int]


class VoteOut(BaseModel):
    id: int
    group_id: int
    created_by_id: int
    is_open: bool
    created_at: datetime

    class Config:
        from_attributes = True


class VoteCastPayload(BaseModel):
    book_id: int


class CloseVoteResponse(BaseModel):
    winning_book_id: int
