from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models.member_model import Member
from app.schemas.general_schema import CreateResponse
from app.schemas.member_schema import MemberCreate, MemberOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    # ensure email not already used
    exists = db.query(Member).filter(Member.email == member.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(member.password)

    crud.create_member(
        db=db,
        name=member.name,
        email=member.email,
        password_hash=hashed,
        join_date=member.join_date,
    )

    return {"message": f"{member.name} created successfully"}
