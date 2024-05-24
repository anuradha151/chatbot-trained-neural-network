from sqlalchemy.orm import Session

from . import models

def get_intents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


