from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, index=True)
    response_text = Column(String, index=True)

    text_patterns = relationship("TextPattern", back_populates="intent")
    response_links = relationship("ResponseLink", back_populates="intent")


class TextPattern(Base):
    __tablename__ = "text_patterns"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="text_patterns")


class ResponseLink(Base):
    __tablename__ = "response_links"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="response_links")