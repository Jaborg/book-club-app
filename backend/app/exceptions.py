from fastapi import HTTPException


def not_found(entity: str = "Resource") -> None:
    """Raise a 404 HTTPException with a standardized message."""
    raise HTTPException(status_code=404, detail=f"{entity} not found")


def bad_request(detail: str) -> None:
    """Raise a 400 HTTPException with the provided detail."""
    raise HTTPException(status_code=400, detail=detail)


def conflict(detail: str) -> None:
    """Raise a 409 HTTPException for conflicts (e.g., duplicate email)."""
    raise HTTPException(status_code=409, detail=detail)


def invalid_credentials() -> None:
    """Raise a 400 indicating authentication failed with generic message."""
    raise HTTPException(status_code=400, detail="Incorrect email or password")


def ensure_exists(obj, entity: str = "Resource"):
    """Utility that raises 404 if obj is falsy and returns the obj otherwise.

    This makes route code concise:
        member = crud.get_by_id(...)
        ensure_exists(member, "Member")
    """
    if not obj:
        not_found(entity)
    return obj
