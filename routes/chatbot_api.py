from fastapi import Depends, APIRouter
from chatbot import chat
from database import SessionLocal
from sqlalchemy.orm import Session

chatbot = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@chatbot.get("/chat/{message}")
def read_message(message, db: Session = Depends(get_db)):
    return chat(message, db)
