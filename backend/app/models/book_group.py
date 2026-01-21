from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class BookGroup(Base):
    __tablename__ = "book_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # optional active book
    active_book_id = Column(Integer, ForeignKey("books.id"), nullable=True)

    # relationships
    active_book = relationship("Book", foreign_keys=[active_book_id])
    # members relationship uses association table defined in member_model
    members = relationship("Member", secondary="group_members", back_populates="groups")
    # votes started for this group
    votes = relationship("Vote", back_populates="group", cascade="all, delete-orphan")
