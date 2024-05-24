from fastapi import FastAPI

from routes.admin_api import admin
from routes.chatbot_api import chatbot

app = FastAPI()
app.include_router(admin)
app.include_router(chatbot)
