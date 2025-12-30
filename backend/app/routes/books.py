from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    books = sorted(crud.get_all(db, models.Book), key=lambda b: b.name)
    return books


@router.post("/create_book", response_model=schemas.BookResponse)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_all(db, models.Book, book)
    return db_book
