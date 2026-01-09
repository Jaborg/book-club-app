from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/", response_model=list[schemas.MemberOut])
async def read_root(db: Session = Depends(get_db)):
    return sorted(crud.get_all(db, models.Member), key=lambda b: b.name)


@router.post("/create_member", response_model=schemas.CreateResponse, status_code=201)
async def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    crud.create_all(db, models.Member, member)
    return {"message": "Member created successfully"}


@router.get("/{member_id}", response_model=schemas.MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id.is_(member_id).first())
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
