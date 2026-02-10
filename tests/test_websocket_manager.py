import pytest
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


def test_add_connection(websocket_manager):
    class DummyWS:
        def send_text(self, msg):
            pass

    websocket = DummyWS()
    websocket_manager.add_connection(websocket, "test_user")
    assert websocket_manager.active_connections["test_user"] == websocket


def test_remove_connection(websocket_manager):
    class DummyWS:
        def send_text(self, msg):
            pass

    websocket = DummyWS()
    websocket_manager.add_connection(websocket, "test_user")
    websocket_manager.remove_connection("test_user")
    assert "test_user" not in websocket_manager.active_connections


def test_broadcast_message(websocket_manager):
    class DummyWS:
        def __init__(self):
            self.last = None

        def send_text(self, msg):
            self.last = msg

    websocket1 = DummyWS()
    websocket2 = DummyWS()
    websocket_manager.add_connection(websocket1, "user1")
    websocket_manager.add_connection(websocket2, "user2")

    websocket_manager.broadcast("Hello, World!")

    assert websocket1.last == "Hello, World!"
    assert websocket2.last == "Hello, World!"
