from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    user_id: str
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    id: str
    user_id: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime

    def add_message(self, user_id: str, content: str):
        message = Message(user_id=user_id, content=content, timestamp=datetime.now())
        self.messages.append(message)
        self.updated_at = datetime.now()