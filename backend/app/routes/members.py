from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.exceptions import conflict, ensure_exists
from app.models.member_model import Member
from app.schemas.general_schema import CreateResponse
from app.schemas.member_schema import MemberCreate, MemberOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/", response_model=list[MemberOut])
async def read_root(db: Session = Depends(get_db)):
    return sorted(crud.get_all(db, Member), key=lambda b: b.name)


@router.get("/{member_id}", response_model=MemberOut)
async def get_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_by_id(db, Member, member_id)
    return ensure_exists(member, "Member")


@router.post("/create_member", response_model=CreateResponse, status_code=201)
async def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    # ensure email not already used
    exists = db.query(Member).filter(Member.email == member.email).first()
    if exists:
        # email conflict
        conflict("Email already registered")
    hashed = pwd_context.hash(member.password)

    crud.create_member(
        db=db,
        name=member.name,
        email=member.email,
        password_hash=hashed,
        join_date=member.join_date,
    )

    return {"message": f"{member.name} created successfully"}
