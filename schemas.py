from os import link
from pydantic import BaseModel

# InputPattern 
class InputPatternBase(BaseModel):
    text: str

class InputPatternCreate(InputPatternBase):
    pass

class InputPattern(InputPatternBase):
    id: int
    intent_id: int

    class Config:
        orm_mode = True


# ResponseLink
class ResponseLinkBase(BaseModel):
    url: str

class ResponseLinkCreate(ResponseLinkBase):
    pass

class ResponseLink(ResponseLinkBase):
    id: int
    intent_id: int

    class Config:
        orm_mode = True


# Intent
class IntentBase(BaseModel):
    tag: str
    response_text: str

class IntentCreate(IntentBase):
    input_patterns: list[str] = []
    response_links: list[str] = []
    pass

class Intent(IntentBase):
    id: int
    input_patterns: list[InputPattern] = []
    response_links: list[ResponseLink] = []

    class Config:
        orm_mode = True

class IntentResponse(IntentCreate):
    id: int
