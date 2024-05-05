from typing import Union

from fastapi import FastAPI
from chatbot

app = FastAPI()


@app.get("/")
def read_root():
    return "Hellow Chatterbot!"

