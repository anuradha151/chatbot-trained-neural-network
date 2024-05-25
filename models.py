from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, index=True)
    response_text = Column(String, index=True)

    input_patterns = relationship("InputPattern", back_populates="intent")
    response_links = relationship("ResponseLink", back_populates="intent")


class InputPattern(Base):
    __tablename__ = "input_patterns"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="input_patterns")


class ResponseLink(Base):
    __tablename__ = "response_links"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="response_links")