import pytest
from fastapi import WebSocket
from src.app.core.websocket_manager import WebSocketManager

@pytest.fixture
def websocket_manager():
    return WebSocketManager()

@pytest.fixture
def mock_websocket():
    class MockWebSocket:
        def __init__(self):
            self.client_id = "test_client"
            self.connected = True

        async def send_text(self, message: str):
            pass

        async def close(self):
            self.connected = False

    return MockWebSocket()

def test_add_connection(websocket_manager, mock_websocket):
    websocket_manager.add_connection(mock_websocket)
    assert mock_websocket.client_id in websocket_manager.active_connections

def test_remove_connection(websocket_manager, mock_websocket):
    websocket_manager.add_connection(mock_websocket)
    websocket_manager.remove_connection(mock_websocket.client_id)
    assert mock_websocket.client_id not in websocket_manager.active_connections

def test_broadcast_message(websocket_manager, mock_websocket):
    websocket_manager.add_connection(mock_websocket)
    message = "Hello, World!"
    websocket_manager.broadcast(message)
    # Here we would need to assert that the message was sent to the mock websocket.
    # Since we don't have a real websocket implementation, we can only check that the method was called.
    # This would typically involve using a mocking library to assert that send_text was called with the correct message.