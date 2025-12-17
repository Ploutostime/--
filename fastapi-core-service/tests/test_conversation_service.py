from fastapi import WebSocket
import pytest
from src.app.core.conversation_service import ConversationService

@pytest.fixture
def conversation_service():
    return ConversationService()

def test_start_conversation(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    assert conversation_id is not None
    assert conversation_service.get_conversation(conversation_id).user_id == user_id

def test_send_message(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    message = "Hello, World!"
    conversation_service.send_message(conversation_id, user_id, message)
    conversation = conversation_service.get_conversation(conversation_id)
    assert len(conversation.messages) == 1
    assert conversation.messages[0].content == message

def test_get_conversation(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    conversation = conversation_service.get_conversation(conversation_id)
    assert conversation is not None
    assert conversation.user_id == user_id

def test_end_conversation(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    conversation_service.end_conversation(conversation_id)
    conversation = conversation_service.get_conversation(conversation_id)
    assert conversation is None