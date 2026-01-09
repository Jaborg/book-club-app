from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[schemas.BookOut])
async def read_root(member_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Book)

    if member_id is not None:
        query = query.filter(models.Book.member_id.is_(member_id))

    return sorted(query.all(), key=lambda b: b.name)


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id.is_(book_id).first())
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/create_book", response_model=schemas.CreateResponse, status_code=201)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    crud.create_all(db, models.Book, book)
    return {"message": "Books created successfully"}
