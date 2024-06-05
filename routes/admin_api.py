from fastapi import Depends, APIRouter, HTTPException, FastAPI
from schemas import Intent, IntentCreate
from training import train
from repository import find_all_intents, create_intent, find_by_tag, delete_by_tag
from database import SessionLocal

from sqlalchemy.orm import Session

admin = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# model apis


@admin.get("/admin/model/train")
def train_model():
    return train()


@admin.post("/admin/intent/create", response_model=Intent)
def create_intent_api(intent: IntentCreate, db: Session = Depends(get_db)):
    db_intent = find_by_tag(db, tag=intent.tag)
    if db_intent:
        raise HTTPException(status_code=400, detail="Tag already created")

    return create_intent(db=db, intent=intent)


@admin.put("/admin/intent/update", response_model=Intent)
def update_intent_api(intent: IntentCreate, db: Session = Depends(get_db)):
    db_intent = find_by_tag(db, tag=intent.tag)
    if not db_intent:
        raise HTTPException(status_code=404, detail="Tag not found")

    delete_by_tag(db, tag=intent.tag)
    return create_intent(db=db, intent=intent)


@admin.get("/admin/intents", response_model=list[IntentCreate])
def find_all_intents_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_intents = find_all_intents(
        db, skip=skip, limit=limit)  

    return [
        IntentCreate(
            id=intent.id,
            tag=intent.tag,
            response_text=intent.response_text,
            input_patterns=[
                pattern.text for pattern in intent.input_patterns],
            response_links=[link.url for link in intent.response_links],
        )
        for intent in db_intents
    ]

@admin.get("/admin/intent/{tag}", response_model=IntentCreate)
def find_by_tag_api(tag: str, db: Session = Depends(get_db)):
    db_intent = find_by_tag(db, tag=tag)
    if not db_intent:
        raise HTTPException(status_code=404, detail="Tag not found")

    return IntentCreate(
        id=db_intent.id,
        tag=db_intent.tag,
        response_text=db_intent.response_text,
        input_patterns=[pattern.text for pattern in db_intent.input_patterns],
        response_links=[link.url for link in db_intent.response_links],
    )


@admin.delete("/admin/intent/delete/{tag}")
def delete_intent_api(tag: str, db: Session = Depends(get_db)):
    db_intent = find_by_tag(db, tag=tag)
    if not db_intent:
        raise HTTPException(status_code=404, detail="Tag not found")

    delete_by_tag(db, tag=tag)
    return {"message": "Intent deleted successfully"}
