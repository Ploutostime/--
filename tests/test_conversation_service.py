import pytest
from src.app.core.conversation_service import ConversationService

@pytest.fixture
def conversation_service():
    return ConversationService()

def test_start_conversation(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    assert conversation_id is not None

def test_add_message_and_get(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    message = "Hello, World!"
    msg = conversation_service.add_message(conversation_id, user_id, message)
    assert msg["content"] == message
    conversation = conversation_service.get_conversation(conversation_id)
    assert conversation is not None
    assert len(conversation["messages"]) >= 1

def test_end_behavior(conversation_service):
    user_id = "user123"
    conversation_id = conversation_service.start_conversation(user_id)
    # basic lifecycle: start and fetch
    conversation = conversation_service.get_conversation(conversation_id)
    assert conversation is not None