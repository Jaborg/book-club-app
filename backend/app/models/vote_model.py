from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("book_groups.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    is_open = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("BookGroup", back_populates="votes")
    creator = relationship("Member")
    candidates = relationship(
        "VoteCandidate", back_populates="vote", cascade="all, delete-orphan"
    )
    casts = relationship(
        "VoteCast", back_populates="vote", cascade="all, delete-orphan"
    )


class VoteCandidate(Base):
    __tablename__ = "vote_candidates"

    id = Column(Integer, primary_key=True, index=True)
    vote_id = Column(Integer, ForeignKey("votes.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    vote = relationship("Vote", back_populates="candidates")
    book = relationship("Book")


class VoteCast(Base):
    __tablename__ = "vote_casts"

    id = Column(Integer, primary_key=True, index=True)
    vote_id = Column(Integer, ForeignKey("votes.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vote = relationship("Vote", back_populates="casts")
    member = relationship("Member")
    book = relationship("Book")
