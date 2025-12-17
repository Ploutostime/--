from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from app.core.websocket_manager import WebSocketManager
from app.core.conversation_service import ConversationService

router = APIRouter()
manager = WebSocketManager()
conversation_service = ConversationService()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await conversation_service.handle_message(user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)