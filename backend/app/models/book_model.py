from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"))

    due_date = Column(DateTime, nullable=False)
    rating = Column(String, nullable=False)
    initial_date = Column(DateTime, default=datetime.utcnow)
    revised_date = Column(DateTime, default=None)

    member = relationship("Member", back_populates="books")
