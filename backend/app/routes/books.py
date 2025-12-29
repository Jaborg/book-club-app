from fastapi import APIRouter,Depends,Form
from datetime import datetime
from sqlalchemy.orm import Session



from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/books",tags=["books"])

@router.get("/")
def read_root(db: Session = Depends(get_db)):
    books = crud.get_all(db,models.Book)

    return books

@router.post("/create_book")
def read_root(
    name: str = Form(...),
    author: str = Form(...),
    member_id: int = Form(...),
    due_date: datetime = Form(...),
    rating: str = Form(...),
    db: Session = Depends(get_db)):

    book_data = schemas.BookCreate(
        name=name,
        author=author,
        member_id=member_id,
        due_date=due_date,
        rating=rating,
        initial_date=datetime.utcnow()
    )

    crud.create_all(db, models.Book, book_data)
    return book_data

