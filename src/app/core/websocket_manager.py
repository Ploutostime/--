import asyncio


class WebSocketManager:
    def __init__(self):
        self.active_connections = {}

    def add_connection(self, websocket, user_id: str):
        self.active_connections[user_id] = websocket

    def remove_connection(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            maybe = websocket.send_text(message)
            if asyncio.iscoroutine(maybe):
                await maybe

    def broadcast(self, message: str):
        for connection in self.active_connections.values():
            try:
                maybe = connection.send_text(message)
                if asyncio.iscoroutine(maybe):
                    asyncio.create_task(maybe)
            except Exception:
                # ignore errors in broadcast
                pass