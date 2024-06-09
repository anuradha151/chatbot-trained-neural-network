import json

from sqlalchemy.orm import Session

from models import Intent, InputPattern, ResponseLink
from schemas import IntentCreate, IntentTrainData


def create_intent(db: Session, intent: IntentCreate):
    db_intent = Intent(tag=intent.tag, response_text=intent.response_text)
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    db.add_all([InputPattern(text=text, intent_id=db_intent.id)
               for text in intent.input_patterns])
    db.add_all([ResponseLink(url=link, intent_id=db_intent.id)
               for link in intent.response_links])
    db.commit()
    return db_intent


def find_all_intents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Intent).offset(skip).limit(limit).all()


def find_by_tag(db: Session, tag: str):
    return db.query(Intent).filter(Intent.tag == tag).first()


def delete_by_tag(db: Session, tag: str):
    intent = db.query(Intent).filter(Intent.tag == tag).first()
    if intent:
        orphaned_patterns = db.query(InputPattern).filter(
            InputPattern.intent_id == intent.id).all()
        for pattern in orphaned_patterns:
            db.delete(pattern)
        orphaned_links = db.query(ResponseLink).filter(
            ResponseLink.intent_id == intent.id).all()
        for link in orphaned_links:
            db.delete(link)
        db.delete(intent)
        db.commit()

def find_all_intents_for_train(db: Session):
    intents = db.query(Intent).all()
    return [
        IntentTrainData(
            tag=intent.tag,
            patterns=[pattern.text for pattern in intent.input_patterns]
        )
        for intent in intents
    ]


# def find_all_intents_for_train(db: Session):
#     intents = db.query(Intent).all()
#     # Convert each IntentTrainData object to a dictionary
#     intent_data_list = [
#         intent.model_dump() for intent in [IntentTrainData(
#             tag=intent.tag,
#             patterns=[pattern.text for pattern in intent.input_patterns]
#         ) for intent in intents]
#     ]
#     # Use json.dumps to convert the list of dictionaries to a JSON string
#     json_response = json.dumps(intent_data_list)
#     return json_response
