from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    return sorted(crud.get_all(db, models.Member), key=lambda b: b.name)


@router.post("/create_member", response_model=schemas.CreateResponse, status_code=201)
async def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    crud.create_all(db, models.Member, member)
    return {"message": "Member created successfully"}
