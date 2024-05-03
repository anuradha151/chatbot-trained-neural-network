from typing import Union

from fastapi import FastAPI
from chatbot import chat

app = FastAPI()


@app.get("/")
def read_root():
    return chat()

