from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from src.app.core.websocket_manager import WebSocketManager
from src.app.core.conversation_service import ConversationService

router = APIRouter()
ws_manager = WebSocketManager()
conversation_service = ConversationService()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    ws_manager.add_connection(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_message(user_id, f"Echo: {data}")
    except WebSocketDisconnect:
        ws_manager.remove_connection(user_id)
