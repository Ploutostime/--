from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    id: str
    participants: List[str]
    messages: List[Message] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()