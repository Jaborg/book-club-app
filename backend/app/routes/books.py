from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/books",tags=["books"])

@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    books = crud.get_all(db,models.Book)

    return books

@router.post("/create_book")
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)):

    crud.create_all(db, models.Book, book)
    return book

