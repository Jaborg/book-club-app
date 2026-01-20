from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book_group import BookGroup
from app.models.book_model import Book
from app.models.member_model import Member
from app.schemas.book_schema import BookPayload
from app.schemas.group_schema import GroupCreate, GroupOut
from app.schemas.member_schema import MemberPayload

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=list[GroupOut])
def list_groups(db: Session = Depends(get_db)):
    groups = db.query(BookGroup).all()
    return groups


@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(BookGroup).filter(BookGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/", response_model=dict, status_code=201)
def create_group(payload: GroupCreate, db: Session = Depends(get_db)):
    # create group
    group = BookGroup(name=payload.name)

    # set active book if provided
    if payload.active_book_id:
        book = db.query(Book).filter(Book.id == payload.active_book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Active book not found")
        group.active_book = book

    # attach members
    if payload.member_ids:
        members = db.query(Member).filter(Member.id.in_(payload.member_ids)).all()
        if len(members) != len(set(payload.member_ids)):
            # some ids not found
            raise HTTPException(status_code=400, detail="One or more members not found")
        group.members = members

    db.add(group)
    db.commit()
    db.refresh(group)
    return {"message": "Group created", "id": group.id}


@router.post("/{group_id}/add_member", response_model=dict)
def add_member(group_id: int, payload: MemberPayload, db: Session = Depends(get_db)):
    group = db.query(BookGroup).filter(BookGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member in group.members:
        return {"message": "Member already in group"}

    group.members.append(member)
    db.add(group)
    db.commit()
    return {"message": "Member added"}


@router.post("/{group_id}/remove_member", response_model=dict)
def remove_member(group_id: int, payload: MemberPayload, db: Session = Depends(get_db)):
    group = db.query(BookGroup).filter(BookGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member not in group.members:
        return {"message": "Member not in group"}

    group.members.remove(member)
    db.add(group)
    db.commit()
    return {"message": "Member removed"}


@router.post("/{group_id}/set_active_book", response_model=dict)
def set_active_book(group_id: int, payload: BookPayload, db: Session = Depends(get_db)):
    group = db.query(BookGroup).filter(BookGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    group.active_book = book
    db.add(group)
    db.commit()
    return {"message": "Active book set"}
