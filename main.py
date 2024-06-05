from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware;

from routes.admin_api import admin
from routes.chatbot_api import chatbot

from models import Base
from database import engine



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin)
app.include_router(chatbot)
