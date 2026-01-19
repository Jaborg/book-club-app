from datetime import datetime

from sqlalchemy.orm import Session

from app import models
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
