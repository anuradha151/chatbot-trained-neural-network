from fastapi import FastAPI

from routes.admin_api import admin
from routes.chatbot_api import chatbot

from models import Base
from database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin)
app.include_router(chatbot)
