from datetime import datetime

from sqlalchemy.orm import Session

from app import models
from app.exceptions import bad_request, not_found
from app.models.book_group import BookGroup
from app.models.book_model import Book
from app.models.member_model import Member


def get_all(db: Session, obj: models):
    """Select all query"""
    query = db.query(obj)
    return query.all()


def create_book(
    db: Session,
    name: str,
    author: str,
    member_id: int,
    original_due_date: datetime,
    rating: str,
    initial_date: datetime | None = None,
    revised_due_date: datetime | None = None,
):
    """Create a new book"""
    db_book = Book(
        name=name,
        author=author,
        member_id=member_id,
        original_due_date=original_due_date,
        rating=rating,
        initial_date=initial_date,
        revised_due_date=revised_due_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_member(
    db: Session,
    name: str,
    email: str,
    password_hash: str,
    join_date: datetime | None = None,
):
    """Create a new member"""
    db_member = Member(
        name=name,
        email=email,
        password_hash=password_hash,
        join_date=join_date,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_by_id(db: Session, model, obj_id: int):
    return db.query(model).filter(model.id == obj_id).first()


def create_group(
    db: Session,
    name: str,
    member_ids: list[int] | None = None,
    active_book_id: int | None = None,
):
    """Create a group with optional member IDs and optional active book.

    This function centralizes validation and raises HTTPException on errors so
    routes don't need to duplicate checks.
    """
    group = BookGroup(name=name)

    if active_book_id:
        book = get_by_id(db, Book, active_book_id)
        if not book:
            not_found("Active book")
        group.active_book = book

    if member_ids:
        members = db.query(Member).filter(Member.id.in_(member_ids)).all()
        if len(members) != len(set(member_ids)):
            # some member ids not found
            bad_request("One or more members not found")
        group.members = members

    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def add_member_to_group(db: Session, group_id: int, member_id: int):
    """Add a member to a group.

    Returns a dict with 'status' and 'group'. Status values: 'added', 'exists'.
    Raises HTTPException(404) if group or member not found.
    """
    group = get_by_id(db, BookGroup, group_id)
    if not group:
        not_found("Group")
    member = get_by_id(db, Member, member_id)
    if not member:
        not_found("Member")
    if member in group.members:
        return {"status": "exists", "group": group}
    group.members.append(member)
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"status": "added", "group": group}


def remove_member_from_group(db: Session, group_id: int, member_id: int):
    """Remove a member from a group.

    Returns a dict with 'status' and 'group'. Status values: 'removed', 'not_in_group'.
    Raises HTTPException(404) if group or member not found.
    """
    group = get_by_id(db, BookGroup, group_id)
    if not group:
        not_found("Group")
    member = get_by_id(db, Member, member_id)
    if not member:
        not_found("Member")
    if member not in group.members:
        return {"status": "not_in_group", "group": group}
    group.members.remove(member)
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"status": "removed", "group": group}


def set_group_active_book(db: Session, group_id: int, book_id: int):
    group = get_by_id(db, BookGroup, group_id)
    if not group:
        not_found("Group")
    book = get_by_id(db, Book, book_id)
    if not book:
        not_found("Book")
    group.active_book = book
    db.add(group)
    db.commit()
    db.refresh(group)
    return group
