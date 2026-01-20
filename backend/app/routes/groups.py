from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.exceptions import ensure_exists
from app.models.book_group import BookGroup
from app.schemas.book_schema import BookPayload
from app.schemas.group_schema import GroupCreate, GroupOut
from app.schemas.member_schema import MemberPayload

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
def create_group(payload: GroupCreate, db: Session = Depends(get_db)):
    # Delegate validation and creation to crud.create_group
    group = crud.create_group(
        db,
        name=payload.name,
        member_ids=payload.member_ids,
        active_book_id=payload.active_book_id,
    )
    return {"message": "Group created", "id": group.id}


@router.post("/{group_id}/add_member", response_model=dict)
def add_member(group_id: int, payload: MemberPayload, db: Session = Depends(get_db)):
    result = crud.add_member_to_group(db, group_id, payload.member_id)
    # result is a dict {status, group}
    if result["status"] == "exists":
        return {"message": "Member already in group"}
    return {"message": "Member added"}


@router.post("/{group_id}/remove_member", response_model=dict)
def remove_member(group_id: int, payload: MemberPayload, db: Session = Depends(get_db)):
    result = crud.remove_member_from_group(db, group_id, payload.member_id)
    if result["status"] == "not_in_group":
        return {"message": "Member not in group"}
    return {"message": "Member removed"}


@router.post("/{group_id}/set_active_book", response_model=dict)
def set_active_book(group_id: int, payload: BookPayload, db: Session = Depends(get_db)):
    # crud.set_group_active_book will raise HTTPException on missing entities
    crud.set_group_active_book(db, group_id, payload.book_id)
    return {"message": "Active book set"}
