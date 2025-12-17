from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from db import Base


class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(128))
    instruction = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DocumentRecord(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(256), nullable=True)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)
    milvus_id = Column(String(128), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConversationRecord(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MessageRecord(Base):
    __tablename__ = "messages"
    id = Column(String(36), primary_key=True, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    user_id = Column(String(36), nullable=True)
    role = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
