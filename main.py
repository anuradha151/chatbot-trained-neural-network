from typing import Union

from fastapi import FastAPI
from training import train
from chatbot import chat

app = FastAPI()

@app.get("/train")
def train_model():
    return train()


@app.get("/chat/{message}")
def read_root(message):
    return chat(message)

