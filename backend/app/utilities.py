from datetime import datetime, timedelta
from typing import Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models.member_model import Member

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for Bearer tokens, used by dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def is_incorrect_login():
    return "Incorrect email or password"


def get_current_member(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Member:
    """Decode token and return the Member model from the DB.

    Raises HTTP 401 when token is invalid or member not found.
    """
    try:
        payload = decode_access_token(token)
        member_sub = payload.get("sub")
        if member_sub is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        member_id = int(member_sub)
    except Exception:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        ) from None

    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=401, detail="Member not found")
    return member


def admin_required(current_member: Member = Depends(get_current_member)) -> Member:
    """Dependency that ensures the current member is an admin.

    Raises HTTP 403 if not an admin.
    """
    if not getattr(current_member, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_member
