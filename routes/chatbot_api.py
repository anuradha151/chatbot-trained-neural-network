from fastapi import APIRouter
from chatbot import chat

chatbot = APIRouter()


@chatbot.get("/chat/{message}")
def read_message(message):
    return {"message": chat(message)}
