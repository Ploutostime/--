from typing import List, Dict, Any

class ConversationService:
    def __init__(self):
        self.conversations: Dict[str, List[str]] = {}

    def start_conversation(self, user_id: str) -> str:
        conversation_id = f"conversation_{user_id}"
        self.conversations[conversation_id] = []
        return conversation_id

    def send_message(self, conversation_id: str, message: str) -> None:
        if conversation_id in self.conversations:
            self.conversations[conversation_id].append(message)

    def get_conversation_history(self, conversation_id: str) -> List[str]:
        return self.conversations.get(conversation_id, [])