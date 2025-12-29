from fastapi import APIRouter,Depends,Form
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/members",tags=["members"])

@router.get("/")
def read_root(db: Session = Depends(get_db)):
    books = crud.get_all(db,models.Member)

    return books

@router.post("/create_member")
def read_root(
    name: str = Form(...),
    db: Session = Depends(get_db)):

    member_data = schemas.MemberCreate(
        name=name,
        join_date = datetime.utcnow()

    )

    crud.create_all(db, models.Member, member_data)
    return member_data

