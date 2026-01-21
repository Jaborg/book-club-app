from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.exceptions import ensure_exists
from app.models.book_group import BookGroup
from app.schemas.book_schema import BookPayload
from app.schemas.group_schema import GroupCreate, GroupOut
from app.schemas.member_schema import MemberPayload
from app.schemas.vote_schema import (
    CloseVoteResponse,
    VoteCastPayload,
    VoteCreate,
)
from app.utilities import admin_required, get_current_member

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=list[GroupOut])
def list_groups(db: Session = Depends(get_db)):
    # Delegate to CRUD helper
    return crud.get_all(db, BookGroup)


@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_by_id(db, BookGroup, group_id)
    return ensure_exists(group, "Group")


@router.post("/", response_model=dict, status_code=201)
def create_group(
    payload: GroupCreate, db: Session = Depends(get_db), _admin=Depends(admin_required)
):
    # Delegate validation and creation to crud.create_group
    group = crud.create_group(
        db,
        name=payload.name,
        member_ids=payload.member_ids,
        active_book_id=payload.active_book_id,
    )
    return {"message": "Group created", "id": group.id}


@router.post("/{group_id}/votes", response_model=dict)
def create_vote_for_group(
    group_id: int,
    payload: VoteCreate,
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    """Admin-only: create a vote for this group with candidate book ids."""
    vote = crud.create_vote(
        db,
        group_id=group_id,
        creator_id=_admin.id,
        candidate_book_ids=payload.candidate_book_ids,
    )
    return {"message": "Vote created", "id": vote.id}


@router.post("/{group_id}/votes/{vote_id}/cast", response_model=dict)
def cast_vote_for_group(
    group_id: int,
    vote_id: int,
    payload: VoteCastPayload,
    db: Session = Depends(get_db),
    current_member=Depends(get_current_member),
):
    # ensure the vote belongs to the group
    # crud.get_by_id expects a model;
    # import Vote model dynamically to avoid circular imports
    from app.models.vote_model import Vote

    vote = crud.get_by_id(db, Vote, vote_id)
    ensure_exists(vote, "Vote")
    crud.cast_vote(
        db, vote_id=vote_id, voter_id=current_member.id, book_id=payload.book_id
    )
    return {"message": "Vote cast"}


@router.post("/{group_id}/votes/{vote_id}/close", response_model=CloseVoteResponse)
def close_vote_for_group(
    group_id: int,
    vote_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    winner_id = crud.close_vote_and_apply(db, vote_id=vote_id, closer_id=_admin.id)
    return {"winning_book_id": winner_id}


@router.post("/{group_id}/add_member", response_model=dict)
def add_member(
    group_id: int,
    payload: MemberPayload,
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    result = crud.add_member_to_group(db, group_id, payload.member_id)
    # result is a dict {status, group}
    if result["status"] == "exists":
        return {"message": "Member already in group"}
    return {"message": "Member added"}


@router.post("/{group_id}/remove_member", response_model=dict)
def remove_member(
    group_id: int,
    payload: MemberPayload,
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    result = crud.remove_member_from_group(db, group_id, payload.member_id)
    if result["status"] == "not_in_group":
        return {"message": "Member not in group"}
    return {"message": "Member removed"}


@router.post("/{group_id}/set_active_book", response_model=dict)
def set_active_book(
    group_id: int,
    payload: BookPayload,
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    # crud.set_group_active_book will raise HTTPException on missing entities
    crud.set_group_active_book(db, group_id, payload.book_id)
    return {"message": "Active book set"}
