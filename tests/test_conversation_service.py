import pytest
from src.app.core.conversation_service import ConversationService

@pytest.fixture
def conversation_service():
    return ConversationService()

def test_start_conversation(conversation_service):
    conversation_id = conversation_service.start_conversation()
    assert conversation_id is not None

def test_send_message(conversation_service):
    conversation_id = conversation_service.start_conversation()
    response = conversation_service.send_message(conversation_id, "Hello!")
    assert response == "Message sent"

def test_get_conversation_history(conversation_service):
    conversation_id = conversation_service.start_conversation()
    conversation_service.send_message(conversation_id, "Hello!")
    history = conversation_service.get_conversation_history(conversation_id)
    assert len(history) == 1
    assert history[0] == "Hello!"