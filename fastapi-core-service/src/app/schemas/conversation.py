from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    user_id: str
    content: str
    timestamp: datetime

class ConversationCreate(BaseModel):
    user_id: str
    messages: List[Message]

class ConversationResponse(BaseModel):
    id: str
    user_id: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime

class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]