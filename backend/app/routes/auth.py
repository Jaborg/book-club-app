from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member_model import Member
from app.schemas.member_schema import MemberLogin
from app.utilities import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(member: MemberLogin, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.email == member.email).first()
    if not db_member:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(member.password, db_member.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token({"sub": str(db_member.id), "email": db_member.email})
    return {"access_token": token, "token_type": "bearer"}
