from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models.member_model import Member
from app.schemas.general_schema import CreateResponse
from app.schemas.member_schema import MemberCreate, MemberOut

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/", response_model=list[MemberOut])
async def read_root(db: Session = Depends(get_db)):
    return sorted(crud.get_all(db, Member), key=lambda b: b.name)


@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id.is_(member_id)).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/create_member", response_model=CreateResponse, status_code=201)
async def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    crud.create_all(db, Member, member)
    return {"message": "Member created successfully"}
