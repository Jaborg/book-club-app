from sqlalchemy.orm import Session
from app import models, schemas


def get_all(db: Session, obj: models):
    """Select all query"""
    query = db.query(obj)
    return query.all()


def create_all(db: Session, model: models, obj: schemas):
    """Create a new object"""
    db_object = model(**obj.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

