from sqlalchemy.orm import Session

from models import Intent, InputPattern, ResponseLink
from schemas import IntentCreate

def create_intent(db: Session, intent: IntentCreate):
    db_intent = Intent(tag=intent.tag, response_text=intent.response_text)
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    db.add_all([InputPattern(text=text, intent_id=db_intent.id) for text in intent.input_patterns])
    db.add_all([ResponseLink(text=link, intent_id=db_intent.id) for link in intent.response_links])
    db.commit()
    return db_intent

def find_all_intents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Intent).offset(skip).limit(limit).all()

def find_by_tag(db: Session, tag: str):
    return db.query(Intent).filter(Intent.tag == tag).first()
