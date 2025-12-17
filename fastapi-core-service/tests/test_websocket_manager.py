from fastapi import WebSocket
import pytest
from src.app.core.websocket_manager import WebSocketManager

@pytest.fixture
def websocket_manager():
    return WebSocketManager()

def test_add_connection(websocket_manager):
    websocket = WebSocket(None)
    websocket_manager.add_connection(websocket, "test_user")
    assert websocket_manager.active_connections["test_user"] == websocket

def test_remove_connection(websocket_manager):
    websocket = WebSocket(None)
    websocket_manager.add_connection(websocket, "test_user")
    websocket_manager.remove_connection("test_user")
    assert "test_user" not in websocket_manager.active_connections

def test_broadcast_message(websocket_manager):
    websocket1 = WebSocket(None)
    websocket2 = WebSocket(None)
    websocket_manager.add_connection(websocket1, "user1")
    websocket_manager.add_connection(websocket2, "user2")

    # Mock the send method
    websocket1.send_text = pytest.Mock()
    websocket2.send_text = pytest.Mock()

    websocket_manager.broadcast("Hello, World!")

    websocket1.send_text.assert_called_with("Hello, World!")
    websocket2.send_text.assert_called_with("Hello, World!")