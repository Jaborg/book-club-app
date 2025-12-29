from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"))

    due_date = Column(DateTime, nullable=False)
    rating = Column(String, nullable=False)
    initial_date = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member", back_populates="books")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="member")