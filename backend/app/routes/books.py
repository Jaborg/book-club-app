from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    return sorted(crud.get_all(db, models.Book), key=lambda b: b.name)


@router.post("/create_book", response_model=schemas.CreateResponse, status_code=201)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    crud.create_all(db, models.Book, book)
    return {"message": "Books created successfully"}
