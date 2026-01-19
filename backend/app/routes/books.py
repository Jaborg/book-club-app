from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models.book_model import Book
from app.schemas.book_schema import BookCreate, BookOut
from app.schemas.general_schema import CreateResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookOut])
async def read_root(member_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)

    if member_id is not None:
        query = query.filter(Book.member_id.is_(member_id))

    return sorted(query.all(), key=lambda b: b.name)


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id.is_(book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/create_book", response_model=CreateResponse, status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    crud.create_book(
        db,
        book.name,
        book.author,
        book.member_id,
        book.original_due_date,
        book.rating,
        book.initial_date,
        book.revised_due_date,
    )
    return {"message": "Book created successfully"}


@router.put("/{book_id}", response_model=BookOut)
async def update_book_due_date(book_id: int | None, db: Session = Depends(get_db)):
    """Update book due date"""
    return
