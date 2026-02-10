from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    sender: str
    content: str

class ConversationCreate(BaseModel):
    title: str
    participants: List[str]

class ConversationResponse(BaseModel):
    id: str
    title: str
    participants: List[str]
    messages: List[Message] = []

class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[Message]