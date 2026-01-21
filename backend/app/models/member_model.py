from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False, nullable=False)

    books = relationship("Book", back_populates="member")
    # many-to-many: members can belong to multiple book groups
    # association table is defined in this module so other models can import it


# association table for BookGroup <-> Member
group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", ForeignKey("book_groups.id"), primary_key=True),
    Column("member_id", ForeignKey("members.id"), primary_key=True),
)

# backref relationship defined in BookGroup model (string reference used below)
Member.groups = relationship(
    "BookGroup", secondary=group_members, back_populates="members"
)
