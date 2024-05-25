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
    text: str

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
    pass

class Intent(IntentBase):
    id: int
    input_patterns: list[InputPattern] = []
    links: list[ResponseLink] = []

    class Config:
        orm_mode = True
