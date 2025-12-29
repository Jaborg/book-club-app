from fastapi import APIRouter,Depends,Form
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/members",tags=["members"])

@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    books = crud.get_all(db,models.Member)

    return books

@router.post("/create_member")
async def read_root(
    member: schemas.MemberCreate,
    db: Session = Depends(get_db)):

    crud.create_all(db, models.Member, member)
    return member

