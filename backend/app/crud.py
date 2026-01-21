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
    is_admin: bool = False,
):
    """Create a new member"""
    db_member = Member(
        name=name,
        email=email,
        password_hash=password_hash,
        join_date=join_date,
        is_admin=is_admin,
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


def create_vote(
    db: Session, group_id: int, creator_id: int, candidate_book_ids: list[int]
):
    """Create a Vote with candidate books. Only existing books may be candidates.

    Raises NotFound/BadRequest via helpers on invalid input.
    """
    group = get_by_id(db, BookGroup, group_id)
    if not group:
        not_found("Group")

    # ensure creator exists and is a member of the group
    creator = get_by_id(db, Member, creator_id)
    if not creator:
        not_found("Member")
    if creator not in group.members and not creator.is_admin:
        bad_request("Creator must be a member of the group or an admin")

    # ensure candidate books exist
    books = db.query(Book).filter(Book.id.in_(candidate_book_ids)).all()
    if len(books) != len(set(candidate_book_ids)):
        bad_request("One or more candidate books not found")

    from app.models.vote_model import Vote, VoteCandidate

    vote = Vote(group_id=group_id, created_by_id=creator_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)

    # create candidate entries
    for bid in candidate_book_ids:
        vc = VoteCandidate(vote_id=vote.id, book_id=bid)
        db.add(vc)
    db.commit()
    db.refresh(vote)
    return vote


def cast_vote(db: Session, vote_id: int, voter_id: int, book_id: int):
    """Cast a vote for a candidate book.
    Prevent double-voting and ensure candidate membership."""
    from app.models.vote_model import Vote, VoteCandidate, VoteCast

    vote = get_by_id(db, Vote, vote_id)
    if not vote:
        not_found("Vote")
    if not vote.is_open:
        bad_request("Vote is closed")

    voter = get_by_id(db, Member, voter_id)
    if not voter:
        not_found("Member")

    # ensure voter belongs to the group
    group = get_by_id(db, BookGroup, vote.group_id)
    if voter not in group.members and not voter.is_admin:
        bad_request("Voter must be a member of the group")

    # ensure book is a candidate
    candidate = (
        db.query(VoteCandidate)
        .filter(VoteCandidate.vote_id == vote_id, VoteCandidate.book_id == book_id)
        .first()
    )
    if not candidate:
        bad_request("Book is not a candidate for this vote")

    # ensure not already voted
    existing = (
        db.query(VoteCast)
        .filter(VoteCast.vote_id == vote_id, VoteCast.member_id == voter_id)
        .first()
    )
    if existing:
        bad_request("Member has already voted")

    cast = VoteCast(vote_id=vote_id, member_id=voter_id, book_id=book_id)
    db.add(cast)
    db.commit()
    db.refresh(cast)
    return cast


def close_vote_and_apply(db: Session, vote_id: int, closer_id: int):
    """Close a vote, compute winner, set group's active book to winner.

    Returns the winning book id.
    """
    from sqlalchemy import func

    from app.models.vote_model import Vote, VoteCast

    vote = get_by_id(db, Vote, vote_id)
    if not vote:
        not_found("Vote")
    if not vote.is_open:
        bad_request("Vote already closed")

    # closer must be admin (we also check at route level) or group member
    closer = get_by_id(db, Member, closer_id)
    if not closer:
        not_found("Member")

    # tally votes
    counts = (
        db.query(VoteCast.book_id, func.count(VoteCast.id).label("cnt"))
        .filter(VoteCast.vote_id == vote_id)
        .group_by(VoteCast.book_id)
        .all()
    )
    if not counts:
        bad_request("No votes cast")

    # pick highest count; tie-breaker: smallest book_id
    winner_book_id = sorted(counts, key=lambda r: (-r.cnt, r.book_id))[0].book_id

    # set group's active book
    set_group_active_book(db, vote.group_id, winner_book_id)

    # mark vote closed
    vote.is_open = False
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return winner_book_id


def promote_member_to_admin(db: Session, member_id: int):
    member = get_by_id(db, Member, member_id)
    if not member:
        not_found("Member")
    member.is_admin = True
    db.add(member)
    db.commit()
    db.refresh(member)
    return member
